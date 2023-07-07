""
Created on Tue Jul  4 05: 17: 46 2023


@author: sudhirsundrani
"""

# To help construct our Chat Messages
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

# We will be using a chat model, defaults to gpt-3.5-turbo
from langchain.chat_models import ChatOpenAI

# To parse outputs and get structured data back
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

openai.api_key = "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"

chat_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=openai_api_key)