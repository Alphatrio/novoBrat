from dataclasses import dataclass

@dataclass
class Entity:
    """Represents a labeled concept."""
    id: str
    label: str
