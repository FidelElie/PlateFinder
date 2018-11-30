from Libraries.FileHandler import FileHandler
import numpy as np
# file_handler = FileHandler()
# file_handler.plate_dowload()
# plate_data = file_handler.choose_file("Plate Files")
# # print (plate_data[0])
# plate_list = []
# list_length = []

# for i in range(0,len(plate_data)):
#     plate_list.append(plate_data[i])
#     list_length.append(len(plate_list[i]))
# x = plate_list[2822]

# print ("Plate Prefix: {}".format(x[0:2]))
# print ("Plate Number: {}".format(x[2:7])) # important
# print ("Plate Suffix: {}".format(x[7:8])) # maybe important
# # print ("Survey Code: {}".format(x[8:11])) 
# # print ("Non Survey Code : {}".format(x[11:15]))
# # print ("Field Number: {}".format(x[15:20]))
# print ("Ra and Dec: {}".format(x[20:30])) #important
# print ("UT Date of exposure: {}".format(x[30:36])) # important
# print ("Local Sidereal Time of exposure: {}".format(x[36:40])) # important
# # print ("Emulsion: {}".format(x[40:46])) 
# # print ("Filter: {}".format(x[46:52]))
# print ("Exposure TImes In Tenghts of a minute {}".format(x[52:56])) # important
# print ("Qualtiy Control: {}".format(x[56:61])) #maybe important
# # print ("Prism Code: {}".format(x[61:64]))

# print ("\n \n")

# plate_numb = x[2:7]
# plate_suff = x[7:8]
# ra_and_dec = x[20:30]
# ut_date_of_exp = x[30:36]
# loc_sid_time_of_exp = x[36:40]
# exp_times = x[52:56]
# qual_control = x[56:61]

# print (plate_numb)

LAT = -31
LONGITUDE = 149

def gst_to_ut(number):
    s = ut_date_to_jul(number) - 2451545.0
    t = s / 36525.0
    t0 = 6.697374558 + (2400.051 * t) + (0.000025862 * pow(t, 2))
    time_in_dhours = lst_to_gst(number)
    time_in_dhours -= t0
    if time_in_dhours > 24:
        while time_in_dhours > 24:
            time_in_dhours -= 24
    elif time_in_dhours < 0:
        while time_in_dhours < 0:
            time_in_dhours += 24
    time_in_dhours = time_in_dhours * 0.9972695663
    number = time_in_dhours
    return numbers

def ut_date_to_jul(date):
    year = int(date[0:2])
    month = int(date[2:4])
    day = int(date[4:6])
    if month == 1 or month == 2:
        year -= 1
        month += 12
    a = year / 100
    b = 2 - a + a/4
    if year < 0:
        c = 365.25 * year - 0.75
    else:
        c = 365.25 * year
    d = 30.6001 * (month + 1)
    julian_date = b + c + d + day + 1720994.5
    return julian_date

def lst_to_gst(time):
    time = hms_to_dhours(time)
    longitude_in_h = LONGITUDE / 15
    time -= longitude_in_h
    if time > 24:
        time -= 24
    elif time < 0:
        time += 24
    return time

def hms_to_dhours(number):
    print (number)
    number = number.replace(":","")
    minutes = float(number[2:4]) / 60
    hours = float(number[0:2])
    total = hours + minutes
    if len(number) > 5:
        total += float(number[4:len(number)])
    if number[0:2][0] == " ":
        total += 12
    return total

def dhours_to_hms(number):
    number = str(number).split(".")
    minutes = float("0." + number[1]) * 60
    minutes = str(minutes).split(".")
    seconds = float("0." + minutes[0]) * 60
    if int(number[0]) < 10:
        number[0] = "0" + number[0] 
    if int(minutes[0]) < 10:
        minutes[0] = "0" + minutes[0]
    string = "{}:{}:{}".format(number[0], minutes[0], int(seconds))
    return string

def equi_change(ra_and_dec):
    m, n, n_prime = 3.07420, 1.33589, 20.0383 / 3600 * (np.pi / 180)
    ut_year = "19" + ra_and_dec[0:2]
    if "-" in ra_and_dec:
        split_data = ra_and_dec.split("-")
        right_ascension, declination = split_data[0], "-" + split_data[1] 
    elif "+" in ra_and_dec:
        split_data = ra_and_dec.split("+")
        right_ascension, declination = split_data[0], "+" + split_data[1]
    N = float(ut_year) - 1950
    right_ascension = change_ra(right_ascension) 
    declination = change_dec(declination)
    right_ascension = right_ascension + time_to_radians((m + n * np.sin(right_ascension) * np.tan(declination)) * N)
    declination = declination + (n_prime * np.cos(right_ascension)) * N

    return [right_ascension, declination]

def time_to_radians(time):
    time = (time / 3600) * 15 * (np.pi / 180)
    return time

def change_ra(right_ascension):
    hours = int(right_ascension[0:2])
    minutes = int(right_ascension[2:4]) / 60
    seconds = int(right_ascension[4:len(right_ascension)]) / 3600 
    total_radians = ((hours + minutes + seconds) * 15) * (np.pi / 15)
    return total_radians

def change_dec(declination):
    degrees = int(declination[0:3])
    arc_seconds_in_deg = (int(declination[3:5]) / 3600)
    total_radians = (degrees + arc_seconds_in_deg) * (np.pi / 15)
    return total_radians

def ten_of_min_to_s(exp_time):
    exp_time = exp_time * 60 # in seconds
    return exp_time

def check_strings_cont(array):
    for item in array: 
        if len(item.strip()) == 0:
            print ("There is an ivalid data point")
            break 

def strip_whitespace(array):
    for i in range(0, len(array)):
        array[i] = array[i].strip()
    return array

if __name__ == '__main__':
    file_handler = FileHandler()
    file_handler.plate_dowload()
    plate_data = file_handler.choose_file("Plate Files")
    # print (plate_data[0])
    plate_list = []

    for i in range(0,len(plate_data)):
        plate_list.append(plate_data[i])
    x = plate_list[2822]
    # print (x)

    plate_numb = x[2:7]
    ra_and_dec = x[20:30]
    ut_date_of_exp = x[30:36]
    loc_sid_time_of_exp = x[36:40]
    exp_times = x[52:56]
    qual_control = x[56:61]

    array = [plate_numb, ra_and_dec, ut_date_of_exp,
    loc_sid_time_of_exp, exp_times, qual_control]
    # array = strip_whitespace(array)

    check_strings_cont(array)
    hms_to_dhours(array[3])
    array[1] = equi_change(array[1])

    # print (array)
    # array = gst_to_ut(array)
