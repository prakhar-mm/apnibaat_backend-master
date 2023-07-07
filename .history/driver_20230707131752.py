import subprocess
import time
import streamlit as st
import os
import json
from PIL import Image
import glob


scripts = [
    './data_gen_load/content_gen.py',
    './data_gen_load/img_gen.py',
    #'./data_gen_load/cloudinary_upload.py',
    #'./data_gen_load/pre_fb_cleanup.py',
    #'./data_gen_load/translator_cost_effective.py',
    #'./data_gen_load/firebase_upload.py',
]
scripts_1 = [
    #'./data_gen_load/content_gen.py',
    #'./data_gen_load/img_gen.py',
    './data_gen_load/cloudinary_upload.py',
    './data_gen_load/pre_fb_cleanup.py',
    './data_gen_load/translator_cost_effective.py',
    './data_gen_load/firebase_upload.py',
]

st.title('Article generator')
# Check if 'submit' is in the session state (initialize it if not)
if 'publish_1' not in st.session_state:
    st.session_state.publish_1 = False
if 'submit' not in st.session_state:
    st.session_state.submit = False
topic = st.text_input('Type the topic/title for Article to be generated:', value='Try Something')
submit_button = st.button('Submit')
if submit_button:
    st.session_state.submit = True


# Determine present working directory
present_dir = os.getcwd()
filepath = os.path.join(present_dir, 'inputs.json')

if submit_button and topic != '' and topic != 'Try Something':
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

                # Display error only if there is an error message
                if error:
                    st.write(f"--- Error from {script} ---")
                    st.code(error)
                st.write(f'{script} has finished running.')

                # Check if there is any unexpected null output or error
                if output is None or error is None:
                    st.error(f"Unexpected null output or error from script '{script}'. Stopping the execution.")
                    break

                break
            except Exception as e:
                retry_count += 1
                st.error(f"Error running script '{script}': {str(e)}")
                st.info(f"Retrying {script} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            st.error(f"Max retries exceeded for script '{script}'. Skipping...")
            break

        # Rest of the code for processing each script
        if script == './data_gen_load/content_gen.py':
            process.wait()  # make sure the process is done
            directory_path = './outputs/content/'
            files = os.listdir(directory_path)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
            latest_content_json = os.path.join(directory_path, latest_file)
            with open(latest_content_json) as f:
                data = json.load(f)
            for topic, article in data.items():
                st.write('---')
                #st.subheader(f"Topic: {topic}")
                st.write(f"Category: {article['category']}")
                st.subheader(f"Title: {article['title']}")
                st.write(f"Content: {article['content']}")

        if script == './data_gen_load/img_gen.py':
            process.wait()  # make sure the process is done
            with open('outputs/json_with_img_path/article_data_imageUrl_slug.json') as f:
                data = json.load(f)
            for topic, article in data.items():
                img_path = article['Image_url']
                image = Image.open(img_path)
                st.image(image, caption=f'generated_image_{article["Slug"]}', use_column_width=True)

if st.session_state.submit and topic != '' and topic != 'Try Something':
    
    genre = st.radio(
            "Have you reviewed the article?",
            ('Publish', 'Abort')
            )

    if genre == 'Publish' :
            button_label = ":green[Publish]"
    else:
        button_label = ":red[Abort]"
    publish_button = st.button(button_label)
    if publish_button:
        st.session_state.publish_1 = True

    if publish_button and genre != '':            
        if genre == 'Publish':
            st.write('Publishing Article please wait')
            max_retries = 3
            retry_delay = 5
            processes = []
            for script in scripts_1:
                subprocess.run(["python", script])
            st.write('Article Published')
            # Empty the inputs.json file
            files = glob.glob('outputs/content/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            # Get list of all .png files
            png_files = glob.glob('outputs/images/*.png')

            # Find the latest file (by modification time)
            latest_file = max(png_files, key=os.path.getmtime) if png_files else None

            # Extract the file name only (without the directory path and extension)
            file_name = None
            if latest_file:
                file_name = latest_file.split('/')[-1].split('.')[0]

            base_url = "https://www.apnibaat.in/post/{}?lang=Hindi"
            url = base_url.format(file_name)

            
            files = glob.glob('outputs/images/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/translated/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/final_cleaned_json/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/json_with_img_path/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/json_with_img_url/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            with open('inputs.json', 'w') as json_file:
                json.dump({"Try Something": {
                    "topic": "Try Something",
                    "article_num": 1
                    }}, json_file)
            #topic = st.text_input('Type the topic/title for Article to be generated:')
            st.session_state.submit = False
            time.sleep(5)  
            
            
        else:
            st.write('Process aborted')
            files = glob.glob('outputs/content/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/images/**/*.json',recursive=True)
            for f in files:
                os.remove(f)
            
            
            
            # Empty the inputs.json file
            with open('inputs.json', 'w') as json_file:
                json.dump({"Try Something": {
                    "topic": "Try Something",
                    "article_num": 1
                    }}, json_file)
            #topic = st.text_input('Type the topic/title for Article to be generated:')
            st.session_state.submit = False
            time.sleep(5)  # Pause for 5 seconds
            st.experimental_rerun()

if st.session_state.publish_1 and topic != '' and topic != 'Try Something':            
    st.write(f"The URL is: {url}")

if st.session_state.submit and topic != '' and topic != 'Try Something':            
    another_publish_button = st.button(":green[Publish Another Article]")
    st.experimental_rerun()