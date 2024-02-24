# project_directory/topic.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topic'

    topicId = Column(Integer, primary_key=True, autoincrement=True)
    topicName = Column(String)
    pdfId = Column(Integer, ForeignKey('metadata.pdfId'))

    metadata = relationship('Metadata', back_populates='topics')
