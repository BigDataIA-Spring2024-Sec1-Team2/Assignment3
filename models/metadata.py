from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Metadata(Base):
    __tablename__ = 'metadata'

    pdfId = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    lang = Column(String)
    s3FilePath = Column(String)
    fileSize = Column(Integer)
