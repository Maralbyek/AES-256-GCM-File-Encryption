from pathlib import Path

import pytest

from aes_tool.crypto_engine import EncryptionError, decrypt_file, encrypt_file


PASSWORD = "correct horse battery staple"


def test_round_trip_preserves_binary_bytes(tmp_path: Path) -> None:
    original = tmp_path / "sample.bin"
    original.write_bytes(bytes(range(256)) * 32)

    encrypted = encrypt_file(original, PASSWORD, iterations=1_000)
    recovered = tmp_path / "recovered.bin"
    decrypt_file(encrypted, PASSWORD, recovered)

    assert recovered.read_bytes() == original.read_bytes()
    assert encrypted.read_bytes() != original.read_bytes()


def test_wrong_password_creates_no_output(tmp_path: Path) -> None:
    original = tmp_path / "secret.txt"
    original.write_text("private content", encoding="utf-8")
    encrypted = encrypt_file(original, PASSWORD, iterations=1_000)
    output = tmp_path / "wrong.txt"

    with pytest.raises(EncryptionError, match="incorrect password or modified file"):
        decrypt_file(encrypted, "wrong password", output)

    assert not output.exists()


def test_tampered_ciphertext_is_rejected(tmp_path: Path) -> None:
    original = tmp_path / "secret.txt"
    original.write_text("private content", encoding="utf-8")
    encrypted = encrypt_file(original, PASSWORD, iterations=1_000)
    data = bytearray(encrypted.read_bytes())
    data[-1] ^= 1
    encrypted.write_bytes(data)
    output = tmp_path / "tampered.txt"

    with pytest.raises(EncryptionError, match="incorrect password or modified file"):
        decrypt_file(encrypted, PASSWORD, output)

    assert not output.exists()


def test_malformed_file_is_rejected(tmp_path: Path) -> None:
    encrypted = tmp_path / "bad.enc"
    encrypted.write_bytes(b"not an encrypted file")

    with pytest.raises(EncryptionError, match="format is invalid"):
        decrypt_file(encrypted, PASSWORD, tmp_path / "output.bin")


def test_existing_destination_is_protected(tmp_path: Path) -> None:
    original = tmp_path / "sample.txt"
    original.write_text("content", encoding="utf-8")
    destination = tmp_path / "sample.enc"
    destination.write_bytes(b"keep me")

    with pytest.raises(EncryptionError, match="destination already exists"):
        encrypt_file(original, PASSWORD, destination, iterations=1_000)

    assert destination.read_bytes() == b"keep me"
