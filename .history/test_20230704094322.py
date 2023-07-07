from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Now you can access the keys in .env as environment variables
openai_key = os.getenv('OPENAI_KEY')
print(openai_key)

# similarly for other keys
# other_key = os.getenv('OTHER_KEY')



# Now you can access the keys in .env as environment variables
STABILITY_KEY = os.getenv('STABILITY_KEY')
print(STABILITY_KEY)
