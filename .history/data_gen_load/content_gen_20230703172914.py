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


content_ideas = {1: 'Bollywood movies and celebrities', 2: 'Politics and current events', 3: 'Indian cuisine and recipes',
                 4: 'Religion and spirituality', 5: 'Travel destinations in India', 6: 'Technology and gadgets', 7: 'Health and wellness tips',
                 8: 'Indian fashion and beauty trends', 9: 'History and culture of India', 10: 'Personal finance and investments',
                 11: 'Education and career guidance', 12: 'Business and entrepreneurship', 13: 'Social media trends and influencers',
                 14: 'Automobiles and bikes', 15: 'Gaming and esports', 16: 'Fitness and exercise routines', 17: 'Music and concerts',
                 18: 'Art and photography', 19: 'DIY home improvement and renovation ideas', 20: 'Wildlife and nature conservation',
                 21: 'Feminism and gender issues', 22: 'Mental health and self-care', 23: 'Science and innovation',
                 24: 'Inspirational stories of successful individuals', 25: 'Parenting and child-rearing tips', 26: 'Mythology and folklore',
                 27: 'Environmental issues and sustainability', 28: 'Yoga and meditation practices', 29: 'Indian literature and poetry',
                 30: 'Fashion and style tips for men', 31: 'Comedy and humor content', 32: 'TV shows and web series reviews',
                 33: 'Technology startups and innovation hubs', 34: 'Motorcycles and their customization', 35: 'Psychology and personality development',
                 36: 'Latest mobile phones and gadgets', 37: 'Indian mythological web series', 38: 'DIY fashion and jewelry making ideas',
                 39: 'Medical and health news', 40: 'Economic trends and business news', 41: 'Indian spiritual practices and beliefs',
                 42: 'Interior designing and home decor ideas', 43: 'Indian street food and its origin', 44: 'Global news from an Indian perspective',
                 45: 'Cinema history and trends', 46: 'Indian stock market and investing tips', 47: 'Mindful living and minimalism',
                 48: 'Indian travel bloggers and influencers', 49: 'Reviews and comparisons of consumer products'
                 }

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
