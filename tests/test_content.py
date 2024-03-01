from unittest import TestCase
from models.content_pdf import ContenPDF
from pydantic import ValidationError
import pytest


class ContenPDFTestClass(TestCase):

    def setUp(self):
        self.data = ContenPDF(topic_id=1, heading="heading", content="content")
    

    def test_positive_correct_topic_id(self):
        objTestData = self.data
        self.assertEqual(objTestData.topic_id, 1)

    def test_positive_incorrect_topic_id(self):
        objTestData = self.data
        self.assertNotEqual(objTestData.topic_id, 2)

    def test_negative_correct_topic_id(self):
        with self.assertRaises(ValidationError):
            ContenPDF(topic_id=0, heading="heading", content="content")

    def test_negative_empty_fields(self):
        with self.assertRaises(ValidationError):
            ContenPDF(topic_id="", heading="", content="")
            
    def test_positive_correct_int(self):
        metadataTestData = self.data
        self.assertTrue(isinstance(metadataTestData.topic_id, int))

    

    
   