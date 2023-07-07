import subprocess
import time
import streamlit as st
import os
import json
from PIL import Image

scripts = [
    './data_gen_load/content_gen.py',
    './data_gen_load/img_gen.py',
    './data_gen_load/cloudinary_upload.py',
    './data_gen_load/pre_fb_cleanup.py',
    './data_gen_load/content_cleaner.py',
    './data_gen_load/translator.py',
    './data_gen_load/firebase_upload.py',
]

st.title('Article generator')

topic = st.text_input('Type the topic/title for Article to be generated:')
submit_button = st.button('Submit')

# Determine present working directory
present_dir = os.getcwd()
filepath = os.path.join(present_dir, 'inputs.json')

if submit_button and topic != '':
    input_data = {topic: {'topic': topic, 'article_num': 1}}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(input_data, f, ensure_ascii=False, indent=4)

    max_retries = 3
    retry_delay = 5
    processes = []

    for script in scripts:
        retry_count = 0
        while retry_count < max_retries:
            try:
                st.write(f'{script} is running ...')
                process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                processes.append(process)
                output, error = process.communicate()
                st.write(f"--- Output from {script} ---")
                st.code(output)
                st.write(f"--- Error from {script} ---")
                st.code(error)
                st.write(f'{script} has finished running.')
                break
            except Exception as e:
                retry_count += 1
                st.error(f"Error running script '{script}': {str(e)}")
                st.info(f"Retrying {script} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            st.error(f"Max retries exceeded for script '{script}'. Skipping...")

        if script == './data_gen_load/content_gen.py':
            process.wait()  # make sure the process is done
            directory_path = './outputs/content/'
            files = os.listdir(directory_path)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
            latest_content_json = os.path.join(directory_path, latest_file)
            with open(latest_content_json) as f:
                data = json.load(f)
            for topic, categories in data.items():
                st.write('---')
                st.subheader(f"Topic: {topic}")
                for category, articles in categories.items():
                    for article_key, item in articles.items():
                        st.write('---')
                        st.subheader(item['Title'])
                        st.write(item['Content'])

        if script == './data_gen_load/img_gen.py':
            process.wait()  # make sure the process is done
            with open('outputs/json_with_img_path/article_data_imageUrl_slug.json') as f:
                data = json.load(f)
            for topic, categories in data.items():
                for category, articles in categories.items():
                    for article_key, item in articles.items():
                        img_path = item['Image_url']
                        image = Image.open(img_path)
                        st.image(image, caption=f'generated_image_{item["Slug"]}', use_column_width=True)

        if script == './data_gen_load/firebase_upload.py':
            process.wait()  # make sure the process is done
            st.write('Content uploaded successfully!')
