from dataclasses import dataclass, field
from typing import List
from .annotation import Annotation

@dataclass
class Document:
    """Text document that may contain annotations."""
    id: str
    text: str
    annotations: List[Annotation] = field(default_factory=list)

    def add_annotation(self, annotation: Annotation) -> None:
        if annotation.document_id != self.id:
            raise ValueError("Annotation document_id does not match Document id")
        self.annotations.append(annotation)
