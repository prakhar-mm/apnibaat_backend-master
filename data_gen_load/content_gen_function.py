import glob

from datetime import datetime
import openai
import json
import os
import subprocess
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Now you can access the keys in .env as environment variables
openai.api_key = os.getenv('OPENAI_KEY')

# %%
from pydantic import BaseModel, Field
from simpleaichat import AIChat

ai = AIChat(
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model="gpt-3.5-turbo-0613",
    params={"temperature": 0.7},
)

class get_event_metadata(BaseModel):
    """Based on an article, fill out the details"""

    content: str = Field(description="blog article about prompt in around 1000 tokens. Add logical markdowns if missing in Content")
    title: str = Field(description="article headline to generate maximum engagement")
    catagory: int = Field(description="The category of the article")
    Products: str = Field(description="items that can be sold to person reading this article")
    Summary: str = Field(description="article summary in 50 words ")

# returns a dict, with keys ordered as in the schema
ai("First iPhone announcement", output_schema=get_event_metadata)


# # Initialize the chat model
# chat_model = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo-16k', openai_api_key=openai_key)

# def generate_article(topic):
#     # The schema I want out
#     response_schemas = [
#         ResponseSchema(name="Content", description="article about prompt in around 1000 tokens. Add logical markdowns if missing in Content"),
#         ResponseSchema(name="Title", description="article headline to generate maximum clicks"),
#         ResponseSchema(name="Category", description="The category of the article."),
#         ResponseSchema(name="Products", description="items I can sell to person reading this article"),
#         ResponseSchema(name="Summary", description="Artistic summary of the article in 2 sentences.Use simple language that start with the main subject, such as 'Portrait of woman','unicorn with tiger stripes', 'giant robot standing' etc, followed by descriptive terms like 'beautiful lighting','ultra-realistic', 'graceful', 'detailed face' etc")
        
#     ]

#     # The parser that will look for the LLM output in my schema and return it back to me
#     output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

#     # The format instructions that LangChain makes. Let's look at them
#     format_instructions = output_parser.get_format_instructions()

#     # The prompt template that brings it all together
#     # Note: This is a different prompt template than before because we are using a Chat Model
#     prompt = ChatPromptTemplate(
#     messages=[
#         HumanMessagePromptTemplate.from_template("For Indian audiences write an article on: {topic}\n \
#                                                     {format_instructions}\n{user_prompt}")
#     ],
#     input_variables=["topic", "user_prompt"],
#     partial_variables={"format_instructions": format_instructions}
#     )

#     article_query = prompt.format_prompt(topic=topic, user_prompt=topic)

#     article_output = chat_model(article_query.to_messages())
#     output = output_parser.parse(article_output.content)
    
#     return output

# Loading inputs
filepath = './inputdummy.json'
input_data = {}
with open(filepath) as f:
    input_data = json.load(f)

# Generating articles
output = {}
for cat, data in input_data.items():
    topic = data['topic']
    p="For Indian audience write me an article on {topic}"
    output[cat] = ai(p,output_schema=get_event_metadata)



# Convert the keys to lowercase except for "Products"
output_json = {outer_key: {inner_key if inner_key == "Products" else inner_key.lower(): value for inner_key, value in inner_dict.items()} for outer_key, inner_dict in output.items()}



# Writing output to JSON file
output_directory = os.path.join(os.getcwd(), "./outputs/content")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"article_data_{timestamp}.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)

# Delete all files in the output directory except the file we just created
files = glob.glob(os.path.join(output_directory, '*'))
for f in files:
    if f != filepath:  # prevent deleting the file we just created
        os.remove(f)
