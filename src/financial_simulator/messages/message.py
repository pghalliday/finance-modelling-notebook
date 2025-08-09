from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Message:
    source: Sequence[str]
    destination: Sequence[str]
