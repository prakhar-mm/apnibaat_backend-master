from google.cloud import translate_v2 as translate
import json
import os
import time
from datetime import datetime
import shutil

# Replace with your Google Cloud API key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './keys/translate/custom-defender-377912-f75180027dcd.json'

translate_client = translate.Client()

def translate_text(text, target_language="hi"):
    while True:
        try:
            result = translate_client.translate(text, target_language=target_language)
            return result['translatedText']
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)
            continue

# Create a directory for the partial output files
output_dir = './outputs/translated/partial_out'
os.makedirs(output_dir, exist_ok=True)

# Read the input JSON file
# with open('./outputs/cleaned_json/cleaned.json', 'r') as file:
#     json_data = json.load(file)
directory_path = './outputs/final_cleaned_json/'
files = os.listdir(directory_path)
latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
latest_content_json = os.path.join(directory_path, latest_file)
with open(latest_content_json, 'r') as file:
    json_data = json.load(file)
print(latest_content_json)

# translated_articles = {}
# if os.path.exists("./outputs/translated/translated_articles.json"):
#     with open('./outputs/translated/translated_articles.json', 'r', encoding='utf-8') as f:
#         translated_articles = json.load(f)


# Process each entry in the JSON data
for i, entry in enumerate(json_data):
    title = entry['title']
    if False:
        pass
    # if title in translated_articles:
    #     print(f'article {title} already translated. Skipping.')
    else:
        partial_output_file = f'{output_dir}/output_{i}.json'
        # print(i,entry)
        # Check if a partial output file already exists for this entry
        if not os.path.exists(partial_output_file):
            # Modify the JSON entry by translating the title and content
            translated_title = translate_text(entry['title'])
            entry['title'] = translated_title

            translated_content = translate_text(entry['content'])
            entry['content'] = translated_content
            
            # translated_articles[title] = {
            #     'translated_title': translated_title,
            #     'translated_content': translated_content
            # }
            # Save the modified JSON entry to a separate output file
            with open(partial_output_file, 'w', encoding='utf-8') as file:
                json.dump(entry, file, ensure_ascii=False, indent=4)

# with open('./outputs/translated/translated_articles.json', 'w', encoding='utf-8') as f:
#     json.dump(translated_articles, f, ensure_ascii=False, indent=4)


# Merge the partial output files into a single output file
merged_data = []
print(merged_data)
for i in range(len(json_data)):
    with open(f'{output_dir}/output_{i}.json', 'r', encoding='utf-8') as file:
        merged_data.append(json.load(file))

# Save the merged JSON data as a new output file
output_directory = './outputs/translated/'
os.makedirs(output_directory, exist_ok=True)
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file_path = os.path.join(output_directory,f'translated_merged_article_data_{now}.json')
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

# to delete the temp partial outputs
shutil.rmtree(output_dir)