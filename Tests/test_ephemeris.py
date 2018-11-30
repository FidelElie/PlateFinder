import os
import numpy as np
from ephem import *

external_directory = os.path.abspath("External")
standard_bodies_file_name = "StandardBodies.txt"

standard_bodies = np.genfromtxt(os.path.join(external_directory, standard_bodies_file_name),
skip_header=1, dtype=str)

for i, name in enumerate(standard_bodies, 1):
    print ("{}. {}".format(i, name))


