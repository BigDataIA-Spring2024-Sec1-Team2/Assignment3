from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Content(Base):
    __tablename__ = 'content'

    contentId = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String)
    topicId = Column(Integer, ForeignKey('topic.topicId'))
    content = Column(String)

    topic = relationship('Topic', back_populates='contents')
