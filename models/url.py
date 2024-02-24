from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = 'url'

    pdfLink = Column(String, primary_key=True)
    parentTopic = Column(String)
    year = Column(Integer)
    level = Column(Integer)
    introduction = Column(String)
    learningOutcome = Column(String)
    summary = Column(String)
    categories = Column(String)
    topicName = Column(String)
    url = Column(String)
