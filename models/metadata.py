from pydantic.dataclasses import dataclass
from pydantic import Field, validator, HttpUrl
from typing import List
from itertools import count

@dataclass
class MetadataPDF:
    pdf_id: int = Field(default_factory=count(1).__next__)
    name: str = Field(min_length=1)
    level: str = Field(min_length=7)
    year: int = Field(min=1900, max=2099)
    total_topics: int = Field(ge=0)
    topics: list = Field(List[str])
    total_sub_topics: int = Field(ge=0)
    sub_topics: list = Field(List[str])
    content_length: int = Field(ge=1)
    s3_filepath: HttpUrl = ""# Validates that the link is a proper URL

    # Validation for the 'level' field to ensure it's one of the predefined levels
    @validator('level')
    def level_must_be_valid(cls, value):
        valid_levels = ['Level I', 'Level II', 'Level III']
        if value not in valid_levels:
            raise ValueError(f"Invalid level. Valid levels are: {', '.join(valid_levels)}")
        return value



