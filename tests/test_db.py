import os
import sys
import importlib

# Ensure backend package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backend.db as db


def setup_module(module):
    # Ensure a clean database for tests
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()
    importlib.reload(db)


def test_document_crud():
    doc = db.create_document("Hello")
    assert doc["text"] == "Hello"
    doc_id = doc["id"]
    assert db.get_document(doc_id) == doc
    docs = db.list_documents()
    assert any(d["id"] == doc_id for d in docs)
    updated = db.update_document(doc_id, "Hi")
    assert updated["text"] == "Hi"
    db.delete_document(doc_id)
    assert db.get_document(doc_id) is None


def test_annotation_crud():
    doc = db.create_document("Hello world")
    ann = db.create_annotation(
        document_id=doc["id"],
        start_offset=0,
        end_offset=5,
        entity_id="e1",
        entity_label="GREETING",
    )
    ann_id = ann["id"]
    assert db.get_annotation(ann_id)["entity_label"] == "GREETING"
    anns = db.list_annotations(document_id=doc["id"])
    assert anns[0]["id"] == ann_id
    updated = db.update_annotation(ann_id, start_offset=1)
    assert updated["start_offset"] == 1
    db.delete_annotation(ann_id)
    assert db.get_annotation(ann_id) is None
