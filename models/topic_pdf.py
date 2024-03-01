from itertools import count
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class TopicPDF:
    id: int = Field(default_factory=count(1).__next__)
    level: str = Field(min_length=7)
    topic: str = Field(min_length=1)


