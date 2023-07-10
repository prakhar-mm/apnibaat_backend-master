# %%
import openai
import json
import os
import subprocess

# load and set our key
openai.api_key = os.environ["OPENAI_API_KEY"]

# %%
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's 24.546+33.2323?"}],
)
