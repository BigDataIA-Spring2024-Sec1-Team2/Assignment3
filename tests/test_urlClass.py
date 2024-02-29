from unittest import TestCase
from pydantic import ValidationError
import sys
import os

current_directory = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(current_directory)
sys.path.append(current_directory)


from models.urlClass import UrlClass

from unittest import TestCase
from pydantic import ValidationError
from models.urlClass import UrlClass

class TestUrlClass(TestCase):

    def setUp(self):
        self.data = {
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

    def test_positive_correct_url_year(self):
        urlTestData = UrlClass(**self.data)
        self.assertEqual(urlTestData.year, 2023)

    def test_positive_incorrect_url_year(self):
        urlTestData = UrlClass(**self.data)
        self.assertNotEqual(urlTestData.year, 2021)

    def test_positive_not_empty_fields(self):
        urlTestData = UrlClass(**self.data)
        self.assertTrue(urlTestData.introduction and urlTestData.learningOutcome and urlTestData.summary)

    def test_positive_valid_pdf_link(self):
        urlTestData = UrlClass(**self.data)
        self.assertTrue(urlTestData.pdfLink.startswith("http:"))

    def test_positive_valid_categories(self):
        urlTestData = UrlClass(**self.data)
        self.assertTrue(all(isinstance(cat, str) for cat in urlTestData.categories))

    def test_negative_empty_fields(self):
        self.data["introduction"] = ""  # Empty introduction
        with self.assertRaises(ValidationError):
            UrlClass(**self.data)

    def test_negative_invalid_pdf_link(self):
        self.data["pdfLink"] = ""  # Empty PDF link
        with self.assertRaises(ValidationError):
            UrlClass(**self.data)

    def test_negative_invalid_categories(self):
        self.data["categories"] = "Education"  # Invalid type: str instead of List[str]
        with self.assertRaises(ValidationError):
            UrlClass(**self.data)

    def test_negative_invalid_year(self):
        self.data["year"] = 1800  # Invalid year
        with self.assertRaises(ValidationError):
            UrlClass(**self.data)
    def test_negative_invalid_url(self):
    # Test with an invalid URL format for pdfLink
        self.data["pdfLink"] =  "invalid_url_format"
        with self.assertRaises(ValidationError):
            UrlClass(**self.data)
