"""Run the browser-based AES Vault interface."""

from __future__ import annotations

import argparse
import mimetypes
import tempfile
import webbrowser
from email import policy
from email.parser import BytesParser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from aes_tool.crypto_engine import EncryptionError, decrypt_file, encrypt_file
from aes_tool.database import recent_operations, record_operation

ROOT = Path(__file__).resolve().parent.parent / "frontend"


class VaultHandler(BaseHTTPRequestHandler):
    """Serve the interface and perform one-off local file operations."""

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/health":
            self._send_json({"ok": True})
            return
        if urlparse(self.path).path == "/api/history":
            self._send_json({"operations": recent_operations()})
            return
        requested = urlparse(self.path).path
        file_path = ROOT / ("index.html" if requested in ("", "/") else requested.lstrip("/"))
        if not file_path.is_file() or ROOT not in file_path.parents:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/process":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
            message = BytesParser(policy=policy.default).parsebytes(
                b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + body
            )
            fields = {}
            for part in message.walk():
                disposition = part.get("Content-Disposition", "")
                if "form-data" not in disposition:
                    continue
                field_name = part.get_param("name", header="Content-Disposition")
                if field_name:
                    fields[field_name] = part
            operation = fields.get("operation").get_content() if fields.get("operation") else "encrypt"
            password = fields.get("password").get_content() if fields.get("password") else ""
            upload = fields.get("file")
            if not password or upload is None or not upload.get_filename():
                raise EncryptionError("Choose a file and enter a password.")
            original_name = Path(upload.get_filename()).name
            with tempfile.TemporaryDirectory() as folder:
                source = Path(folder) / original_name
                source.write_bytes(upload.get_payload(decode=True) or b"")
                destination = Path(folder) / (original_name + ".enc" if operation == "encrypt" else Path(original_name).stem)
                created = (encrypt_file if operation == "encrypt" else decrypt_file)(source, password, destination)
                payload = created.read_bytes()
            record_operation(operation, original_name, len(payload))
            self._send_file(payload, created.name)
        except (EncryptionError, OSError, KeyError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        import json
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, data: bytes, filename: str) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="AES-256-GCM file encryption tool")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), VaultHandler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"AES Vault running at {url}")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
