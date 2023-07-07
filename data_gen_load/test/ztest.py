# import json

# num_of_ideas = 5

# filepath = './inputs.json'
# input_data = {}
# with open(filepath) as f:
#     input_data = json.load(f)

# # num= input_data['article_num']
# # if int(num) <= 5: 
# #     num_of_ideas = int(num)

# # content_idea = input_data['topic']
# # print(content_idea, num_of_ideas)


# for cat, data in input_data.items():
#     print(f'category = {cat}')
#     print(f'data = {data}')
#     num = int(data['article_num'])
#     if num <= 5: 
#         num_of_ideas = num

#     content_idea = data['topic']
# d = {}
# categorey = 'Wellness'
# d = {categorey:{'topic':content_idea, 'article_num':num}}
# print(f'input data = {input_data}, \n d = {d}')
# if 'tags' not in input_data[categorey]:
#     print('yoo hoo!')
# print(input_data)






# import streamlit as st

# # Streamlit framework
# st.title('Dropdown List Example')

# # Define the options for the dropdown list
# categories = ["Entertainment", "News", "Food", "Spirituality", "Tourism", "Gadgets", "Wellness", "Style", "Heritage", "Money", "Jobs", "Business", "Internet", "Cars", "Games", "Exercise", "Concerts", "Art", "DIY", "Nature", "Gender", "Psychology", "Science", "Motivation", "Family", "Mythology", "Sustainability", "Meditation", "Books", "Men", "Humor", "Television", "Startups", "Bikes", "Personality", "Mobiles", "Mythology", "Fashion", "Health", "Economy", "Spirituality", "Design", "Food", "International", "Movies", "Finance", "Minimalism", "Travel", "Reviews"]

# # Display the dropdown list
# selected_option = st.selectbox('Select an option:', categories)

# # Use the selected option
# st.write(f"You selected: {selected_option}")







import os
import json

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
        print(item['Content'])
        # st.write(item['topic'])