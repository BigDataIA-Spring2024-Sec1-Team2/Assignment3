from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

load_dotenv('../config/.env', override=True)

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
        from scripts.topic import Base as TopicBase
        from scripts.content import Base as ContentBase
        from scripts.metadata import Base as MetadataBase
        from scripts.url import Base as URLBase

        TopicBase.metadata.create_all(self.engine)
        ContentBase.metadata.create_all(self.engine)
        MetadataBase.metadata.create_all(self.engine)
        URLBase.metadata.create_all(self.engine)

    def create_warehouse(self, warehouse_name, warehouse_size='X-SMALL',
                         auto_suspend=180, auto_resume=True, initially_suspended=True):
        create_warehouse_query = f"""CREATE OR REPLACE WAREHOUSE {warehouse_name} WITH
           WAREHOUSE_SIZE='{warehouse_size}'
           AUTO_SUSPEND = {auto_suspend}
           AUTO_RESUME = {str(auto_resume).upper()}
           INITIALLY_SUSPENDED={str(initially_suspended).upper()};
           """
        self.execute_query(create_warehouse_query)

    def create_database(self, database_name):
        drop_database_query = f'DROP DATABASE IF EXISTS {database_name};'
        create_database_query = f'CREATE OR REPLACE DATABASE {database_name};'

        self.execute_query(drop_database_query)
        self.execute_query(create_database_query)

    def create_stage(self, stage_name, enable=True):
        create_stage_query = f'CREATE OR REPLACE STAGE {stage_name} DIRECTORY = (ENABLE = {str(enable).upper()});'
        self.execute_query(create_stage_query)

    def upload_to_stage(self, stage_name, local_directory, file_pattern='*.csv'):
        upload_to_stage_query = f"PUT file://{local_directory}/{file_pattern} @.{stage_name};"
        self.execute_query(upload_to_stage_query)

    def copy_stage_to_table(self, table_name, stage_name, file_pattern, field_optionally_enclosed_by='"'):
        copy_stage_to_table_query = f"""COPY INTO {table_name}
          FROM @.{stage_name}
          FILE_FORMAT = (type = csv field_optionally_enclosed_by='{field_optionally_enclosed_by}')
          PATTERN = '{file_pattern}'
          ON_ERROR = 'skip_file';"""
        self.execute_query(copy_stage_to_table_query)

    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                connection.execute(query)
        except OperationalError as e:
            print(f"Error executing query: {e}")

    def write_data_to_tables(self, local_directory, stage_name='your_external_stage_name'):
        # Assuming your CSV files in local_directory follow a certain pattern
        file_pattern = 'FinanceHub.csv.gz'

        # Create external stage
        self.create_stage(stage_name)

        # Upload data to external stage
        self.upload_to_stage(stage_name, local_directory, file_pattern)

        # Copy data from stage to tables
        self.copy_stage_to_table('CFA_WEB_DATA_R', stage_name, file_pattern)
        # Add similar lines for other tables if needed

# Example usage:

snowflake_db = SnowflakeDatabase(
    snowflake_account='your_snowflake_account',
    snowflake_user='your_snowflake_user',
    snowflake_password='your_snowflake_password',
    snowflake_database='your_snowflake_database',
    snowflake_warehouse='your_snowflake_warehouse',
    snowflake_schema='your_snowflake_schema'
)

# Create warehouse and database
snowflake_db.create_warehouse('your_warehouse_name')
snowflake_db.create_database('your_database_name')

# Create tables
snowflake_db.create_tables()

# Write data to tables using S3 external stage
snowflake_db.write_data_to_tables(local_directory='/path/to/local/directory', stage_name='your_external_stage_name')
