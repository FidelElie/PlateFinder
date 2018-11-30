import ephem

MM_PER_RADIANS =  1 / ((67.12 / 3600.0) * (ephem.pi / 180.0))

def convert_to_jul(date, time = None):
    """Creates a Dublin Julian Date object"""
    if time != None:
        date = date + " " + time
    dublin_julian_date = ephem.Date(date)
    return dublin_julian_date

def standard_julian(dublin_julian_date):
    """Converts Dublin Julian Dates To Standard"""
    return (float(dublin_julian_date) + 2415020.0)

def manipulate_string(string ,identifier):
    """Manipulates String Into Standard Formats"""
    if identifier == "angle:ra":
        tenths_of_minute = string[-1]
        seconds = tenths_to_seconds(tenths_of_minute)
        string = string[0:4] + str(seconds)

    elif identifier == "angle:dec":
        string = string + "00"

    elif identifier  == "date":
        if string[0] == "0":
            string = "20" + string
        else:
            string = "19" + string
    formatted_string = standard_format(string, identifier)
    return formatted_string

def convert_to_hours(angle):
    """Convert to To pyEphem Hours Object"""
    return ephem.hours(angle)

def convert_to_deg(angle):
    """Convert To PyEphem Degrees Object"""
    return ephem.degrees(angle)

def tenths_to_seconds(tenths_ofa_minute):
    """Converts tenths of a minute to seconds"""
    minutes = float(tenths_ofa_minute) / 10.0
    time_in_seconds = minutes * 60
    return time_in_seconds

def degrees_to_rads(degrees):
    return (float(degrees) * (use_pi() / 180))

def standard_format(string, identifier):
    """Creates Standard String Formats for Different Units"""
    mod_string = []
    for i in range(0, len(string)):
        if (i == 2 or i == 4) and identifier == "angle:ra":
            mod_string.append(":")
        elif (i == 3 or i == 5) and identifier == "angle:dec":
            mod_string.append(":")
        elif (i == 4 or i == 6) and identifier == "date":
            mod_string.append("/")
        mod_string.append(string[i])
    formatted_string = "".join(mod_string)
    return formatted_string

def hms_to_dhours(number):
    """Converts H:M:S to decimal hours"""
    number = number.replace(":","")
    if " " in number:
        mod_numb = []
        for i in range(0, len(number)):
            if number[i] == " ":
                mod_numb.append("0")
            else:
                mod_numb.append(number[i])
        number = "".join(mod_numb)
    minutes = (float(number[2:4])) / 60.0
    seconds = None
    if len (number) > 4:
        seconds = (float(number[4:6])) / 3600
    if float(number[0:2]) == 0.0:
        total = minutes
    else:
        hours = float(number[0:2])
        total = hours + minutes
    if seconds != None:
        total += seconds
    return total

def dhours_to_hms(number):
    """Function to convert decimal hours to H:M:S"""
    number = str(number).split(".")
    minutes = float("0." + number[1]) * 60.0
    minutes = str(minutes).split(".")
    seconds = float("0." + minutes[1]) * 60.0
    if int(number[0]) < 10.0:
        number[0] = "0" + number[0]
    if int(minutes[0]) < 10.0:
        minutes[0] = "0" + minutes[0]
    string = "{}:{}:{}".format(number[0], minutes[0], float(seconds))
    return string


def change_uncertainties(uncertainties):
    """Converts uncertainties from arcseconds to mm"""
    for i in range(0, len(uncertainties)):
        if uncertainties[i][0] != "":
            ra_uncertainty = (float(uncertainties[i][0]) / 3600) * (use_pi()/ 180)
            x_uncertainty = ra_uncertainty * MM_PER_RADIANS
            uncertainties[i][0] = str(round(x_uncertainty, 1))
        if uncertainties[i][1] != "":
            dec_uncertainty = (float(uncertainties[i][1]) / 3600) * (use_pi()/ 180)
            y_uncertainty = dec_uncertainty *  MM_PER_RADIANS
            uncertainties[i][1] = str(round(y_uncertainty, 1))
    return uncertainties

def angle_to_mm(xi, eta, plate_size_in_mm = 355.0):
    """Calcualtes x coordinate and y coordinate in mm of the object on
    the plate"""
    x_coordinate = MM_PER_RADIANS * xi
    y_coordinate = MM_PER_RADIANS * eta
    if x_coordinate < 0.0 or x_coordinate > 0.0:
        x_coordinate = (plate_size_in_mm / 2.0) + x_coordinate
    else:
        x_coordinate = plate_size_in_mm / 2.0
    if y_coordinate < 0.0 or y_coordinate > 0.0:
        y_coordinate = (plate_size_in_mm / 2.0) + y_coordinate
    else:
        y_coordinate = plate_size_in_mm / 2.0
    return [round(x_coordinate, 1), round(y_coordinate, 1)]

def angles_to_str(ra, dec):
    """Places right ascension and declination into a string for web"""
    ra, dec = ra.replace(":", " "), dec.replace(":", " ")
    full_string = ra + " " + dec
    return full_string

def use_pi():
    """Return Pi Value"""
    return ephem.pi

if __name__ == '__main__':
    pass
