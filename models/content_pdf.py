from itertools import count
from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class ContenPDF:
    # id_generator: itertools.count(1) = itertools.count(1)
    id: int = Field(default_factory=count(1).__next__)
    topic_id: int = Field(gt=0)
    heading: str = ""
    content: str = ""
    
    

    

        
