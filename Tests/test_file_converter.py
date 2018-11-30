import os
import numpy as np
from tqdm import tqdm

def main():

    plate_file_directory = os.path.abspath("Plate Files")
    plate_file_names = os.listdir(plate_file_directory)

    while True:
        convert_files = input("Convert Files?: ").lower()
        # convert_files = "yes"
        if convert_files == "yes" or convert_files == "y":
            for files in range(0, len(plate_file_names)):
                print ("Converting File: {}. {}".format(files + 1, plate_file_names[files]))
                with open(os.path.join(plate_file_directory, plate_file_names[files]), "r") as plate_file:
                   file_width  = []
                   mod_file = []
                   x = plate_file.readlines()
                   x = [x[i].replace("\n","") for i in range(0, len(x))]
                   del x[0]
                   for i in range(0, len(x)):
                       file_width.append(len(x[i].split()))
                   print("Converting Values....")
                   for i in tqdm(range(0, len(x))):
                       x[i] = x[i].split()
                       while len(x[i]) < max(file_width):
                           x[i].append("NULL")
                       mod_file.append("  ".join(x[i]))
                with open(os.path.join(plate_file_directory, plate_file_names[files]), "w") as plate_file:
                    for i in range(0, len(mod_file)):
                        plate_file.write("{}\n".format(mod_file[i]))
            break
        elif convert_files == "no" or convert_files == "n":
            print ("Nothing Will Be Downloaded")
            break
        else:
            print ("Please enter a valid answer of 'Yes/Y' or 'No/N'")
main()
    