import os
import sys
import requests
from dotenv import load_dotenv
from grobid_client.grobid_client import GrobidClient
from bs4 import BeautifulSoup

## config
print("PYTHONPATH = ",sys.path)
print("Current working directory = ",os.getcwd())
print("Adding current working directory to PYTHONPATH")
sys.path.append(os.getcwd())


from models.content_pdf import ContenPDF
from models.topic_pdf import TopicPDF


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

def parse_xml_content(level, xml_file_path):

    print(level[-1])
    title_topic = "Quantitative Methods"
    if level[-1] == 3 : title_topic = "Economics"
    
    topic = TopicPDF(int(level[-1]),title_topic )
    with open(xml_file_path, 'r') as tei:
        soup = BeautifulSoup(tei, 'xml')
        # print(soup)

    # Find all 'div' elements
    divs = soup.find_all('div', {'xmlns': 'http://www.tei-c.org/ns/1.0'})

    content_list = []
    topic_list =[]
    cont = None
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
        if not content:
            # if there no content, then it is a topic
            topic = TopicPDF(level, heading)
            topic_list.append(topic)
            continue
        # add heading and content to the list
        cont = ContenPDF(topic.id, heading, content)
        content_list.append(cont)
        
        # print("Heading:", heading)
        # print("Content:", content)
        # print("---")
    
    return topic_list,content_list


def parse_all_xml():
    # Iterate through all PDF files in the directory
    grobid_output_dir = output_dir+"grobid/"
    for filename in os.listdir(grobid_output_dir):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(grobid_output_dir, filename)
            print("Parsing xml file ",filename, " saved at path ", xml_file_path)
            
            year = filename.split("-")[0]
            level = filename.split("-")[1]

            topic_list,content_list = parse_xml_content(level, xml_file_path)
            print(len(content_list))
            print(len(topic_list))
            pypdf_name = "PyPDF_RR_"+year+"_"+level+"_combined.txt"
            
extract_grobid()
parse_all_xml()           


    










