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
        if not (2000 <= value <= 2099):
            raise ValueError('Year must be between 1900 and 2099')
        return value

    # Validation for the 'level' field to ensure it's one of the predefined levels
    @validator('level')
    def level_must_be_valid(cls, value):
        valid_levels = ['Level I', 'Level II', 'Level III']
        if value not in valid_levels:
            raise ValueError(f"Invalid level. Valid levels are: {', '.join(valid_levels)}")
        return value

    # Validation for the 'categories' field to ensure it's a non-empty list
    @validator('categories')
    def categories_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('Categories must not be empty')
        return value

    # Validation for the 'introduction' field to ensure it's not empty
    @validator('introduction')
    def introduction_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Introduction must not be empty')
        return value

    # Validation for the 'learningOutcome' field to ensure it's not empty
    @validator('learningOutcome')
    def learning_outcome_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Learning outcome must not be empty')
        return value

    # Validation for the 'summary' field to ensure it's not empty
    @validator('summary')
    def summary_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Summary must not be empty')
        return value

    # Validation for the 'pdfLink' field to ensure it's not empty
    @validator('pdfLink')
    def pdf_link_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('PDF link must not be empty')
        return value
          
    # You can add more validators here as needed for other fields
if __name__ == '__main__':
    data = {
    "pdfLink": "http://example.com/somefile.pdf",
    "parentTopic": "Science",
    "year": 2023,
    "level": "Level I",
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

    

