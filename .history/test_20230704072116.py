from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv('OPENAI_KEY')

# Print the OPENAI_KEY
print(openai_key)
