from models.database import create_tables, Session
from scripts.topic import Topic
from scripts.content import Content
from scripts.metadata import Metadata
from scripts.url import URL

# Create tables
create_tables()

# Example usage
session = Session()

# Insert data into 'content' table
content_entry = Content(heading='Sample Heading', topicId=1, content='Sample Content')
session.add(content_entry)
session.commit()

# Query data from 'metadata' table
query_result = session.query(Metadata).all()
for entry in query_result:
    print(f"Author: {entry.author}, File Size: {entry.fileSize}")

session.close()
