import os
import snowflake.connector
from typing import List
from dotenv import load_dotenv
import csv

class Utility:

    def __init__(self) -> None:
        # read env file and set all variables
        # Example: Assuming you have environment variables in a file named '.env'
        # You can use python-dotenv to load them.
        load_dotenv()

        self.snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.snowflake_user = os.getenv('SNOWFLAKE_USER')
        self.snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
        self.snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
        self.snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')
    
    def setup_snowflake(self):
        # create snowflake data warehouse
        connection = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account,
            warehouse='YOUR_WAREHOUSE',
            database=self.snowflake_database,
            schema=self.snowflake_schema
        )

        try:
            cursor = connection.cursor()

            # create topic table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topic (
                    topicId INT AUTOINCREMENT PRIMARY KEY,
                    topicName STRING,
                    pdfId INT
                )
            """)

            # create content table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content (
                    contentId INT AUTOINCREMENT PRIMARY KEY,
                    heading STRING,
                    topicId INT,
                    content STRING
                )
            """)

            # create metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    pdfId INT AUTOINCREMENT PRIMARY KEY,
                    author STRING,
                    lang STRING,
                    s3FilePath STRING,
                    fileSize INT
                )
            """)

            # create URL table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS url (
                    pdfLink STRING,
                    parentTopic STRING,
                    year INT,
                    level INT,
                    introduction STRING,
                    learningOutcome STRING,
                    summary STRING,
                    categories STRING,
                    topicName STRING,
                    url STRING
                )
            """)
        finally:
            connection.close()

    def s3_write(self):
        # Implementation to write to S3
        pass

    @staticmethod
    def store_to_csv(object_list, file_dir, file_name):
    # Ensure the list is not empty
        if object_list:
            # Get attribute names from the first object
            fieldnames = list(vars(object_list[0]).keys())
            # fieldnames = [field.name for field in fields(Person)]

            # Check if the directory exists, create it if not
            if not os.path.exists(file_dir):
                print("Creating directory to store csv")
                os.makedirs(file_dir)

            csv_file_path = os.path.join(file_dir, file_name)

            with open(csv_file_path, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for object in object_list:
                    if object:
                        writer.writerow({field: getattr(object, field) for field in fieldnames})

            print(f'Data has been written to {csv_file_path}.')
        else:
            print("List is empty, nothing to write to CSV.")



    def s3_read(self):
        # Implementation to read from S3
        pass

    def snowflake_write(self, data: List[dict]):
        connection = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account,
            warehouse='YOUR_WAREHOUSE',
            database=self.snowflake_database,
            schema=self.snowflake_schema
        )

        try:
            cursor = connection.cursor()

            # Example: Inserting data into the 'metadata' table
            for row in data:
                cursor.execute("""
                    INSERT INTO metadata (author, lang, s3FilePath, fileSize)
                    VALUES (%s, %s, %s, %s)
                """, (row['author'], row['lang'], row['s3FilePath'], row['fileSize']))

            connection.commit()

        finally:
            connection.close()

    def snowflake_read(self):
        # Implementation to read from Snowflake
        pass

# Example usage:
if __name__ == "__main__":
    utility = Utility()
    utility.setup_snowflake()

    # Example data to write to Snowflake
    data_to_write = [
        {'author': 'John Doe', 'lang': 'English', 's3FilePath': 's3://your-bucket/file.pdf', 'fileSize': 1024},
        {'author': 'Jane Smith', 'lang': 'Spanish', 's3FilePath': 's3://your-bucket/file2.pdf', 'fileSize': 2048}
    ]

    utility.snowflake_write(data_to_write)
