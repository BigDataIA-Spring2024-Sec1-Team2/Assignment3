import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine
class Config:
    def __init__(self,pathConfig = '../config/.env') -> None:
        # read env file and set all variables
        # Example: Assuming you have environment variables in a file named '.env'
        # You can use python-dotenv to load them.
        load_dotenv('../config/.env',override=True)

        self.snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.snowflake_user = os.getenv('SNOWFLAKE_USER')
        self.snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
        self.snowflake_database = os.getenv('SNOWFLAKE_DATABASE')
        self.snowflake_schema = os.getenv('SNOWFLAKE_SCHEMA')


    def connectionToSnow(self,path='../config/.env',connection_test=True):
        engine = create_engine(
            'snowflake://{user}:{password}@{account_identifier}/'.format(
                user=self.snowflake_user,
                password=self.snowflake_password,
                account_identifier=self.snowflake_account,
            )
        )
        try:
            connection = engine.connect()
            results = connection.execute('select current_version()').fetchone()
            print(results[0])
            if connection_test:
                connection.close()
            else:
                return connection
        except Exception as e:
            print("error in connectionToSnow  -->",e)
        finally:
            engine.dispose()
        

# Example usage:
if __name__ == "__main__":
    utility = Config()
    utility.connectionToSnow()
