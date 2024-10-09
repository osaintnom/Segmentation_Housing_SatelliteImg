import os
from azure.storage.blob import BlobServiceClient
from tqdm import tqdm

# Tu conexión de Azure
connection_string = "DefaultEndpointsProtocol=https;AccountName=imagenessatelitales;AccountKey=kajhTlmzPZ5QXJo/diEKLy9jvwZX2/Yb2ZGYKif3D3Wj05BoRCV6R5OA6B3R2NWVZ+pDal+zuu8J+ASteap8IA==;EndpointSuffix=core.windows.net"
container_name = "blob"

# Inicializa el BlobServiceClient fuera de las funciones para no hacerlo repetidas veces
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def download_blob_from_azure(file_name, output_dir):
    """
    Descarga un archivo desde Azure Blob Storage a un directorio especificado.

    :param file_name: Nombre del archivo a descargar.
    :param output_dir: Directorio donde se descargará el archivo.
    """
    # Crea la carpeta de destino si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Ruta completa del archivo de descarga
    download_path = os.path.join(output_dir, file_name)

    # Obtener el blob client para el archivo específico
    blob_client = container_client.get_blob_client(file_name)

    # Obtener el tamaño del blob
    blob_properties = blob_client.get_blob_properties()
    total_size = blob_properties.size

    # Descargar el blob con una barra de progreso
    with open(download_path, "wb") as file, tqdm(
        total=total_size, unit='B', unit_scale=True, desc=file_name, ascii=True
    ) as pbar:
        stream = blob_client.download_blob()
        for chunk in stream.chunks():
            file.write(chunk)
            pbar.update(len(chunk))
    
    print(f"Downloaded '{file_name}' to '{download_path}'")
    return download_path

if __name__ == "__main__":
    # Archivo a descargar
    file_name = "train;img;Tresdefebrero_GE.tif"

    # Obtener el directorio donde está ubicado este script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Definir el directorio de salida (puedes cambiarlo si deseas otro)
    output_dir = os.path.join(current_dir, "data")

    print("Downloading file from Azure Blob Storage...")
    
    # Descargar el archivo
    download_blob_from_azure(file_name, output_dir)
    print("Download complete!")
