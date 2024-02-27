from pydantic import BaseModel, HttpUrl, validator
from typing import List
import csv

class UrlClass(BaseModel):
    pdfLink: HttpUrl  # Validates that the link is a proper URL
    parentTopic: str
    year: int
    level: str
    introduction: str
    learningOutcome: str
    summary: str
    categories: List[str]  # A list of strings
    topicName: str
    url: HttpUrl  # Validates that the link is a proper URL

    # Additional validation for the 'year' field to ensure it's a valid year
    @validator('year')
    def year_must_be_valid(cls, value):
        if not (1900 <= value <= 2099):
            raise ValueError('Year must be between 1900 and 2099')
        return value

          
    # You can add more validators here as needed for other fields
if __name__ == '__main__':
    data = {
    "pdfLink": "http://example.com/somefile.pdf",
    "parentTopic": "Science",
    "year": 2023,
    "level": "Beginner",
    "introduction": "This is an introduction.",
    "learningOutcome": "You will learn Pydantic.",
    "summary": "This is a summary.",
    "categories": ["Education", "Programming"],
    "topicName": "Pydantic Validation",
    "url": "http://example.com"
}
    try:
        url_instance = UrlClass(**data)
        print("Validation successful!")
        print(url_instance)
    except Exception as e:
        print(f"Validation error: {e}")

    

