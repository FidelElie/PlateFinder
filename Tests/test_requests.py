import requests
import os
from tqdm import tqdm

"""
Code block for downloading plate file data
"""

file_directory = os.path.abspath("External")
save_local = os.path.abspath("Plate Files")
file_name = "PlateFileLocals.txt"
if len(os.listdir(save_local)) == 0:
    print("Downloading Plate Files")
    with open(os.path.join(file_directory, file_name)) as plate_file_locals:
        file_data = plate_file_locals.readlines()
        plate_file_titles = [file_data[i].replace("\n","") for i in range(0, len(file_data), 2)]
        plate_file_urls = [file_data[i].replace("\n","") for i in range(1 , len(file_data), 2)]
    for i in range(0, len(plate_file_urls)):
        save_file_name = "{}".format(plate_file_urls[i].split("/")[-1].replace(".lis",".txt"))
        try:
            r = requests.get(plate_file_urls[i], allow_redirects=True)
        except ConnectionError:
            print ("Connection Error : Download of file {} failed".format(save_file_name[i]))
        except TimeoutError:
            print ("Timeout Error: Download of file {} failed".format(save_file_name[i]))
        print ("Downloading Plate Catalog: {}. {}".format(i+1, save_file_name))
        with open(os.path.join(save_local, save_file_name), "w") as save_file:
            save_file.write("{}\n".format(plate_file_titles[i]))
            for data in tqdm(r.text):
                save_file.write(data)
    print ("All Catalogues Downloaded")
else:
    print ("All files have already been downloaded")