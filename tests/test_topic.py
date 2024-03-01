from unittest import TestCase
from models.topic_pdf import TopicPDF
from pydantic import ValidationError
import pytest


class TopicPDFTestClass(TestCase):

    def setUp(self):
        self.data = TopicPDF(level="Level I", topic="heading")
    

    def test_positive_correct_id_int(self):
        objTestData = self.data
        self.assertTrue(isinstance(objTestData.id, int))

    def test_positive_incorrect_id(self):
        objTestData = self.data
        self.assertNotEqual(objTestData.id, 0)

    def test_negative_incorrect_str(self):
        with self.assertRaises(ValidationError):
            TopicPDF(level=1, topic="heading")

    def test_negative_empty_fields(self):
        with self.assertRaises(ValidationError):
            TopicPDF(level="", topic="")
            
    def test_negative_incorrect_level_len(self):
        with self.assertRaises(ValidationError):
            TopicPDF(level="l1", topic="Topic")

    

    
   