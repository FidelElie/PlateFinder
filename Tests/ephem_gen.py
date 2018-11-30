import ephem

ceres = "1 Ceres,e,10.5935,80.3099,73.1153,2.767046,0.2141309,0.07553468,352.2305,03/23.0/2018,2000,H 3.34,0.12"

gatech = ephem.Observer()
gatech.epoch = ephem.B1950
gatech.lon = '149.066111'
gatech.lat = '-31.2768056'
gatech.pressure = 0
date = ephem.Date(35614.18378677219)
# print (date)
date2 = date + 2415020
print (date2)
gatech.date = date
gatech.date -= ephem.delta_t() * ephem.second
test = ephem.readdb(ceres)
test.compute(gatech)

print (test.a_ra, test.a_dec)
