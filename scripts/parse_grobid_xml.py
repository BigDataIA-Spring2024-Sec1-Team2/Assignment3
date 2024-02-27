import os
import sys
import requests
from dotenv import load_dotenv
from grobid_client.grobid_client import GrobidClient
from bs4 import BeautifulSoup
from pydantic import TypeAdapter, ValidationError
import csv
import json
import dataclasses

## config
print("PYTHONPATH = ",sys.path)
print("Current working directory = ",os.getcwd())
print("Adding current working directory to PYTHONPATH")
sys.path.append(os.getcwd())


from models.content_pdf import ContenPDF
from models.topic_pdf import TopicPDF
from models.metadata import MetadataPDF
from utility_s3 import download_files_from_s3


load_dotenv('.env',override=True)

def load_env():
    grobid_url = os.getenv("GROBID_URL")
    pdf_directory = os.getenv("PDF_DIR_PATH") # Store the downloaded PDF files from S3
    output_dir = os.getenv("OUTPUT_DIR_PATH") # Store the extracted txt files
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    region = os.getenv("S3_REGION")
    
    return grobid_url, pdf_directory, output_dir, s3_bucket_name, access_key, secret_key, region

# load env
grobid_url, pdf_directory, output_dir, s3_bucket_name, access_key, secret_key, region = load_env() 

def extract_grobid():
    print("Changing current working directory to:")
    os.chdir("grobid_client_python")
    print(os.getcwd())
    output_path = f'../{output_dir}/grobid'
    try:
        client = GrobidClient(config_path="./config.json")
        client.process("processFulltextDocument", "../data",
                    output=output_path, consolidate_citations=True, tei_coordinates=True, force=True)
        print("Done")
        
    except Exception as e:
        print("Failed to extract pdf using grobid with error:")
        print(str(e))
    finally:
        os.chdir("../")
        print("Changing current working directory back to:")
        print(os.getcwd())

def dump_to_s3():
    pass

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
                writer.writerow({field: getattr(object, field) for field in fieldnames})

        print(f'Data has been written to {csv_file_path}.')
    else:
        print("List is empty, nothing to write to CSV.")


def parse_xml_content(level, xml_file_path):

    content_list = []
    topic_list =[]
    cont = None

    print(level[-1])
    title_topic = "Quantitative Methods"
    if level[-1] == 3 : title_topic = "Economics"
    
    topic = TopicPDF(level=level,topic=title_topic )
    topic_model = TypeAdapter(TopicPDF).validate_python(topic)
    topic_list.append(topic_model)

    with open(xml_file_path, 'r') as tei:
        soup = BeautifulSoup(tei, 'xml')
        # print(soup)
    if not soup:
        print("Some error occurred")
        return
    # Calculate the length of the content excluding tags
    content_length = len(soup.get_text())

    # Find all 'div' elements
    divs = soup.find_all('div', {'xmlns': 'http://www.tei-c.org/ns/1.0'})

    
    # Iterate through each 'div' element
    for div in divs:
        if div.head is None:
            # append it to previous content
            if cont:
                cont.content += div.text
            else:
                print("Skipping this content : ")
                print(div.text)
            continue 
        # Extract the heading from 'head' element
        heading = div.head.text
        if heading == "LEARNING OUTCOMES":
            #skip as there is no content
            continue
        
        # Extract content from 'p' elements
        content = ' '.join(p.text for p in div.find_all('p'))
        try:
            if not content:
                # if there no content, then it is a topic
                topic = TopicPDF(level=level, topic=heading)

                topic_model = TypeAdapter(TopicPDF).validate_python(topic)
                topic_list.append(topic_model)
                continue
            # add heading and content to the list
            cont = ContenPDF(topic_id=topic.id, heading=heading, content=content)
            # validating the dataclass 
            content_model = TypeAdapter(ContenPDF).validate_python(cont)
            content_list.append(content_model)
        except ValidationError as e:
            print(e)
            print("Skipping this content : ")
            print(div.text)
            continue
    
    return topic_list, content_list, content_length


def parse_all_xml():
    # Iterate through all PDF files in the directory
    grobid_output_dir = output_dir+"grobid/"
    topic_list,content_list = [], []
    metadata_list = []
    for filename in os.listdir(grobid_output_dir):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(grobid_output_dir, filename)
            print("Parsing xml file ",filename, " saved at path ", xml_file_path)
            
            year = filename.split("-")[0]
            level = filename.split("-")[1]

            topics, contents, content_length = parse_xml_content(level, xml_file_path)
            # metadata
            pdf_id = level[-1]
            # 2024-l1-topics-combined-2.grobid.tei.xml
            name = filename.split(".")[0]
            total_topics = len(topics)
            total_sub_topics = len(contents)
            
            topic_names = [top.topic for top in topics]
            sub_topics_names = [st.heading for st in contents]
            metadata = MetadataPDF(pdf_id=pdf_id, name=name, level=level, year=year, total_topics=total_topics,
                                   topics=topic_names, total_sub_topics=total_sub_topics, 
                                   sub_topics=sub_topics_names,
                                   content_length=content_length, s3_filepath="s3://cfa-pdf/cleaned_data/")
            
            metadata_list.append(metadata)
            topic_list.append(topics)
            content_list.append(contents)
            print(len(content_list))
            print(len(topic_list))
    return metadata_list, topic_list, content_list


def prase_grobid_driver(): 
    
    # if not os.path.exists("data/"):
    #     print("Creating directory to store raw pdfs")
    #     os.makedirs("data/")
    # download the pdf files from s3
    # download_files_from_s3("data/", "raw-pdfs")
    # extract grobid xml from PDF
    extract_grobid()
    # parse the xmls and validate objs using pydantic
    metadata_list,topic_list,content_list = parse_all_xml()
    # store the objects to csv
    csv_output_dir = f'{output_dir}cleaned_csv/'
    store_to_csv(metadata_list, csv_output_dir, "MetadataPDF.csv")

    # flatten the lists before storing it to csv
    topic_flattened = [topic for row in topic_list for topic in row]
    store_to_csv(topic_flattened, csv_output_dir, "TopicPDF.csv")

    content_flattened = [content for row in content_list for content in row]
    store_to_csv(content_flattened, csv_output_dir, "ContentPDF.csv")


prase_grobid_driver()         


    










