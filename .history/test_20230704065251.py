
import openai
from openai.error import OpenAIError
import time
import json
#from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# To help construct our Chat Messages
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

# We will be using a chat model, defaults to gpt-3.5-turbo
from langchain.chat_models import ChatOpenAI

# To parse outputs and get structured data back
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# Load .env file

print(os.getenv('OPENAI_KEY'))
openai.api_key = os.getenv('OPENAI_KEY')


chat_model = ChatOpenAI(
    temperature=0, model_name='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_KEY'))
