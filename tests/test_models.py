import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from backend.models import Document, Annotation, Entity


def test_annotation_offsets_validation():
    entity = Entity(id="e1", label="PERSON")
    with pytest.raises(ValueError):
        Annotation(id="a1", document_id="d1", start_offset=5, end_offset=5, entity=entity)
    with pytest.raises(ValueError):
        Annotation(id="a1", document_id="d1", start_offset=-1, end_offset=5, entity=entity)


def test_document_annotation_relationship():
    doc = Document(id="d1", text="Hello world")
    entity = Entity(id="e1", label="GREETING")
    ann = Annotation(id="a1", document_id="d1", start_offset=0, end_offset=5, entity=entity)
    doc.add_annotation(ann)
    assert doc.annotations[0] is ann
    assert ann.entity.label == "GREETING"
    assert ann.start_offset == 0
    assert ann.end_offset == 5

    ann2 = Annotation(id="a2", document_id="d2", start_offset=6, end_offset=11, entity=entity)
    with pytest.raises(ValueError):
        doc.add_annotation(ann2)
