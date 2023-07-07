
from googletrans import Translator
from google.cloud import translate_v2 as translate
import json
import os
import time
from datetime import datetime
import shutil

def translate_json(input_json):
    languages = {
        'Hindi': 'hi',
        'Malayalam': 'ml',
        'Kannada': 'kn',
        'Marathi': 'mr',
        'Tamil': 'ta',
        'Telugu': 'te'
    }

    translator = Translator(service_urls=['translate.google.com'])

    for language, code in languages.items():
        translated_json = input_json.copy()
        translated_json['title'] = translator.translate(input_json['title'], dest=code).text
        translated_json['content'] = translator.translate(input_json['content'], dest=code).text

        output_file = f"translated_{language.lower()}.json"
        with open(output_file, 'w') as f:
            json.dump(translated_json, f, indent=4)
        print(f"Translated JSON for {language} saved as {output_file}")



#     json_data = json.load(file)
directory_path = './outputs/final_cleaned_json/'
files = os.listdir(directory_path)
latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
latest_content_json = os.path.join(directory_path, latest_file)
with open(latest_content_json, 'r') as file:
    json_data = json.load(file)
print(latest_content_json)

translate_json(latest_content_json)
