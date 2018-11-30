import os
import numpy as np
from tqdm import tqdm

plate_file_directory = os.path.abspath("Plate Files")
plate_file_names = os.listdir(plate_file_directory)

if len(plate_file_names) == 0:
    raise Exception("No Plate Files Present, Please Download Some")

print ("Plate Catalogues to choose from:")
for i in range(0, len(plate_file_names)):
    print ("{}. {}".format(i+ 1, plate_file_names[i]))
    with open(os.path.join(plate_file_directory, plate_file_names[i]), "r") as file_ob:
        print (file_ob.readline().replace("\n",""))

while True:
    # chosen_file = int(input("Input Number corresponding to chosen file 1 to {}: ".format(len(plate_file_names))))
    chosen_file = 1
    if chosen_file < 1:
        print ("Please Enter A Valid Number Between 1 and {}".format(len(plate_file_names)))
    elif chosen_file > len(plate_file_names):
        print ("Please Enter A Valid Number Between 1 and {}".format(len(plate_file_names)))
    try:
        int(chosen_file)
    except ValueError:
        print ("Please enter a valid answer")
    else:
        with open(os.path.join(plate_file_directory, plate_file_names[chosen_file - 1]), "r") as plate_file:
            file_width  = []
            mod_file = []
            x = plate_file.readlines()
            x = [x[i].replace("\n","") for i in range(0, len(x))]
            del x[0]
            for i in range(0, len(x)):
                file_width.append(len(x[i].split()))
            print("Converting Values...")
            for i in tqdm(range(0, len(x))):
                x[i] = x[i].split()
                while len(x[i]) < max(file_width):
                    x[i].append("NULL")
                mod_file.append("  ".join(x[i]))
        with open(os.path.join(plate_file_directory, plate_file_names[chosen_file - 1]), "w") as plate_file:
            for i in range(0, len(mod_file)):
                plate_file.write("{}\n".format(mod_file[i]))

        plate_data = np.genfromtxt(os.path.join(plate_file_directory, plate_file_names[chosen_file - 1]), skip_header=1, 
        dtype=str, filling_values="NULL", missing_values="")
        break


