from dataclasses import dataclass
from .entity import Entity

@dataclass
class Annotation:
    """Span-based annotation tied to a document and entity."""
    id: str
    document_id: str
    start_offset: int
    end_offset: int
    entity: Entity

    def __post_init__(self) -> None:
        if self.start_offset < 0 or self.end_offset < 0:
            raise ValueError("Offsets must be non-negative")
        if self.start_offset >= self.end_offset:
            raise ValueError("start_offset must be less than end_offset")
