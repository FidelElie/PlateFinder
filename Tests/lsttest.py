import ephem

gatech = ephem.Observer()
gatech.lon = '149.0'
# gatech.lat = -34
gatech.date = "1977/2/13 17:00:35"
gatech.epoch = '1950'

print (gatech)


