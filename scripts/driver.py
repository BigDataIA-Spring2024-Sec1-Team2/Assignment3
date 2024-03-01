from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import concurrent.futures
from tqdm import tqdm 

import requests
import time
import csv
import os
import re

from typing import List

import sys
current_directory = os.getcwd()
sys.path.append(current_directory)


from utility import Utility
from models.urlClass import UrlClass
from web_scaping_url_dataset_creation import * 

from web_scaping_url_dataset_creation import loadenv as web_scaping_loadenv
from parse_grobid_xml import perform_grobid_extraction
from snowflake_setup import * 


print("--------------------------- PART 1: WEB SCRAPING CFA WEBSITES ---------------------------")

csv_filename, folderpath, txt_filename =web_scaping_loadenv()
count = 2

file_path = folderpath+txt_filename  # Replace with the actual file path
## Create/overwrite the file to empty it
try:
    # Open the file in write mode ('w') or truncate mode ('w+')
    with open(file_path, 'w+', encoding='utf-8'):
        pass  # The 'pass' statement does nothing, effectively emptying the file

    print(f"The file '{file_path}' has been emptied.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
listUrl = []
while(count>=0):
    url = f"https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#first={count*100}&sort=%40refreadingcurriculumyear%20descending&numberOfResults=100"
    listUrl += scrape_coveo_links(url)
    count = count - 1 

url_objects = process_urls(listUrl)

csv_path = folderpath+csv_filename
delete_csv_if_exists(csv_path)

# write_url_objects_to_csv(url_objects,csv_path)
Utility.store_to_csv(url_objects,folderpath,csv_filename)

## GROBID
print("--------------------------- PART 2: GROBID EXTRACTION ---------------------------")

perform_grobid_extraction()



local_path, s3_bucket_name, s3_folder, access_key, secret_key, region = Utility.envForS3()
print(local_path, s3_bucket_name, s3_folder, access_key, secret_key, region)

print("--------------------------- PART 3: PUSHING CLEANED CSV FILES TO S3 ---------------------------")
# Upload only new text files or overwrite existing ones in the specified S3 folder
Utility.upload_text_files_to_s3_folder(local_path, s3_bucket_name, s3_folder, access_key, secret_key, region)


print("--------------------------- PART 4: CREATING SNOWFLAKE SCHEMA ---------------------------")
print("\n")
print(".............Testing Snnowflake connection")
connectionToSnow(connection_test=False)

print(".............Starting Snnowflake connection")
connection = connectionToSnow()
setup(connection)

db_prod = os.getenv("SNOWFLAKE_DBT_PROD_DB")
db_dev = os.getenv("SNOWFLAKE_DBT_DEV_DB")
topic_table =  os.getenv("SNOWFLAKE_DBT_TOPIC_TABLE")
content_table = os.getenv("SNOWFLAKE_DBT_CONTENT_TABLE")
metadata_table = os.getenv("SNOWFLAKE_DBT_META_TABLE")
urldata_table = os.getenv("SNOWFLAKE_DBT_URLDATA_TABLE")


print(".............Creating Snnowflake Tables")

createtables(connection,db_prod, topic_table, content_table, metadata_table, urldata_table)
createtables(connection,db_dev, topic_table, content_table, metadata_table, urldata_table)

loadtable_s3(connection, db_dev,urldata_table,metadata_table,content_table,topic_table)
loadtable_s3(connection, db_prod,urldata_table,metadata_table,content_table,topic_table)


connection.close()
sys.exit(0)


