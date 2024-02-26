from itertools import count
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class ContenPDF:
    # id_generator: itertools.count(1) = itertools.count(1)
    heading: str
    content: str
    topic_id: int = Field(gt=0)
    

    id: int = Field(default_factory=count(1).__next__)

        
