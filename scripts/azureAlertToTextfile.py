import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Validate the request content type
    if not req.headers.get("Content-Type") == "application/json":
        return func.HttpResponse("Invalid content type", status_code=400)
    
    try:
        # Parse the request body as JSON
        alert_data = req.get_json()
        
        # Connect to Azure Storage
        storage_connection_string = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        
        # Define the container and blob names
        container_name = "alerts"
        blob_name = "alert.json"
        
        # Get or create the container
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()

        # Create or update the JSON blob with the alert data
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(alert_data), overwrite=True)
        
        return func.HttpResponse("Alert data saved successfully.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
