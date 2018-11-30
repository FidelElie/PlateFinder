import ephem
import numpy as np

gatech = ephem.Observer()
# print(dir(gatech))
gatech.lat = '-31.2666667'
gatech.lon = '149.066667'
# gatech.lat = "-31"
# gatech.lon = "149"
gatech.epoch = ephem.B1950
gatech.date = "2018/03/10 00:00:00"
gatech.elev = 1185.1
mars = ephem.Mars(gatech)

print(mars.a_ra.norm, mars.a_dec.znorm)

