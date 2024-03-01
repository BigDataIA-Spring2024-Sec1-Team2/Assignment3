from itertools import count
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class TopicPDF:
    id: int = Field(default_factory=count(1).__next__)
    level: str = Field(max_length=3)
    topic: str = Field(min_length=1)


