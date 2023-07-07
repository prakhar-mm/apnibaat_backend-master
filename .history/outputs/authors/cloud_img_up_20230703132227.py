#working
import os
import json
import cloudinary
import cloudinary.uploader

os.environ["CLOUDINARY_CLOUD_NAME"] = "dltay5uwr"
os.environ["CLOUDINARY_API_KEY"] = "724776332525466"
os.environ["CLOUDINARY_API_SECRET"] = "h7MkFRWg4uf_L5tUl-0aLHW_TiE"


cloudinary_cloud_name = os.environ["CLOUDINARY_CLOUD_NAME"]
cloudinary_api_key = os.environ["CLOUDINARY_API_KEY"]
cloudinary_api_secret = os.environ["CLOUDINARY_API_SECRET"]


# Set up your Cloudinary credentials
cloudinary.config(
    cloud_name=cloudinary_cloud_name,
    api_key=cloudinary_api_key,
    api_secret=cloudinary_api_secret,
)

# Load input JSON data
with open("./outputs/authors/author_imgs_path.json", "r") as f:
    input_data = json.load(f)

# Initialize the dictionary to store image URLs
uploaded_image_urls = {}

# Load existing image URLs from the JSON file if it exists
if os.path.exists("./outputs/authors/image_urls.json"):
    with open("./outputs/authors/image_urls.json", "r") as f:
        uploaded_image_urls = json.load(f)

# ... (rest of the code remains the same)

for name, tags in input_data.items():
    local_image_path = tags['Image_url']
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
    tags['Image_url'] = cloudinary_url

# ... (rest of the code remains the same)

# Save the updated JSON data to a new file
with open("./outputs/authors/authors.json", "w") as f:
    json.dump(input_data, f, indent=4)

# Save the image URLs to a JSON file
with open("./outputs/authors/image_urls.json", "w") as f:
    json.dump(uploaded_image_urls, f, indent=4)

print("All images have been uploaded to Cloudinary and the input JSON has been updated.")
