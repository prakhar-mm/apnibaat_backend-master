import subprocess
import time
import streamlit as st
from streamlit import session_state
import os
import json
from PIL import Image

scripts = [
    './data_gen_load/content_gen.py',
    # './data_gen_load/authors.py',
    './data_gen_load/img_gen.py',#...
    './data_gen_load/cloudinary_upload.py',
    './data_gen_load/pre_fb_cleanup.py',#...
    './data_gen_load/content_cleaner.py',
    './data_gen_load/translator.py',
    './data_gen_load/firebase_upload.py',
]

# Add more scripts as needed



# streamlit framework
st.title('Article generator')

input_data = {}

# Define the options for the dropdown list
categories = ["--select--" ,"Entertainment", "News", "Food", "Spirituality", "Tourism", "Gadgets", "Wellness", "Style", "Heritage", "Money", "Jobs", "Business", "Internet", "Cars", "Games", "Exercise", "Concerts", "Art", "DIY", "Nature", "Gender", "Psychology", "Science", "Motivation", "Family", "Mythology", "Sustainability", "Meditation", "Books", "Men", "Humor", "Television", "Startups", "Bikes", "Personality", "Mobiles", "Mythology", "Fashion", "Health", "Economy", "Spirituality", "Design", "Food", "International", "Movies", "Finance", "Minimalism", "Travel", "Reviews"]
# Display the dropdown list
category = st.selectbox('Select a category for which the article is to be generated:', categories)
# Use the selected option
st.write(f"You selected: {category}")
# input topic and number of artices t be generated
topic = st.text_input('Type the topic/title for Article to be generated:')
num_of_articles =  st.text_input('Number of Article/s to be generated for each topic/title:')
input_data = {category:{'topic': topic, 'article_num': num_of_articles}}
# input_data['topic'] = topic
# input_data['article_num'] = num_of_articles
submit_button = st.button('Submit')
filepath = './inputs.json'


if submit_button and category != '--select--':
    # create file and save the title/titles
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(input_data, f, ensure_ascii=False, indent=4)

    max_retries = 3
    retry_delay = 5
    processes = []
    p_count = 0
    break_op =False

    for script in scripts:
        retry_count = 0
        while retry_count < max_retries:
            try:
                # break
                # if p_count == 1 or p_count ==2:
                #     break
                st.write(f'{script} is running ...')
                process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # process.wait()
                processes.append(process)
                output, error = process.communicate()
                st.write(f"--- Output from {script} ---")
                st.code(output)
                st.write(f"--- Error from {script} ---")
                st.code(error)
                st.write(f'script have finished running.')
                break  # Break out of the retry loop if no error occurs
            except Exception as e:
                retry_count += 1
                print(f"Error running script '{script}': {str(e)}")
                print(f"Retrying {script} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            print(f"Max retries exceeded for script '{script}'. Skipping...")
        
        #** update count
        p_count += 1

        #** add if conditions here

        # printing the content after it have been generated
        if p_count == 1: # print the article's content
            for process in processes:
                process.wait()
            # Open the JSON file
            directory_path = './outputs/content/'
            files = os.listdir(directory_path)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
            latest_content_json = os.path.join(directory_path, latest_file)
            with open(latest_content_json) as f:
                data = json.load(f)
            # Loop through each item in the JSON data
            for category, articles in data.items():
                # Loop through each article in the category
                for article_key, item in articles.items():
                    st.write('---')
                    st.subheader(item['Title'])
                    st.write(item['Content'])
        
        # printing img after it have been generated
        if p_count == 2:
            for process in processes:
                process.wait()
            with open('outputs/json_with_img_path/article_data_imageUrl_slug.json') as f:
                data = json.load(f)
            for category, articles in data.items():
                for article_key, item in articles.items():
                    img_path = item['Image_url']
                    image = Image.open(img_path)
                    # image.show()
                    # st.write(img_path)
                    st.image(image, caption=f'generated_image_{item["Slug"]}', use_column_width=True)
            # upload = st.button('Proceed to upload')
            # cancel = st.button('Cancel upload')
        # After image and cntent generation
        # to break the content generation or not
            # if cancel:
            #     st.write('Content generation stopped.')
            #     break
            # if upload:
            #     st.write('Continuing with the upload of artilce.')
            #     continue
        
        if p_count == 7:
            st.write('Content uplaoded sucessfully!')

    # Wait for all processes to finish
    # for process in processes:
    #     process.wait()