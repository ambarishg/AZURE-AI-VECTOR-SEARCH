from azure.storage.blob import BlobServiceClient, \
BlobClient, ContainerClient, generate_blob_sas,\
BlobSasPermissions

from datetime import datetime, timedelta

class AzureBlobHelper:
    def __init__(self,
                 account_name,
                 account_key,
                 container_name):
        self.container_name = container_name
        self.account_name = account_name
        self.account_key = account_key
    
    # code to list blobs in a container
    def list_blob(self):
        blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net/",
                                               credential=self.account_key)
        container_client = blob_service_client.get_container_client(self.container_name)
        blob_list = container_client.list_blobs()
        return [blob.name for blob in blob_list]


    # code to generate SAS URL for a blob
    def generate_sas_url(self,blob_name):
        if not blob_name.lower().endswith('.pdf'):
            return None

        sas_blob = generate_blob_sas(account_name=self.account_name,
                                    container_name=self.container_name,
                                    blob_name=blob_name,
                                    account_key=self.account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=2))  # Token valid for 2 hour
        return f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}?{sas_blob}"
    
    def check_pdf(self,filename):
        filename = filename.lower()
        if filename.endswith(".pdf"):
            return True
        else:
            return False
        
    def upload_blob(self, data, blob_name):
        blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net/",
                                               credential=self.account_key)
        container_client = blob_service_client.get_container_client(self.container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        return blob_name        
    
           