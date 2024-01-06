from dotenv import load_dotenv,dotenv_values
import os
from azure.core.credentials import AzureKeyCredential

# Configure environment variables  
load_dotenv()  
service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") 
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME") 
key = os.getenv("AZURE_SEARCH_ADMIN_KEY") 
model = os.getenv("MODEL_NAME")
semantic_config = os.getenv("AZURE_SEARCH_SEMANTIC_CONFIG_NAME")
credential = AzureKeyCredential(key)

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

NUMBER_OF_RESULTS_TO_RETURN = os.getenv("NUMBER_OF_RESULTS_TO_RETURN")
NUMBER_OF_NEAR_NEIGHBORS = os.getenv("NUMBER_OF_NEAR_NEIGHBORS")
