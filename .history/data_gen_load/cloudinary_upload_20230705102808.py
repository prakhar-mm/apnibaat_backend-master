#working
import os
import json
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Now you can access the keys in .env as environment variables
openai_key = os.getenv('OPENAI_KEY')


import sys
sys.path.append('./')
import keys.ekeys as key

os.environ["CLOUDINARY_CLOUD_NAME"] = key.cloud_name
os.environ["CLOUDINARY_API_KEY"] = key.cloud_api_key
os.environ["CLOUDINARY_API_SECRET"] = key.cloud_api_secret


cloudinary_cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"]
cloudinary_api_key = os.getenv["CLOUDINARY_API_KEY"]
cloudinary_api_secret = os.getenv["CLOUDINARY_API_SECRET"]


# Set up your Cloudinary credentials
cloudinary.config(
    cloud_name=cloudinary_cloud_name,
    api_key=cloudinary_api_key,
    api_secret=cloudinary_api_secret,
)

# Load input JSON data
with open("./outputs/json_with_img_path/article_data_imageUrl_slug.json", "r") as f:
    input_data = json.load(f)

# Initialize the dictionary to store image URLs
uploaded_image_urls = {}

# Load existing image URLs from the JSON file if it exists
if os.path.exists("./outputs/json_with_img_urls/image_urls.json"):
    with open("./outputs/json_with_img_urls/image_urls.json", "r") as f:
        uploaded_image_urls = json.load(f)

# ... (rest of the code remains the same)

for category, articles in input_data.items():
    for article_name, article_data in articles.items():
        local_image_path = article_data['Image_url']
        image_file = os.path.basename(local_image_path)

        # Check if the image URL already exists in the JSON file
        if image_file in uploaded_image_urls:
            print(f"URL for {image_file} already exists. Skipping.")
            cloudinary_url = uploaded_image_urls[image_file]
        else:
            try:
                # Upload the image to Cloudinary
                response = cloudinary.uploader.upload(local_image_path)

                # Store the uploaded image URL in the dictionary
                cloudinary_url = response['url']
                uploaded_image_urls[image_file] = cloudinary_url
            except Exception as e:
                print(f"Failed to upload {image_file}: {e}")
                cloudinary_url = "NA"

        # Replace the local image path with the Cloudinary URL or "NA"
        article_data['Image_url'] = cloudinary_url

# ... (rest of the code remains the same)

# Save the updated JSON data to a new file
output_directory = os.path.join(os.getcwd(), "./outputs/json_with_img_url")
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
filename = "article_data_with_cloudinary_urls.json"
filepath = os.path.join(output_directory, filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(input_data, f, ensure_ascii=False, indent=4)

# Save the image URLs to a JSON file
with open("./outputs/json_with_img_url/image_urls.json", "w") as f:
    json.dump(uploaded_image_urls, f, indent=4)

print("All images have been uploaded to Cloudinary and the input JSON has been updated.")
