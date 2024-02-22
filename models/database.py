from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_directory.topic import Base as TopicBase
from project_directory.content import Base as ContentBase
from project_directory.metadata import Base as MetadataBase
from project_directory.url import Base as URLBase

SNOWFLAKE_ACCOUNT = 'your_snowflake_account'
SNOWFLAKE_USER = 'your_snowflake_user'
SNOWFLAKE_PASSWORD = 'your_snowflake_password'
SNOWFLAKE_DATABASE = 'your_snowflake_database'
SNOWFLAKE_WAREHOUSE = 'your_snowflake_warehouse'
SNOWFLAKE_SCHEMA = 'your_snowflake_schema'

engine = create_engine(
    f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}?warehouse={SNOWFLAKE_WAREHOUSE}&schema={SNOWFLAKE_SCHEMA}',
    echo=True
)

def create_tables():
    TopicBase.metadata.create_all(engine)
    ContentBase.metadata.create_all(engine)
    MetadataBase.metadata.create_all(engine)
    URLBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
