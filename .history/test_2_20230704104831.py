import json
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# Initialize the chat model
chat_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key='your-api-key-here')

# Define the response schema
response_schemas = [
    ResponseSchema(name="Title", description="The title of the article"),
    ResponseSchema(name="Content", description="The content of the article"),
]

# Prepare the parser
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Get the format instructions
format_instructions = output_parser.get_format_instructions()

# Prepare the chat prompt
prompt_template = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("Write an approx 1000 words article on the provided topic. \n \
                                                    {format_instructions}\n{user_prompt}")
    ],
    input_variables=["user_prompt"],
    partial_variables={"format_instructions": format_instructions}
)

# Load the input file
with open('inputs.json', 'r') as f:
    data = json.load(f)

for cat, data in data.items():
    topic = data['topic']

    # Prepare the prompt
    chat_prompt = prompt_template.format_prompt(user_prompt=topic)

    # Get the output from the chat model
    chat_output = chat_model(chat_prompt.to_messages())

    # Parse the output
    output = output_parser.parse(chat_output.content)

    print(output)
