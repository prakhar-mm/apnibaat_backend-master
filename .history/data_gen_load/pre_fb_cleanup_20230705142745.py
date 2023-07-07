#working
import json
import re
from datetime import datetime, timedelta
import os
import random
import string
import re
import nltk
# nltk.download('punkt')
from textblob import TextBlob
import random
import uuid
import hashlib


from datetime import datetime

iso_string = '2022-04-01T12:30:45.678901'
dt = datetime.fromisoformat(iso_string)

# print(dt)

# Load the JSON file

input_file = os.path.expanduser("./outputs/json_with_img_url/article_data_with_cloudinary_urls.json")
# output_file = os.path.expanduser("~/Downloads/ndtv/summarized_content_cleaned.json")
# set the path to the output directory
authors_json = os.path.join(os.path.expanduser("./outputs/authors/"), "authors.json")
with open(authors_json, "r") as f:
    category_scores = json.load(f)
# print(category_scores)
def get_top_author(category):
    # Load the category scores from the JSON file
    # with open(authors_json, "r") as f:
    #     category_scores = json.load(f)

    # Filter the authors based on the category
    authors = []
    for author, scores in category_scores.items():
        if category in scores:
            authors.append({**{"name": author}, **scores})

    # If there are no authors with the given category, return None
    if not authors:
        return "Bhavya Gupta"

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


categories = ["Entertainment", "News", "Food", "Spirituality", "Tourism", "Gadgets", "Wellness", "Style", "Heritage", "Money", "Jobs", "Business", "Internet", "Cars", "Games", "Exercise", "Concerts", "Art", "DIY", "Nature", "Gender", "Psychology", "Science", "Motivation", "Family", "Mythology", "Sustainability", "Meditation", "Books", "Men", "Humor", "Television", "Startups", "Bikes", "Personality", "Mobiles", "Mythology", "Fashion", "Health", "Economy", "Spirituality", "Design", "Food", "International", "Movies", "Finance", "Minimalism", "Travel", "Reviews","General"]
#print(f'categories len = {len(categories)}')
names = [
    "Aarav Singh",
    "Anjali Desai",
    "Arjun Patel",
    "Bhavya Gupta",
    "Darshan Joshi",
    "Dhruv Shah",
    "Ishaan Sharma",
    "Kavya Menon",
    "Manav Patel",
    "Nandini Sharma",
    "Niharika Singh",
    "Pranav Gupta",
    "Ritvik Sharma",
    "Vivaan Malhotra"
]

Parent_category = {
    "Bollywood movies and celebrities": "Entertainment",
    "Politics and current events": "News",
    "Indian cuisine and recipes": "Food",
    "Religion and spirituality": "Spirituality",
    "Travel destinations in India": "Tourism",
    "Technology and gadgets": "Gadgets",
    "Health and wellness tips": "Wellness",
    "Indian fashion and beauty trends": "Style",
    "History and culture of India": "Heritage",
    "Personal finance and investments": "Money",
    "Education and career guidance": "Jobs",
    "Business and entrepreneurship": "Business",
    "Social media trends and influencers": "Internet",
    "Automobiles and bikes": "Cars",
    "Gaming and esports": "Games",
    "Fitness and exercise routines": "Exercise",
    "Music and concerts": "Concerts",
    "Art and photography": "Art",
    "DIY home improvement and renovation ideas": "DIY",
    "Wildlife and nature conservation": "Nature",
    "Feminism and gender issues": "Gender",
    "Mental health and self-care": "Psychology",
    "Science and innovation": "Science",
    "Inspirational stories of successful individuals": "Motivation",
    "Parenting and child-rearing tips": "Family",
    "Mythology and folklore": "Mythology",
    "Environmental issues and sustainability": "Sustainability",
    "Yoga and meditation practices": "Meditation",
    "Indian literature and poetry": "Books",
    "Fashion and style tips for men": "Men",
    "Comedy and humor content": "Humor",
    "TV shows and web series reviews": "Television",
    "Technology startups and innovation hubs": "Startups",
    "Motorcycles and their customization": "Bikes",
    "Psychology and personality development": "Personality",
    "Latest mobile phones and gadgets": "Mobiles",
    "Indian mythological web series": "Mythology",
    "DIY fashion and jewelry making ideas": "Fashion",
    "Medical and health news": "Health",
    "Economic trends and business news": "Economy",
    "Indian spiritual practices and beliefs": "Spirituality",
    "Interior designing and home decor ideas": "Design",
    "Indian street food and its origin": "Food",
    "Global news from an Indian perspective": "International",
    "Cinema history and trends": "Movies",
    "Indian stock market and investing tips": "Finance",
    "Mindful living and minimalism": "Minimalism",
    "Indian travel bloggers and influencers": "Travel",
    "Reviews and comparisons of consumer products": "Reviews"
}

# Category background color
color_map = {
'Entertainment': 'bg-color-teal',
'News': 'bg-color-blue',
'Food': 'bg-color-red',
'Spirituality': 'bg-color-indigo',
'Tourism': 'bg-color-green',
'Gadgets': 'bg-color-purple',
'Wellness': 'bg-color-gray',
'Style': 'bg-color-pink',
'Heritage': 'bg-color-brown',
'Money': 'bg-color-yellow',
'Jobs': 'bg-color-light-blue',
'Business': 'bg-color-deep-orange',
'Internet': 'bg-color-amber',
'Cars': 'bg-color-cyan',
'Games': 'bg-color-lime',
'Exercise': 'bg-color-light-green',
'Concerts': 'bg-color-teal',
'Art': 'bg-color-indigo',
'DIY': 'bg-color-blue-gray',
'Nature': 'bg-color-green',
'Gender': 'bg-color-pink',
'Psychology': 'bg-color-gray',
'Science': 'bg-color-blue',
'Motivation': 'bg-color-indigo',
'Family': 'bg-color-brown',
'Mythology': 'bg-color-deep-orange',
'Sustainability': 'bg-color-light-green',
'Meditation': 'bg-color-indigo',
'Books': 'bg-color-blue-gray',
'Men': 'bg-color-pink',
'Humor': 'bg-color-teal',
'Television': 'bg-color-cyan',
'Startups': 'bg-color-amber',
'Bikes': 'bg-color-cyan',
'Personality': 'bg-color-gray',
'Mobiles': 'bg-color-purple',
'Fashion': 'bg-color-pink',
'Health': 'bg-color-gray',
'Economy': 'bg-color-yellow',
'Design': 'bg-color-indigo',
'International': 'bg-color-blue',
'Movies': 'bg-color-teal',
'Finance': 'bg-color-yellow',
'Minimalism': 'bg-color-blue-gray',
'Travel': 'bg-color-green',
'Reviews': 'bg-color-lime',
'General': 'bg-color-teal',

}

# Author Bios
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

data_social = {
    "author_social": [
        {
            "icon": "fab fa-facebook-f",
            "url": "https://www.facebook.com/profile.php?id=100091575483556",
        },
        {
            "icon": "fab fa-twitter",
            "url": "https://twitter.com/apnibaat_ai",
        },
        {
            "icon": "fab fa-behance",
            "url": "https://www.behance.net/",
        },
        {
            "icon": "fab fa-linkedin-in",
            "url": "https://www.instagram.com/apnibaat_ai/",
        },
    ]
}

tag = {
    "tags": ['Gaming',
    'Adventure',
    'Travel',
    'Sports',
    'Science',
    'Technology',
    'Fashion',
    'Life Style']
        
    }


# Load the JSON file
with open(input_file) as f:
    data = json.load(f)

def slugify(title):
    """Helper function to convert title to slug"""
    return '-'.join(title.lower().split())


# Loop through each item in the JSON data
for article_key, item in data.items():
    
    # Generate a unique key
    apnibaat_post_unique_key = hashlib.md5(item['title'].encode('utf-8')).hexdigest()
    # Assign the unique key to the item
    item['apnibaat_post_unique_key'] = apnibaat_post_unique_key
    # Perform other operations as needed
    # Clean up the title    
    title = item['title']
    title = re.sub(r'[\n\"]', '', title)  # Remove newlines and quotes
    item['title'] = title.strip()  # Remove leading/trailing whitespace
    title = item['title']
    slug = item['Slug']
    # slug = title.replace(' ', '-').replace(':', '').lower()
    # slug = re.sub('[^0-9a-zA-Z-]+', '', slug).strip('-').lower()
    summary = item['content']
    category = item['category']
    sentences = nltk.sent_tokenize(summary)
    excerpt = " ".join(sentences[:2])
    item['excerpt'] = excerpt
    item['slug'] = slug
    if slug in '':
        item['slug'] = apnibaat_post_unique_key

    # Category extraction
    # Tokenize the text into sentences
    # sentences = nltk.sent_tokenize(sample_text)
    
    # *************************************************
    # *************************************************
    # *************************************************
    
    # WILL HAVE TO ASK USER TO INPUT CATEGORY AS WELL
    item['cate'] = category
    item['cate_bg'] = color_map.get(item['cate'])
    # Loop through each sentence and classify it into a category
    

    # Clean up the summary
    #summary = item['content']
    #summary = re.sub(r'[\n\"]', '', summary)  # Remove newlines and quotes
    #summary = re.sub(r'\s+', ' ', summary)  # Remove extra whitespace
    item['content'] = summary.strip()  # Remove leading/trailing whitespace
    #Social Seed
    post_views_num = random.randint(10, 100)
    item['post_views'] = f'{post_views_num}K Views'
    post_share_num = random.randint(1, 10000)
    item['post_share'] = f'{post_share_num} Shares'

    top_author = get_top_author(category)
    #print('****************')
    #print(category)
    # print(top_author)
    if top_author is not None:
        item['author_name'] = top_author.get('name')
    else:
            item['author_name'] = "Parag Agarwal"

    item['author_desg']='Publisher'
    
    if top_author is not None:
        item['author_bio']=top_author['bio']
    else:
            item['author_bio'] = "Am a random guy. Keen interest in AI"
    item['postFormat']='standard'
    
    item['trending'] = random.choices([True, False], weights=[5, 95])[0]
    random_seconds = random.randint(1, 300)
    # Add the random seconds to the current date and time
    new_date = datetime.now() + timedelta(seconds=random_seconds)
    
    # Format the new date and time as a string in ISO 8601 format
    new_date_str = new_date.isoformat()
    
    # Parse the ISO 8601 formatted string back to a datetime object
    dt = datetime.fromisoformat(new_date_str)
    
    item['date'] = dt.isoformat()
    item['quoteText']='Some times jus chill'
    url=item['Image_url']
    item['featureImg'] = url
    #author_social
    print(item)
    item['author_social'] = data_social['author_social']
    
    if item['author_name'] == 'Parag Agarwal':
        item['author_img'] = "https://res.cloudinary.com/dltay5uwr/image/upload/v1678784926/YelpCamp/szjik5gswadkbipg5zyq.png"
    else :
        item['author_img'] = category_scores[item['author_name']].get('Image_url')
    item['tags'] = tag['tags']


output_data = []
input_data = data

# Extract the data from the input object and append it to the output list
for category_name, category_data in input_data.items():
    for article_name, article_data in category_data.items():
        output_data.append({
            "title": article_data["title"],
            "summary": article_data["excerpt"],
            "apnibaat_post_unique_key": article_data["apnibaat_post_unique_key"],
            "excerpt": article_data["excerpt"],
            "slug": article_data["slug"],
            "cate": article_data["cate"],
            "cate_bg": article_data["cate_bg"],
            "content": article_data["content"],
            "post_views": article_data["post_views"],
            "post_share": article_data["post_share"],
            "author_name": article_data["author_name"],
            "author_desg": article_data["author_desg"],
            "author_bio": article_data["author_bio"],
            "postFormat": article_data["postFormat"],
            "trending": article_data["trending"],
            "date": article_data["date"],
            "quoteText": article_data["quoteText"],
            "featureImg": article_data["featureImg"],
            "author_social": article_data["author_social"],
            "author_img": article_data["author_img"],
            "tags": article_data["tags"]
        })


# Get the current date and time in a string format
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define the output file path
output_dir = "./outputs/final_jsons/"
os.makedirs(output_dir, exist_ok=True)
filename = f"output_{now}.json"
output_path = os.path.join(output_dir, filename)

# Save the cleaned data to a new JSON file in the outputs/final_jsons folder with the current date and time appended to the filename
with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=4)


# Print the output list as a JSON string
print(json.dumps(output_data, indent=4))