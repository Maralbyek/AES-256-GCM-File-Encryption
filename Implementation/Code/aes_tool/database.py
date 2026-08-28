"""SQLite history for local AES Vault operations."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "aes_vault.db"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL CHECK(operation IN ('encrypt', 'decrypt')),
            filename TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    connection.commit()
    return connection


def record_operation(operation: str, filename: str, size_bytes: int) -> None:
    with _connect() as connection:
        connection.execute(
            "INSERT INTO operations (operation, filename, size_bytes, created_at) VALUES (?, ?, ?, ?)",
            (operation, filename, size_bytes, datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )
        connection.commit()


def recent_operations(limit: int = 8) -> list[dict[str, object]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, operation, filename, size_bytes, created_at FROM operations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
