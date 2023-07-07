import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import os

# Replace this path with the path to your Service Account Key JSON file
service_account_key_file = '/Users/sudhirsundrani/Downloads/custom-defender-377912-firebase-adminsdk-d5npo-2bbaa143de.json'

# Initialize the Firebase app if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_key_file)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://custom-defender-377912-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace 'your-project-id' with your actual Firebase project ID
    })

def upload_json_files(directory):
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                language = file_name.split('.')[0].capitalize()  # Capitalize the language name
                push_data(language, data)
                print(f"Data uploaded for language: {language}")

def push_data(language, data):
    ref = db.reference(f'/posts/{language}')
    ref.push(data)

directory_path = './outputs/translated'
upload_json_files(directory_path)

print("Data uploaded successfully")
