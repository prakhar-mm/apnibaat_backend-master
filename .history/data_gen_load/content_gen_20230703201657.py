
import openai
from openai.error import OpenAIError
import time
import re
import json
from datetime import datetime
#import keys.ekeys as key
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


openai.api_key = os.getenv('OPENAI_KEY')


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


filepath = './inputs.json'
input_data = {}
with open(filepath) as f:
    input_data = json.load(f)

for cat, data in input_data.items():
    category = cat
    num_of_ideas = min(5, int(data['article_num']))
    content_idea = data['topic']

    data = {}
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
        time.sleep(5)

    data.update(content_data)

output_directory = os.path.join(os.getcwd(), ".\outputs\content")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"article_data_{timestamp}.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

os.system("nohup python3 content_gen.py &")
