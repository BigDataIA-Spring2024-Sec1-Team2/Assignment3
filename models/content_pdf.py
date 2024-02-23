import itertools

class ContenPDF:
    id_generator = itertools.count(1)

    def __init__(self, topic_id: int, heading: str, content: str):
        self.id = next(self.id_generator)
        self.topic_id = topic_id
        self.heading = heading
        self.content = content

    def __str__(self):
        return f"ID: {self.id}\nTopic_id: {self.topic_id}\nHeading: {self.heading}\nContent: {self.content}\n---"

