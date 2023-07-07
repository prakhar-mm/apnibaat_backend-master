#working good
from img_fun import generate_sentence
from img_fun import generate_random_image
from PIL import Image
import json
import os
from slugify import slugify
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

# Get the path of the script and create the "images" subfolder within it
script_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(script_path, "../outputs/images")
if not os.path.exists(images_path):
    os.mkdir(images_path)

def get_latest_file(directory):
    files = os.listdir(directory)
    if not files:
        return None

    # Get the latest modified file
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

def analyze_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Remove stopwords and punctuations
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]

    # Frequency Distribution
    freq_dist = nltk.FreqDist(tokens)

    # Get the top 3 most common keywords
    keywords = [word for word, count in freq_dist.most_common(3)]
    keywords_str = ', '.join(keywords)  # Convert the list of keywords into a comma-separated string

    # Named Entity Recognition
    named_entities = ne_chunk(pos_tag(word_tokenize(text)))

    # Check if the text is about people
    is_about_people = any(chunk.label() == 'PERSON' for chunk in named_entities if hasattr(chunk, 'label'))

    return keywords_str, is_about_people


# Open the JSON file
directory_path = './outputs/content/'
latest_content_json = get_latest_file(directory_path)
with open(latest_content_json) as f:
    data = json.load(f)

new_data = {}  # create a new dictionary to store the updated article data

for topic, article_data in data.items():
    title = article_data["title"]
    if not title:  # ignore articles with missing titles
        continue    

    slug = slugify(title)
    image_filename = f"{slug}.png"
    image_path = os.path.join(images_path, image_filename)

    if os.path.exists(image_path):
        print(f"Image for article {topic} already exists. Skipping.")
        image_url = os.path.join(images_path, image_filename)
        image_url = os.path.abspath(image_url)
        article_data.update({"Image_url": image_url, "Slug": slug})
        new_data[topic] = article_data
        continue

    content = article_data["content"]
    keywords = article_data["keywords"]
    ArticleAboutPeople = article_data["ArticleAboutPeople"]
    image_idea = article_data["image_idea"]
    
    
    try:
        generated_sentence = generate_sentence(image_idea, keywords, ArticleAboutPeople)
        #print(generated_sentence)

        image_source = generate_random_image(generated_sentence, image_filename, images_path)
        image_url = os.path.join(images_path, image_filename)

        #print(image_url)
        #image = Image.open(image_url)
        #st.image(image)
        #image.show()

        article_data.update({"Image_url": image_url, "Slug": slug, "Image_source": image_source})
        new_data[topic] = article_data

    except Exception as e:
        print(f"Failed on topic {topic}: {e}")

# Save the new JSON data to a file
output_directory = './outputs/json_with_img_path'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
filename = 'article_data_imageUrl_slug.json'
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
