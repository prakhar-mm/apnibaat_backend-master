# working

# calling openai api to write conten for us
import keys.ekeys as key
import openai
from openai.error import OpenAIError
import time
import re
import os
import json
from datetime import datetime

import sys
sys.path.append('./')

openai.api_key = key.openai_key


def chat_gpt(instruction, content, max_retries=2):
    prompt = f"{instruction}: {content}"

    retries = 0
    while retries <= max_retries:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.7,
            )

            if response.choices:
                return response.choices[0].text.strip()
            else:
                return "Sorry, I couldn't generate a response."
        except OpenAIError as e:
            retries += 1
            if retries > max_retries:
                print("Error: Maximum retries reached. Aborting.")
                raise e
            print(f"Error: {e}. Retrying... ({retries}/{max_retries})")
            time.sleep(5)  # Wait for 5 seconds before retrying


content_ideas = {}

# *** write code to take input of these two following vars***
# max number of ideas = 5
# max possible value of key is 49, so ignore any other key less than 1 or greater than 49
num_of_ideas = 5

filepath = './inputs.json'
input_data = {}
with open(filepath) as f:
    input_data = json.load(f)
for cat, data in input_data.items():
    # print(f'category = {cat}')
    # print(f'data = {data}')
    category = cat
    num = int(data['article_num'])
    if num <= 5:
        num_of_ideas = num

    content_idea = data['topic']

print(category)
print(content_idea, num_of_ideas)

input_keys = [1]
{  # input
    # num = input("Number of articles to generate per idea (max 5) = ")
    # for i in content_ideas:
    #     print(i, content_ideas[i])
    # inkey = input("List all the idea numbers seperated with comma from the above list to generate ideas: ")
    # inkey = inkey.split(',')
    # print(inkey)

    # for i in inkey:
    #     if int(i) < 50 and int(i) > 0:
    #         input_keys.append(int(i))

    # print(num_of_ideas)
    # print(input_keys)
    # print('*****************')
}


data = {}

for key in input_keys:
    # content_idea = content_ideas[key]
    response = chat_gpt(
        f"Give me {num_of_ideas} article ideas for indian audiences or just redefine my content idea-", content_idea)
    article_ideas = response.strip().split("\n")
    content_data = {}
    content_data[category] = {}
    for i, article_idea in enumerate(article_ideas):
        response = chat_gpt(
            "In not more than thousand words and Keeping in mind that the article is for indian audience Write an article on:", article_idea)
        article_content = response.strip()
        content_data[category][f"Article {i+1}"] = {
            "Title": article_idea,
            "Content": article_content
        }
        print(content_data)
        time.sleep(5)

    data.update(content_data)

# Function to remove numbers and dashes at the beginning of the string


def clean_string(s):
    return re.sub(r"^\d+\.\s?", "", s)


output_directory = os.path.join(os.getcwd(), ".\outputs\content")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"article_data_{timestamp}.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

os.system("nohup python3 EvergreenContentGeneration.py &")
