import glob
import json
from datetime import datetime
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Now you can access the keys in .env as environment variables
openai_key = os.getenv('OPENAI_KEY')

# Initialize the chat model
chat_model = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo', openai_api_key=openai_key)

def generate_article(topic):
    # The schema I want out
    response_schemas = [
        ResponseSchema(name="title", description="The clickbait title of the article"),
        ResponseSchema(name="content", description="content of the article in around 700 words"),
        ResponseSchema(name="category", description="The category of the article"),
        ResponseSchema(name="Products", description="items I can sell to person reading this article"),
        ResponseSchema(name="summary", description="brief to a painter for the article in 2-3 sentences")
        
    ]

    # The parser that will look for the LLM output in my schema and return it back to me
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # The format instructions that LangChain makes. Let's look at them
    format_instructions = output_parser.get_format_instructions()

    # The prompt template that brings it all together
    # Note: This is a different prompt template than before because we are using a Chat Model
    prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("For Indian audiences write an article on: {topic}\n \
                                                    {format_instructions}\n{user_prompt}")
    ],
    input_variables=["topic", "user_prompt"],
    partial_variables={"format_instructions": format_instructions}
    )

    article_query = prompt.format_prompt(topic=topic, user_prompt=topic)

    article_output = chat_model(article_query.to_messages())
    output = output_parser.parse(article_output.content)
    
    return output

# Loading inputs
filepath = './inputs.json'
input_data = {}
with open(filepath) as f:
    input_data = json.load(f)

# Generating articles
output = {}
for cat, data in input_data.items():
    topic = data['topic']
    output[cat] = generate_article(topic)

# Writing output to JSON file
output_directory = os.path.join(os.getcwd(), "./outputs/content")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"article_data_{timestamp}.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

# Delete all files in the output directory except the file we just created
files = glob.glob(os.path.join(output_directory, '*'))
for f in files:
    if f != filepath:  # prevent deleting the file we just created
        os.remove(f)
