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
            files = glob.glob('outputs/content/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/images/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/translated/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/final_cleaned_json/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/json_with_img_path/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/json_with_img_path/**/*.json')
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
            st.experimental_rerun()
            
        else:
            st.write('Process aborted')
            files = glob.glob('outputs/content/**/*.json')
            for f in files:
                os.remove(f)
            files = glob.glob('outputs/images/**/*.json')
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
            


