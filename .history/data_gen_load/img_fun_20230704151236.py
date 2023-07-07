#import spacy
from collections import Counter

# Load the Spacy model
#nlp = spacy.load("en_core_web_sm")





# Image styling module
styles_dict = {
    # 1: "16-Bit",
    # 2: "1800s",
    # 3: "1980s",
    # 4: "4-Bit",
    # 5: "8-Bit",
    # 6: "Amber",
    # 7: "Anatomical Drawing",
    # 8: "Ancient",
    # 9: "Anime",
    # 10: "Antimatter",
    10: "3D Model",
    11: "Arabic",
    12: "Black Hole",
    13: "Realistic",
    14: "Oil painting",
    15: "Concept art"
    
}

lighting_dict = {
    1: "Accent Lighting",
    2: "Backlight",
    3: "Blacklight",
    4: "Blindinglight",
    5: "Candlelight",
    6: "Concert Light",
    7: "Crepuscular Rays",
    8: "Direct Sunlight",
    9: "Dusk",
    10: "Edison Bulb",
    11: "Electric Arc",
    12: "Fire"
}

camera_dict = {
    1: "360 Panorama",
    2: "DSLR",
    3: "Electron Microscope",
    4: "Macro lens",
    5: "Magnification",
    6: "Microscopy",
    7: "Miniature Faking",
    8: "Panorama",
    9: "Pinehole lens",
    10: "Satellite Imagery",
    11: "Super resolution microscopy",
    12: "Telephoto lens"
}

artists_dict = {
    1: "John Singer Sargent",
    2: "Edgar Degas",
    3: "Paul Cézanne",
    4: "Jan van Eyck",
    5: "Leonardo DaVinci",
    6: "Vincent Van Gogh",
    7: "Johannes Vermeer",
    8: "Rembrandt",
    9: "Albrecht Dürer",
    10: "Leonardo da Vinci",
    11: "Michelangelo",
    12: "Jean-Auguste-Dominique Ingres",
    13: "Thomas Moran",
    14: "Claude Monet",
    15: "Alfred Bierstadt",
    16: "Frederic Edwin Church",
    17: "Alphonse Mucha",
    18: "Andy Warhol",
    19: "Art by Yoko Ono",
    20: "Banksy",
    21: "By Francisco De Goya",
    22: "Caravaggio",
    23: "David Hockney",
    24: "Diego Rivera",
    25: "Eugene Delacroix",
    26: "Francis Bacon",
    27: "Frida Kahlo"
}

color_dict = {
    1: "Amber",
    2: "Baby Blue Color",
    3: "Baby Pink Color",
    4: "Beige",
    5: "Blue",
    6: "Brown color",
    7: "CYMK",
    8: "Citrus",
    9: "Coquelicot color",
    10: "Cyan",
    11: "Gold color",
    12: "Gray"
}

material_dict = {
    1: "Aluminium",
    2: "Brick",
    3: "Bronze",
    4: "Carbon Fibre",
    5: "Cardboard",
    6: "Cellulose",
    7: "Ceramic",
    8: "Cotton",
    9: "Fabric",
    10: "Fiber Optic",
    11: "Foil",
    12: "Gasoline"
}


import random

def pick_random_style(styles):
    random_key = random.choice(list(styles.keys()))
    random_style = styles[random_key]
    return f"{random_style}"

def is_text_about_people(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return True
    return False

def generate_sentence(title,keywords,ArticleAboutPeople):
    random_style = pick_random_style(styles_dict)
    random_lighting = pick_random_style(lighting_dict)
    random_camara = pick_random_style(camera_dict)
    random_artist = pick_random_style(artists_dict)
    random_color = pick_random_style(color_dict)
    random_material = pick_random_style(material_dict)
    #keywords_array = extract_keywords(text)
    keyword=keywords
    best_sentence = title
    #ArticleAboutPeople=is_text_about_people(text)

    Prompt1 = f"{title}. {best_sentence}. Emphasize {keyword}, realistic and {random_style}, Lighting:{random_lighting}, Camara:{random_camara}, Material:{random_material}"
    Prompt2 = f"{title}. {best_sentence}. Emphasize {keyword}, If using faces use Indian/North Indian/East Indian faces, realistic and human resembling, avoid using hands, skintone can vary from white to brown,Style: {random_style}, Lighting:{random_lighting}, Camara:{random_camara},  Material:{random_material}"
    #ArticleAboutPeople=is_text_about_people(Prompt1)
    # print(f"ArticleAboutPeople: {ArticleAboutPeople}")
    if ArticleAboutPeople == True:
        return Prompt2
    return Prompt1

# Usage
# title ="How to get a good deal on a new car."
# text="""Most people don't enjoy haggling over the price of a new car. However, if you're armed with the right information, you can get a great deal on your new car. Here are a few tips to help you get the best possible price on a new car:\n\n1. Do your research.\n\nBefore you even step foot in a dealership, you should have a good idea of what kind of car you want and what it's worth. Use online resources to research the true market value of the car you're interested in. This will give you a starting point for negotiating with the dealer.\n\n2. Get multiple quotes.\n\nOnce you know what kind of car you want, get quotes from several dealerships. This will help you get a sense of what the going rate is for the car you're interested in.\n\n3. Be willing to walk away.\n\nIf the dealer isn't willing to meet your price, be prepared to walk away. There are plenty of other dealerships out there, and you shouldn't settle for a car that's overpriced.\n\n4. Don't be afraid to haggle.\n\nMost dealerships are willing to negotiate on price. So, don't be afraid to haggle a bit to get the best possible price.\n\n5. Get the car in writing.\n\nOnce you and the dealer have agreed on a price, make sure to get the car's price in writing. This will help to avoid any misunderstandings later on.\n\nBy following these tips, you can get a great deal on your new car. Just remember to do your research and be willing to walk away if the dealer isn't willing to meet your price."""
# generated_sentence = generate_sentence(title,text)


# print(generated_sentence)


import os
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

import sys
sys.path.append('./')
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Now you can access the keys in .env as environment variables

os.environ['STABILITY_HOST'] = os.getenv('STABILITY_HOST')
os.environ['STABILITY_KEY'] = os.getenv('STABILITY_KEY')

stability_api = client.StabilityInference(
    key=os.getenv('STABILITY_KEY'),
    verbose=True,
    engine="stable-diffusion-xl-1024-v0-9",
)

def generate_image_dream_studio(prompt, output_name, output_folder=None, engine_id="stable-diffusion-xl-1024-v0-9", width=512, height=512):
    answers = stability_api.generate(
        prompt=prompt,
        steps=50,
        cfg_scale=8.0,
        width=width,
        height=height,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )
    
    for answer in answers:
        result_image_data = answer.artifacts[0].binary

    img = Image.open(io.BytesIO(result_image_data))
    # img.show()
    
    # upscale the image to double its size
    upscaled_img = img.resize((img.size[0]*2, img.size[1]*2))
    # upscaled_img.show()

    # Save the upscaled image to a file
    if output_folder is not None:
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_name)
    else:
        output_path = output_name
    upscaled_img.save(output_path)


import requests
# from PIL import Image
# import io
import json
import time
import os

# os.environ["LEONARDO_API_KEY"] = key.leonardo_key
# apikey = os.environ["LEONARDO_API_KEY"]

# def generate_image_leonardo_creative(prompt, output_name, output_folder=None):
#     url = "https://cloud.leonardo.ai/api/rest/v1/generations"

#     payload = {
#         "prompt": prompt,
#         "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
#         #"modelId": "f3296a34-9aef-4370-ad18-88daf26862c3",
        
#         "width": 768,
#         "height": 768,
#         "sd_version": "v2",
#         "num_images": 1,
#         "num_inference_steps": 30,
#         "guidance_scale": 7,
#         "presetStyle": "LEONARDO",
#         # "tiling": True,
#         # "public": True,
#         "promptMagic": True
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "authorization": f"Bearer {apikey}"
#     }

#     # First API call: POST request to start image generation
#     response = requests.post(url, json=payload, headers=headers)
#     response_json = json.loads(response.text)

#     generation_id = response_json["sdGenerationJob"]["generationId"]

#     # Build the URL with the base URL and the generationId
#     base_url = "https://cloud.leonardo.ai/api/rest/v1/generations/"
#     url_with_generation_id = f"{base_url}{generation_id}"

#     # Poll the API until the status is "COMPLETE"
#     while True:
#         response = requests.get(url_with_generation_id, headers=headers)
#         response_json = json.loads(response.text)

#         status = response_json["generations_by_pk"]["status"]
        
#         if status == "COMPLETE":
#             break
#         else:
#             time.sleep(5)  # Wait for 5 seconds before checking again

#     # Second API call: GET request to get the generated image URL
#     image_url = response_json["generations_by_pk"]["generated_images"][0]["url"]

#     # Make a GET request to download the image
#     response_image = requests.get(image_url)
#     img = Image.open(io.BytesIO(response_image.content))

#     # Save the image to a file
#     if output_folder is not None:
#         os.makedirs(output_folder, exist_ok=True)
#         output_path = os.path.join(output_folder, output_name)
#     else:
#         output_path = output_name
#     img.save(output_path)

import random

def generate_random_image(prompt, output_name, output_folder=None, choice=None):
    functions = [
            #generate_image_leonardo_creative, 
            generate_image_dream_studio,
            generate_image_dream_studio
        ]

    # Randomly select a function
    # choice = 0, 1, None
    if not choice:
        selected_function = random.choice(functions)
    else:
        selected_function = functions[choice]

    try:
        # Call the selected function
        selected_function(prompt, output_name, output_folder)

        # Return the name of the selected function
        return selected_function.__name__
    except Exception as e:
        print(f"Failed with {selected_function.__name__}: {e}")

        # Choose the other function as a fallback
        fallback_function = [func for func in functions if func != selected_function][0]
        
        print(f"Trying fallback function {fallback_function.__name__}")
        try:
            # Call the fallback function
            fallback_function(prompt, output_name, output_folder)

            # Return the name of the fallback function
            return fallback_function.__name__
        except Exception as e:
            print(f"Failed with fallback function {fallback_function.__name__}: {e}")
            return None
