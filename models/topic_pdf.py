import itertools

class TopicPDF:
    id_generator = itertools.count(1)

    def __init__(self, pdf_id: int, topic: str):
        self.id = next(self.id_generator)
        self.pdf_id = pdf_id
        self.topic = topic

    def __str__(self):
        return f"ID: {self.id}\nTopic: {self.topic}\PDF id: {self.pdf_id}\n---"

