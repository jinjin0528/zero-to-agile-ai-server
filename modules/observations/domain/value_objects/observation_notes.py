from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ObservationNotes:
    notes: Optional[dict] = None

    @classmethod
    def empty(cls) -> "ObservationNotes":
        return cls(notes=None)
