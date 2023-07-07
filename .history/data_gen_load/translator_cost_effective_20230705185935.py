from googletrans import Translator
import json
import os
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

        output_directory = os.path.join('.outputs/translated', language.lower())
        os.makedirs(output_directory, exist_ok=True)

        # Delete any existing JSON file within the language-specific folder
        existing_files = os.listdir(output_directory)
        for file in existing_files:
            file_path = os.path.join(output_directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        output_file = os.path.join(output_directory, f"translated_{language.lower()}.json")

        with open(output_file, 'w') as f:
            json.dump(translated_json, f, indent=4, ensure_ascii=False)
        print(f"Translated JSON for {language} saved as {output_file}")

directory_path = './outputs/final_cleaned_json/'
files = os.listdir(directory_path)
latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
latest_content_json = os.path.join(directory_path, latest_file)

with open(latest_content_json, 'r') as file:
    json_data = json.load(file)

translate_json(json_data)
