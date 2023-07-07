
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import os

# Replace this path with the path to your Service Account Key JSON file
service_account_key_file = './keys/firebase/custom-defender-377912-firebase-adminsdk-d5npo-f88dcc4a57.json'

# Initialize the Firebase app if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_key_file)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://custom-defender-377912-default-rtdb.asia-southeast1.firebasedatabase.app/'  # Replace 'your-project-id' with your actual Firebase project ID
    })


post_data = {
    'author_name': 'author_name',
    'author_desg': 'author_desg',
    'author_bio': 'author_bio',
    'cate': 'cate',
    'cate_bg':'',
    'content': 'content',
    'date': 'date',
    'excerpt': 'excerpt',
    'feature_image': 'featureImg',
    'post_views': 'post_views',
    'post_share': 'post_share',
    'post_format': 'postFormat',
    'quote_text': 'quoteText',
    'slug': 'slug',
    'summary' : 'summary',
    'title': 'title',
    'trending': 'trending',
}


# Write data to your Realtime Database
#db.reference('/posts/').set(post_data)

# Load your JSON data from a file
# with open("./outputs/final_jsons/output_2023-06-12_17-36-06.json", "r") as file:
#     data = json.load(file)
def get_latest_file(directory):
    files = os.listdir(directory)
    if not files:
        return None

    # Get the latest modified file
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

# Example usage
directory_path = './outputs/final_cleaned_json'
latest_file_path = get_latest_file(directory_path)
with open(latest_file_path, "r", encoding='utf-8') as file:
    eng_data = json.load(file)

latest_file_path = get_latest_file('./outputs/translated')
with open(latest_file_path, "r", encoding='utf-8') as file:
    hi_data = json.load(file)
# set the path
path = '/posts'
# Push the data to your Firebase Realtime Database
def push_eng():
    ref = db.reference(f'{path}/English')
    ref.push(eng_data)

def push_hi():
    ref = db.reference(f'{path}/Hindi')
    ref.push(hi_data)

def del_content(ind):
    if ind == None : return

    ref = db.reference(f'/test/{ind}')
    ref.delete()
# ref = db.reference('/posts')
# ref.delete()
# ref.push(data)
# for i in range(0,200):
#     ref = db.reference(f'/posts/{i}')
#uncomment below to delete a part
#be extra careful
    # ref.delete()


    # ref.push(data)
# del_content()

push_eng()
push_hi()

print("Data uploaded successfully")