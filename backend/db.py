"""SQLite-based data access layer for documents and annotations."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

# Path to the SQLite database file. Can be overridden via DATABASE_URL env var.
DB_PATH = os.environ.get("DATABASE_URL", str(Path(__file__).with_name("data.db")))


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row factory as dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database by executing migration SQL scripts."""
    migrations_dir = Path(__file__).with_name("migrations")
    init_sql = migrations_dir / "001_init.sql"
    with get_connection() as conn, open(init_sql, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


# ---------------------- Document operations ----------------------


def create_document(text: str) -> Dict[str, str]:
    """Insert a new document and return it."""
    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO documents (text) VALUES (?)", (text,))
        doc_id = cursor.lastrowid
    return {"id": str(doc_id), "text": text}


def get_document(doc_id: str) -> Optional[Dict[str, str]]:
    """Retrieve a document by ID."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id, text FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
    if row is None:
        return None
    return {"id": str(row["id"]), "text": row["text"]}


def list_documents() -> List[Dict[str, str]]:
    """Return all documents."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id, text FROM documents")
        rows = cursor.fetchall()
    return [{"id": str(r["id"]), "text": r["text"]} for r in rows]


def update_document(doc_id: str, text: str) -> Optional[Dict[str, str]]:
    """Update document text and return updated document."""
    with get_connection() as conn:
        conn.execute("UPDATE documents SET text = ? WHERE id = ?", (text, doc_id))
    return get_document(doc_id)


def delete_document(doc_id: str) -> None:
    """Delete a document by ID."""
    with get_connection() as conn:
        conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))


# ---------------------- Annotation operations ----------------------


def create_annotation(
    document_id: str,
    start_offset: int,
    end_offset: int,
    entity_id: str,
    entity_label: str,
) -> Dict[str, str]:
    """Insert a new annotation and return it."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO annotations (
                document_id, start_offset, end_offset, entity_id, entity_label
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (document_id, start_offset, end_offset, entity_id, entity_label),
        )
        ann_id = cursor.lastrowid
    return {
        "id": str(ann_id),
        "document_id": str(document_id),
        "start_offset": start_offset,
        "end_offset": end_offset,
        "entity_id": entity_id,
        "entity_label": entity_label,
    }


def get_annotation(ann_id: str) -> Optional[Dict[str, str]]:
    """Retrieve an annotation by ID."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, document_id, start_offset, end_offset, entity_id, entity_label FROM annotations WHERE id = ?",
            (ann_id,),
        )
        row = cursor.fetchone()
    if row is None:
        return None
    return {
        "id": str(row["id"]),
        "document_id": str(row["document_id"]),
        "start_offset": row["start_offset"],
        "end_offset": row["end_offset"],
        "entity_id": row["entity_id"],
        "entity_label": row["entity_label"],
    }


def list_annotations(document_id: Optional[str] = None) -> List[Dict[str, str]]:
    """Return all annotations, optionally filtered by document."""
    with get_connection() as conn:
        if document_id is None:
            cursor = conn.execute(
                "SELECT id, document_id, start_offset, end_offset, entity_id, entity_label FROM annotations"
            )
        else:
            cursor = conn.execute(
                "SELECT id, document_id, start_offset, end_offset, entity_id, entity_label FROM annotations WHERE document_id = ?",
                (document_id,),
            )
        rows = cursor.fetchall()
    return [
        {
            "id": str(r["id"]),
            "document_id": str(r["document_id"]),
            "start_offset": r["start_offset"],
            "end_offset": r["end_offset"],
            "entity_id": r["entity_id"],
            "entity_label": r["entity_label"],
        }
        for r in rows
    ]


def update_annotation(ann_id: str, **fields: Dict[str, object]) -> Optional[Dict[str, str]]:
    """Update fields of an annotation and return the updated annotation."""
    allowed = {"start_offset", "end_offset", "entity_id", "entity_label"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return get_annotation(ann_id)
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [ann_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE annotations SET {set_clause} WHERE id = ?", values)
    return get_annotation(ann_id)


def delete_annotation(ann_id: str) -> None:
    """Delete an annotation by ID."""
    with get_connection() as conn:
        conn.execute("DELETE FROM annotations WHERE id = ?", (ann_id,))
