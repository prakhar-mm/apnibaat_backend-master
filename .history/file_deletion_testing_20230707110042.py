import os
import glob

# Get a list of all the file paths that ends with .json in specified directory and its subdirectories
file_list = glob.glob('outputs/images/**/*.json', recursive=True)

# Iterate over the list of filepaths & remove each file.
for filePath in file_list:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)
