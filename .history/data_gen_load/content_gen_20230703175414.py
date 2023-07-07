# working

# calling openai api to write content for us
import keys.ekeys as key
import openai
from openai.error import OpenAIError
import time
import re
import os
import json
from datetime import datetime

import sys
sys.path.append('./')

openai.api_key = key.openai_key

# Define keywords for each category.
category_keywords = {
    "Bollywood": ["Bollywood", "movie", "celebrity", "film", "actor", "actress"],
    "Politics": ["politics", "government", "election", "party", "law"],
    # Add more categories and their keywords here.
    # ...
}


def categorize_content(content):
    # Loop over the categories.
    for category, keywords in category_keywords.items():
        # Loop over the keywords of the category.
        for keyword in keywords:
            # Check if the content contains the keyword.
            if keyword.lower() in content.lower():
                # Return the category if it contains the keyword.
                return category
    # Return 'Other' if no category is found.
    return "Other"


def chat_gpt(instruction, content, max_retries=2):
    # ...
    # The rest of your code
    # ...


filepath = './inputs.json'
input_data = {}
with open(filepath) as f:
    input_data = json.load(f)

# Change 'cat' to 'topic'.
for topic, data in input_data.items():
    content_idea = data['topic']
    num_of_ideas = int(data['article_num'])
    num_of_ideas = min(num_of_ideas, 5)  # Limit the number of articles to 5.

    data = {}
    response = chat_gpt(
        f"Give me {num_of_ideas} article ideas for Indian audiences or just redefine my content idea-", content_idea)
    article_ideas = response.strip().split("\n")

    for i, article_idea in enumerate(article_ideas):
        response = chat_gpt(
            "In not more than thousand words and keeping in mind that the article is for Indian audience, write an article on:", article_idea)
        article_content = response.strip()
        # Determine the category based on the article content.
        category = categorize_content(article_content)
        if category not in data:
            data[category] = {}
        data[category][f"Article {i+1}"] = {
            "Title": article_idea,
            "Content": article_content
        }

        time.sleep(5)

    # The rest of your code
    # ...
