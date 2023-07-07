import json
import os
import re
from datetime import datetime

def get_latest_file(directory):
    files = os.listdir(directory)
    if not files:
        return None

    # Get the latest modified file
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

# Example usage
directory_path = './outputs/final_jsons'
latest_file_path = get_latest_file(directory_path)
if latest_file_path is not None:
    print("Latest file:", latest_file_path)
else:
    print("No files found in the directory.")


# latest_file_path = "F:\MonitizeMax/backend_data_gen\outputs/final_jsons\output_2023-06-12_17-36-06.json"
with open(latest_file_path,'r') as file:
    json_data = json.load(file)

def extract_start_string(input_string):
    # Remove leading numbering or bullet points
    cleaned_string = input_string.strip().lstrip("1234567890.-").strip()

    # Remove leading whitespace and return the title
    return cleaned_string.strip()

for i, article in enumerate(json_data):
    title = article['title'] 
    print(type(title), title)
    clean_title = extract_start_string(title)
    print(clean_title)
    article['title'] = clean_title



output_directory = './outputs/final_cleaned_json'
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file_path = os.path.join(output_directory,f'cleaned_{now}.json')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
with open(output_file_path,'w') as file:
    json.dump(json_data, file, indent=4)
