"""Password-based AES-256-GCM file encryption."""

from __future__ import annotations

import os
import struct
import tempfile
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b"AFET"
VERSION = 1
SALT_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32
DEFAULT_ITERATIONS = 480_000
HEADER = struct.Struct(">4sB I 16s 12s")


class EncryptionError(Exception):
    """Raised when an encryption or decryption operation cannot complete."""


def _derive_key(password: str, salt: bytes, iterations: int) -> bytes:
    if not password:
        raise EncryptionError("Password cannot be empty.")
    if len(salt) != SALT_SIZE:
        raise EncryptionError("Invalid salt.")
    if iterations < 1:
        raise EncryptionError("Invalid key-derivation parameters.")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def _atomic_write(destination: Path, data: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, destination)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def encrypt_file(
    source: str | Path,
    password: str,
    destination: str | Path | None = None,
    *,
    iterations: int = DEFAULT_ITERATIONS,
    overwrite: bool = False,
) -> Path:
    """Encrypt source bytes and return the created .enc path."""
    source_path = Path(source)
    if not source_path.is_file():
        raise EncryptionError("The selected source file cannot be accessed.")
    destination_path = Path(destination) if destination else Path(f"{source_path}.enc")
    if destination_path.exists() and not overwrite:
        raise EncryptionError("The destination already exists.")

    try:
        plaintext = source_path.read_bytes()
        salt = os.urandom(SALT_SIZE)
        nonce = os.urandom(NONCE_SIZE)
        key = _derive_key(password, salt, iterations)
        encrypted = AESGCM(key).encrypt(nonce, plaintext, None)
        ciphertext, tag = encrypted[:-TAG_SIZE], encrypted[-TAG_SIZE:]
        header = HEADER.pack(MAGIC, VERSION, iterations, salt, nonce)
        _atomic_write(destination_path, header + tag + ciphertext)
        return destination_path
    except EncryptionError:
        raise
    except OSError as exc:
        raise EncryptionError("The file could not be read or written.") from exc


def decrypt_file(
    source: str | Path,
    password: str,
    destination: str | Path | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    """Authenticate and decrypt an .enc file, then return the output path."""
    source_path = Path(source)
    if not source_path.is_file():
        raise EncryptionError("The selected encrypted file cannot be accessed.")
    destination_path = Path(destination) if destination else Path(str(source_path)[:-4])
    if destination_path.exists() and not overwrite:
        raise EncryptionError("The destination already exists.")

    try:
        encrypted_file = source_path.read_bytes()
        minimum_size = HEADER.size + TAG_SIZE
        if len(encrypted_file) < minimum_size:
            raise EncryptionError("The encrypted file format is invalid.")
        magic, version, iterations, salt, nonce = HEADER.unpack_from(encrypted_file)
        if magic != MAGIC or version != VERSION:
            raise EncryptionError("The encrypted file format is invalid.")
        tag_start = HEADER.size
        tag = encrypted_file[tag_start:tag_start + TAG_SIZE]
        ciphertext = encrypted_file[tag_start + TAG_SIZE:]
        key = _derive_key(password, salt, iterations)
        plaintext = AESGCM(key).decrypt(nonce, ciphertext + tag, None)
        _atomic_write(destination_path, plaintext)
        return destination_path
    except EncryptionError:
        raise
    except InvalidTag as exc:
        raise EncryptionError("Decryption failed: incorrect password or modified file.") from exc
    except (OSError, ValueError, struct.error) as exc:
        raise EncryptionError("The encrypted file could not be processed.") from exc
