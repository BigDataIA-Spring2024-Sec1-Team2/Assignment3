from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scripts.topic import Base as TopicBase
from scripts.content import Base as ContentBase
from scripts.metadata import Base as MetadataBase
from scripts.url import Base as URLBase

class SnowflakeDatabase:
    def __init__(self, snowflake_account, snowflake_user, snowflake_password,
                 snowflake_database, snowflake_warehouse, snowflake_schema):
        self.snowflake_account = snowflake_account
        self.snowflake_user = snowflake_user
        self.snowflake_password = snowflake_password
        self.snowflake_database = snowflake_database
        self.snowflake_warehouse = snowflake_warehouse
        self.snowflake_schema = snowflake_schema

        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def create_engine(self):
        connection_string = (
            f'snowflake://{self.snowflake_user}:{self.snowflake_password}@'
            f'{self.snowflake_account}/{self.snowflake_database}?'
            f'warehouse={self.snowflake_warehouse}&schema={self.snowflake_schema}'
        )
        return create_engine(connection_string, echo=True)

    def create_tables(self):
        TopicBase.metadata.create_all(self.engine)
        ContentBase.metadata.create_all(self.engine)
        MetadataBase.metadata.create_all(self.engine)
        URLBase.metadata.create_all(self.engine)

    def connection_to_snow(self, connection_test=False):
        try:
            connection = self.engine.connect()
            results = connection.execute('select current_version()').fetchone()
            print(results[0])
            if connection_test:
                connection.close()
            else:
                return connection
        except Exception as e:
            print("Error connecting to Snowflake:", e)
            return None

    def create_database(self):
        create_database_query = f"CREATE OR REPLACE DATABASE {self.snowflake_database};"
        with self.engine.connect() as connection:
            connection.execute(create_database_query)

    def create_warehouse(self):
        create_warehouse_query = f"""CREATE OR REPLACE WAREHOUSE {self.snowflake_warehouse} WITH
           WAREHOUSE_SIZE='X-SMALL'
           AUTO_SUSPEND = 180
           AUTO_RESUME = TRUE
           INITIALLY_SUSPENDED=TRUE;
        """
        with self.engine.connect() as connection:
            connection.execute(create_warehouse_query)

    def drop_database(self):
        drop_database_query = f"DROP DATABASE IF EXISTS {self.snowflake_database};"
        with self.engine.connect() as connection:
            connection.execute(drop_database_query)

# Example usage:

snowflake_db = SnowflakeDatabase(
    snowflake_account='your_snowflake_account',
    snowflake_user='your_snowflake_user',
    snowflake_password='your_snowflake_password',
    snowflake_database='your_snowflake_database',
    snowflake_warehouse='your_snowflake_warehouse',
    snowflake_schema='your_snowflake_schema'
)

# Drop the existing database if it exists
snowflake_db.drop_database()

# Create the database
snowflake_db.create_database()

# Create the warehouse
snowflake_db.create_warehouse()

# Create tables
snowflake_db.create_tables()

# Establish a connection
snowflake_connection = snowflake_db.connection_to_snow()
