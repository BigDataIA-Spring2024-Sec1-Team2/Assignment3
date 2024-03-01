from unittest import TestCase
from models.metadata import MetadataPDF
from pydantic import ValidationError
import pytest


class MetadataPDFTestClass(TestCase):

    def setUp(self):
        self.data = MetadataPDF(name="name", 
                                level="Level I", 
                                year=2023, 
                                total_topics=10,
                                topics=["topic_names"], 
                                total_sub_topics=10, 
                                sub_topics=["sub_topics_names"],
                                content_length=10, 
                                s3_filepath="https://cfa-pdf/cleaned_data/")
    

    def test_positive_correct_metadata_year(self):
        metadataTestData = self.data
        self.assertEqual(metadataTestData.year, 2023)

    def test_positive_incorrect_metadata_year(self):
        metadataTestData = self.data
        self.assertNotEqual(metadataTestData.year, 2021)

    def test_negative_empty_fields(self):
        with self.assertRaises(ValidationError):
            MetadataPDF(name="", 
                        level="", 
                        year=2023, 
                        total_topics=10,
                        topics=["topic_names"], 
                        total_sub_topics=10, 
                        sub_topics=["sub_topics_names"],
                        content_length=10, 
                        s3_filepath="https://cfa-pdf/cleaned_data/")
            
    def test_positive_correct_metadata_int(self):
        metadataTestData = self.data
        self.assertTrue(isinstance(metadataTestData.year, int))
        self.assertTrue(isinstance(metadataTestData.total_topics, int))
        self.assertTrue(isinstance(metadataTestData.total_sub_topics, int))
        self.assertTrue(isinstance(metadataTestData.content_length, int))

    def test_positive_correct_metadata_not_int(self):
        with self.assertRaises(ValidationError):
            MetadataPDF(name="name", 
                        level="Level I", 
                        year="abc", 
                        total_topics="abc",
                        topics=["topic_names"], 
                        total_sub_topics="abc", 
                        sub_topics=["sub_topics_names"],
                        content_length="abc", 
                        s3_filepath="https://cfa-pdf/cleaned_data/")

    
   