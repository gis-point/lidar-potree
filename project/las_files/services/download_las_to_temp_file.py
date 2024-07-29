import os
import requests
import uuid

def download_las_file(url, save_directory='downloads/las'):
    # Ensure the save directory exists
    os.makedirs(save_directory, exist_ok=True)
    
    # Generate a UUID for the file name
    file_name = f"{uuid.uuid4()}.las"
    save_path = os.path.join(save_directory, file_name)
    # Stream the file download
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Check if the request was successful
        
        # Write the content to the specified file in chunks
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    
    print(f"File downloaded to: {save_path}")
    return save_path