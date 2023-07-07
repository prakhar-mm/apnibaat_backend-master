import json
import random
import os


# set the path to the output directory
output_dir = os.path.expanduser("./outputs/authors")

# create the output directory if it doesn't already exist

os.makedirs(output_dir, exist_ok=True)

# assign category affinity scores and bio to authors
categories = ["Entertainment", "News", "Food", "Spirituality", "Tourism", "Gadgets", "Wellness", "Style", "Heritage", "Money", "Jobs", "Business", "Internet", "Cars", "Games", "Exercise", "Concerts", "Art", "DIY", "Nature", "Gender", "Psychology", "Science", "Motivation", "Family", "Mythology", "Sustainability", "Meditation", "Books", "Men", "Humor", "Television", "Startups", "Bikes", "Personality", "Mobiles", "Mythology", "Fashion", "Health", "Economy", "Spirituality", "Design", "Food", "International", "Movies", "Finance", "Minimalism", "Travel", "Reviews","General"]

authors = {
    "Aarav Singh": "Aarav is an investigative journalist with a passion for uncovering the truth. He has won numerous awards for his reporting on corruption and human rights abuses.",
    "Anjali Desai": "Anjali is a veteran journalist with over 20 years of experience covering politics and international affairs. She is known for her insightful analysis and hard-hitting reporting.",
    "Arjun Patel": "Arjun is a young journalist with a talent for finding untold stories. He has a keen eye for detail and is always on the lookout for the next big scoop.",
    "Bhavya Gupta": "Bhavya is a freelance journalist who specializes in environmental and social justice issues. She has a knack for bringing attention to under-reported stories and giving a voice to marginalized communities.",
    "Darshan Joshi": "Darshan is a features writer with a passion for exploring the human experience. He is known for his thoughtful, empathetic approach to storytelling.",
    "Dhruv Shah": "Dhruv is a business journalist with a keen eye for trends and analysis. He is a regular contributor to major publications and has been recognized for his in-depth reporting on the economy and financial markets.",
    "Ishaan Sharma": "Ishaan is a political correspondent with a deep understanding of policy and governance. He has covered major elections and events and is respected for his insightful reporting.",
    "Kavya Menon": "Kavya is a lifestyle journalist with a talent for finding the hidden gems in the world of fashion, beauty, and culture. She is known for her upbeat, engaging style.",
    "Manav Patel": "Manav is a technology journalist with a knack for explaining complex concepts in simple terms. He is a regular contributor to major tech publications and is always on the cutting edge of new developments.",
    "Nandini Sharma": "Nandini is a food and travel writer with a passion for discovering new tastes and experiences. She has covered destinations all over the world and is known for her engaging, informative writing style.",
    "Niharika Singh": "Niharika is a health and wellness writer with a focus on holistic approaches to wellness. She has a background in alternative medicine and is passionate about promoting natural health solutions.",
    "Pranav Gupta": "Pranav is a science journalist with a talent for breaking down complex scientific concepts for a general audience. He is a regular contributor to major science publications and has won awards for his reporting on breakthrough discoveries.",
    "Ritvik Sharma": "Ritvik is a sports journalist with a passion for all things athletic. He has covered major events and athletes across the globe and is known for his engaging writing style.",
    "Vivaan Malhotra": "Vivaan is an entertainment journalist with a talent for finding the inside scoop on the latest movies, music, and TV shows. He is known for his witty commentary and engaging interviews with celebrities."
}



author_categories = {}
author_bios = {}

for author in authors:
    author_categories[author] = random.sample(categories, 3)
    author_bios[author] = authors[author]

category_scores = {}


for author in author_categories:
    category_scores[author] = {}
    for category in categories:
        if category in author_categories[author]:
            category_scores[author][category] = round(random.uniform(0, 1), 2)
        else:
            category_scores[author][category] = 0
    category_scores[author]['bio'] = author_bios[author]
    
    
# save the category scores to a JSON file
output_file = os.path.join(output_dir, "category_scores.json")

with open(output_file, "w") as f:
    json.dump(category_scores, f)

print(f"Category scores saved to {output_file}")

#*******************************************************#
#*******************************************************#
#*******************************************************#


# set the path to the output directory
category_scores_file = os.path.join(os.path.expanduser("./outputs/authors"), "category_scores.json")

def get_top_author(category, category_scores_file):
    # Load the category scores from the JSON file
    with open(category_scores_file, "r") as f:
        category_scores = json.load(f)

    # Filter the authors based on the category
    authors = []
    for author, scores in category_scores.items():
        if category in scores:
            authors.append({**{"name": author}, **scores})

    # If there are no authors with the given category, return None
    if not authors:
        return None

    # Randomly select 5 authors
    selected_authors = random.sample(authors, 5)

    # Find the author with the maximum score for the given category
    max_score = -1
    top_author = None
    for author in selected_authors:
        if author[category] > max_score:
            max_score = author[category]
            top_author = author

    return top_author

category = "General"

top_author = get_top_author(category, category_scores_file)
if top_author is not None:
    print(f"The top author for {category} is {top_author['name']}")
else:
    print(f"No authors found for {category}")