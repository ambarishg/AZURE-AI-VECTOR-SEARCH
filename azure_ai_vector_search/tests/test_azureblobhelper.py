import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import utilities.azureblob_helper as azureblob_helper
import requests
import io
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

def test_generate_sas_url():
    load_dotenv(override=True)
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")
    blob_name = os.environ.get("AZURE_STORAGE_BLOB_NAME")
    print(f"account_name: {account_name}, account_key: {account_key}, container_name: {container_name}, blob_name: {blob_name}")
    azure_blob_helper = azureblob_helper.AzureBlobHelper(account_name, account_key, container_name)
    sas_url = azure_blob_helper.generate_sas_url(blob_name)
    print(sas_url)
    return sas_url

def read_pdf_sas_url():
    file_path = test_generate_sas_url() 

    # Read the PDF file from the SAS URL
    response = requests.get(file_path)
    with io.BytesIO(response.content) as open_pdf_file:
        reader = PdfReader(open_pdf_file)
        num_pages = len(reader.pages)
        print(num_pages)

        full_doc_text = ""
        pages = reader.pages
        num_pages = len(pages) 
        
        try:
            for page in range(num_pages):
                current_page = reader.pages[page]
                text = current_page.extract_text()
                full_doc_text += text
        except:
            print("Error reading file")
        finally:
            print(full_doc_text)

test_generate_sas_url()
print("Reading PDF from SAS URL...  ")
read_pdf_sas_url()