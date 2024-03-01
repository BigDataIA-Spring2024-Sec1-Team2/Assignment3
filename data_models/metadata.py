from pydantic.dataclasses import dataclass
from pydantic import Field
from typing import List

@dataclass
class MetadataPDF:
    pdf_id: int = Field(ge=1)
    name: str = Field(min_length=1)
    level: str = Field(max_length=2)
    year: int = Field(min=1800, max=3000)
    total_topics: int = Field(ge=0)
    topics: list = Field(List[str])
    total_sub_topics: int = Field(ge=0)
    sub_topics: list = Field(List[str])
    content_length: int = Field(ge=1)
    s3_filepath: str = Field(min_length=3)



