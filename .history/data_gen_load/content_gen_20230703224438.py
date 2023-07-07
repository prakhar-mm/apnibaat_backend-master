import openai
from openai.error import OpenAIError
import time
import json
from datetime import datetime
from dotenv import load_dotenv
import os
# To help construct our Chat Messages
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

# We will be using a chat model, defaults to gpt-3.5-turbo
from langchain.chat_models import ChatOpenAI

# To parse outputs and get structured data back
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

chat_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=openai_api_key)

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
    content_idea = data['topic']

    data = {}
    response = chat_gpt(
        "Give me an article idea for indian audiences or just redefine my content idea-", content_idea)
    article_idea = response.strip()

    content_data = {}
    content_data[category] = {}
    response = chat_gpt(
        "In not more than thousand words and Keeping in mind that the article is for indian audience Write an article on:", article_idea)
    article_content = response.strip()
    content_data[category]["Article 1"] = {
        "Title": article_idea,
        "Content": article_content
    }

    data.update(content_data)

output_directory = os.path.join(os.getcwd(), "./outputs/content")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"article_data_{timestamp}.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
