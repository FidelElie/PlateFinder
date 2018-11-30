import ephem
import math

julian_date = "2009/06/19 18:00:00"
print(float(ephem.Date(julian_date)) + 2415020.0)
