from astroquery.jplhorizons import Horizons
from numpy import pi
dates = []
i = 0
date = 2450634.183786772
while i <2:
    dates.append(date)
    date += 1
    i += 1


location = {'lon' : 149.066111, 'lat' : -31.2768056, 'elevation': 1.1645}
# obj = Horizons(id='2018 AJ12', location=location, epochs=dates, id_type='id')
# obj = Horizons(id='Ceres', location=location, epochs=dates, id_type='id')
obj = Horizons(id='2009 FD', location=location, epochs=dates, id_type='id')

# eph = obj.ephemerides(quantities='1,9,36', get_raw_response=True, refsystem='B1950').split("\n")
eph = obj.ephemerides(quantities='1,9,36', get_raw_response=True, refsystem='B1950')
print(eph)

with open("text.txt", "w") as test_file:
    for line in eph:
        test_file.write("\n{}".format(line))


for i in range(0,len(eph)):
    if "$$SOE" in eph[i]:
        lower_bound = i
    if "$$EOE" in eph[i]:
        upper_bound = i
        data_points = eph[lower_bound + 1: upper_bound]
        break
# print (data_points)
uncertainties = []
for i in range(0, len(data_points)):
    uncertainties.append([float(data) for data in data_points[i].split(",")[8:10]])
    data_points[i] = [(float(data) * pi / 180) for data in data_points[i].split(",")[4:7]]
# print (data_points)
print (uncertainties)


# string = '000204'
# year = float("20" + string[0:2])
# month = float(string[2:4])
# day  = float(string[4:6])
# print (year, month, day)




