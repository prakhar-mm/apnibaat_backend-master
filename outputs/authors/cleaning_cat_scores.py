import json
input_path = 'outputs/authors/category_scores.json'

new_data = {}

with open(input_path) as f:
    data = json.load(f)

# for name,tags in data.items():
#     # print(name)
#     data = {}
#     for keys in tags:
#         if(tags[keys] != 0):
#             # print(keys, tags[keys], end=" ")
#             data[keys] = tags[keys]
#     # print(data)
#     new_data[name] = data

# print(new_data)
with open('outputs/authors/cleaned_author_category_scores.json', 'w') as f:
    json.dump(data, f, indent=4)