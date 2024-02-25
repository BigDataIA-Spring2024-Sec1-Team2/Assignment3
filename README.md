## Big Data Systems and Intelligence Analytics (DAMG 7245)

| Name         | Email                        | NUID    |
| ------------ | ---------------------------- | ------- |
| Ameya Apte   | apte.ame@northeastern.edu    | 2764540 |
| Sayali Dalvi | dalvi.sa@northeastern.edu    | 2799803 |
| Soeb Hussain | hussain.soe@northeastern.edu | 2747200 |

# Assignment 3

# Finance Professional Development Resource Database

Big Data Systems and Intelligence Analytics (DAMG 7245) 

## Overview

This project aims to aggregate and make accessible finance professional development materials through a comprehensive data engineering solution. It involves creating datasets from materials listed on the CFA Institute’s website, structuring the data, extracting text from PDF files, and integrating cloud storage solutions.

## Live application Links

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1_g3QZtY-Eae-6uYk91tGWhSfqPiM0bwwxelIrHwFKZY#0)

## Problem Statement

Part 1:

In this segment, we will design 2 Python classes

URLClass to represent the schema for the Assignment 2(Part 1) CFA webpages (224 pages). Each webpage needs to adhere to guidelines you define as a part of the URLClass
Two PDFClasses to represent the schema for the Grobid output.
MetaDataPDFClass : Stores metadata for the three PDF files
ContentPDFClass: Stores the extracted content from each PDF file
Notes:

Use the provided schema for Part 1 and create schemas for Part 2. For Part 2 (PDFClass), start with creating the Snowflake schema and discuss the intuition of why you created the schema in the first place and what applications could use your schema.
You are expected to do data and schema validation using these objects using Pydantic 2 (See the tutorials and attend the TA lab )and create “clean” csv files
Build 5+5 test cases using Pytest for each of the three classes to show how your validation would succeed/fail (5 pass and 5 fail)
You can use the Grobid data loader and Url data loader classes as starter code or the second example on Grobid Data classes to start with.
Part 2 using DBT.

Your team is reviewing the architecture of Part 1 and think using DBT with Snowflake to run transformation workflows.

Review https://docs.getdbt.com/docs/introductionLinks to an external site. to understand  DBT

Your plan is to redo the tutorial: https://docs.getdbt.com/guides/snowflake?step=7Links to an external site. but with the “clean csv” created in Part 1

Requirements

Load the clean data into Snowflake
You intend to create a summary table with the following schema using DBT.
Level, Topic, Year, Number of articles, Min Length (Summary), Max Length (Summary), Min Length (Learning outcomes), Max Length (Learning outcomes)
You are free to build a model in anyway you want
Materialize it to a new table
Write tests to validate the new columns
Document your model
Commit and Deploy the model
Note: Review https://docs.getdbt.com/docs/dbt-cloud-environmentsLinks to an external site. for deployment
Create a Test and Production Environment. (Note: Your Snowflake should also have a corresponding Test and Production db/tables.
What considerations would you have for a test and Production environment? 

## Features

- **Data Extraction**: Utilizes web scraping to gather finance-related materials.
- **Data Structuring**: Organizes scraped data into a coherent structure suitable for database integration.
- **Text Extraction**: Implements algorithms to extract text from PDF documents.
- **Cloud Integration**: Utilizes AWS S3 for storage and Snowflake for database management.

## Architecture Diagram

![Architecture Diagram](image.png)

## Technologies Used

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Beautiful Soup](https://img.shields.io/badge/beautiful_soup-109989?style=for-the-badge&logo=beautiful_soup&logoColor=white)](https://pypi.org/project/beautifulsoup4/)
[![Selenium](https://img.shields.io/badge/Selenium-39e75f?style=for-the-badge&logo=selenium&logoColor=blue)](https://www.selenium.dev/)
[![Grobid](https://img.shields.io/badge/grobid-909090?style=for-the-badge&logo=grobid&logoColor=blue)](https://grobid.readthedocs.io/en/latest/Introduction/)
[![PyPDF2](https://img.shields.io/badge/PyPDF2-123499?style=for-the-badge&logo=python&logoColor=blue)](https://pypi.org/project/PyPDF2/)
[![Snowflake](https://img.shields.io/badge/Snowflake-90e0ef?style=for-the-badge&logo=snowflake&logoColor=blue)](https://www.snowflake.com/en/)
[![Amazon S3](https://img.shields.io/badge/Amazon_S3-FF4B4B?style=for-the-badge&logo=Amazon_S3&logoColor=white)](https://aws.amazon.com/s3/)

- Python for scripting and web scraping
- Jupyter Notebook for data analysis and visualization
- Snowflake for data storage and management
- AWS S3 for cloud-based file storage

## Data Sources

- [S3 Bucket](https://cfa-pdfs.s3.us-east-2.amazonaws.com/)
- [Finance Website](https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending)

## Pre requisites

No specific prerequisites are required. Only installation of required packages needs to be done

## Project Structure

```
📦 Assignment3

```

_You can generate the project tree using following tools_
_[Project Tree Generator](https://woochanleee.github.io/project-tree-generator)_
_[Generate from terminal](https://www.geeksforgeeks.org/tree-command-unixlinux/)_

## How to run Application locally

### Setup and Installation

1. Clone the repository to your local machine.
2. Install the required Python libraries using `pip install -r requirements.txt`.
3. Configure AWS S3 and Snowflake with the provided setup guide.
4. Install selenium webdriver for edge browser - Download the edge webdriver file and set the Path in environment variables

Naming Conventions:

- s3 bucketname: CFA-PDFs
- snowflake DB: DAMG_7245_CFA
- snowflake warehouse: DAMG_7245_CFA
- Tables:
  - metadata: CFA_META_R
  - web scraped data: CFA_WEB_DATA_R

Execution Step for code/CSV2Snowflake.ipynb

- create a folder in parent directory with name 'config'
- add .env file in it containing following variables

```SNOWFLAKE_USER=''
SNOWFLAKE_PASSWORD=''
SNOWFLAKE_DATABASE='DAMG_7245_CFA_DB'
SNOWFLAKE_WAREHOUSE='DAMG_7245_WH_XS'
SNOWFLAKE_ACCOUNT_IDENTIFIER=''

GROBID_URL='http://localhost:8070/api/processFulltextDocument'
PDF_DIR_PATH='../data'
OUTPUT_DIR_PATH='../sample_output/'

S3_BUCKET_NAME = 'cfa-pdfs'
S3_PYPDF_FOLDER_NAME = 'pypdf'
S3_GROBID_FOLDER_NAME = 'grobid'
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
S3_REGION=''
S3_META_BUCKET = 'cfa-pdfs'
S3_META_ACCESS_KEY = ''
S3_META_SECRET_KEY = ''
```

## References

- [S3 Documentation](https://docs.aws.amazon.com/s3/?icmpid=docs_homepage_featuredsvcs)
- [Snowflake Documentation](https://docs.snowflake.com/en/)
- [Grobid Documentation](https://grobid.readthedocs.io/en/latest/Introduction/)
- [CFA Institute's Website](https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending)
