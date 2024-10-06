import os
from azure.storage.blob import BlobServiceClient

# Your Azure connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=imagenessatelitales;AccountKey=kajhTlmzPZ5QXJo/diEKLy9jvwZX2/Yb2ZGYKif3D3Wj05BoRCV6R5OA6B3R2NWVZ+pDal+zuu8J+ASteap8IA==;EndpointSuffix=core.windows.net"
container_name = "blob"
file_name = "tres_de_febrero.kml"

# Get the directory where storage.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the "data" folder if it doesn't exist
data_folder = os.path.join(current_dir, "data")
os.makedirs(data_folder, exist_ok=True)

# Set the download path to the "data" folder
download_path = os.path.join(data_folder, file_name)

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def download_blob_from_azure(file_name, download_path):
    # Get the blob client for the specific file
    blob_client = container_client.get_blob_client(file_name)
    
    # Download the blob to a local file
    with open(download_path, "wb") as file:
        file.write(blob_client.download_blob().readall())
    
    print(f"Downloaded '{file_name}' to '{download_path}'")

# Download the file
download_blob_from_azure(file_name, download_path)
