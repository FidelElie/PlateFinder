import numpy as np
class Sorter(object):
    """Class For Sorting And Error"""
    def __init__(self, plate_string):
        self.plate_string = plate_string
        self.plate_numb = plate_string[2:7]
        self.ra_and_dec = plate_string[20:30]
        self.date_of_exp = plate_string[30:36]
        self.time_of_exp = plate_string[36:40]
        self.exp_duration = plate_string[52:56]
        # self.qual_control = plate_string[56:61]
        self.plate_data = self.set_plate_data()
    
    def set_plate_data(self):
        return [self.plate_numb, self.ra_and_dec, self.date_of_exp, 
        self.time_of_exp, self.exp_duration]

    def check_invalid_entries(self):
        suitability = True
        for i in range(len(self.plate_data)):
            if len(self.plate_data[i].strip()) == 0:
                suitability = False
        return suitability

    # def check_plate_quality(self):
    #     suitability = True
    #     if self.qual_control[0] != "A" or "B" or "C":
    #         suitability = False
    #     return suitability

    def return_plate_data(self):
        return self.plate_data

class Converter(Sorter):
    def __init__(self, latitude, longitude, plate_data):
        self.latitude = latitude
        self.longitude = longitude
        self.plate_data = plate_data

    def convert(self):
        self.gst_to_ut()
        self.ten_of_min_to_s()
        self.equi_change()
        return self.plate_data

    def gst_to_ut(self):
        s = self.ut_date_jul(self.plate_data[2]) - 2451545.0
        t = s / 36525.0
        t0 = 6.697374558 + (2400.051 * t) + (0.000025862 * pow(t, 2))
        time_in_dhours = self.lst_to_gst(self.plate_data[3])
        time_in_dhours -= t0
        if time_in_dhours > 24:
            while time_in_dhours > 24:
                time_in_dhours -= 24
        elif time_in_dhours < 0:
            while time_in_dhours < 0:
                time_in_dhours += 24
        time_in_dhours = time_in_dhours * 0.9972695663
        self.plate_data[3] = time_in_dhours

    def ut_date_jul(self, date):
        year = int(date[0:2])
        month = int(date[2:4])
        day = int(date[4:6])
        if month == 1 or month == 2:
            year -= 1 
            month += 12 
        a = year / 100
        b = 2 - a + a / 4
        if year < 0:
            c = 365.25 * year - 0.75
        else:
            c  = 365.25 * year
        d  = 30.6601 * (month + 1)
        julian_date = b + c + d + day + 1720994.5
        return julian_date

    def lst_to_gst(self, time):
        time = self.hms_to_dhours(time)
        longitude_in_h = self.longitude / 15
        time -= longitude_in_h
        if time > 24:
            time -= 24
        elif time < 0:
            time += 24
        return time

    def ten_of_min_to_s(self):
        self.plate_data[4] = float(self.plate_data[4]) * 60

    def hms_to_dhours(self, number):
        number = number.replace(":","")
        minutes = float(number[2:4]) / 60
        if len(number[0:2].strip()) == 0: 
            total = minutes
        else:
            hours = float(number[0:2])
            total = hours + minutes
        if len(number) > 5:
            total += float(number[4:len(number)])
        if number[0:2][0] == " ":
            total += 12 
        return total
    
    def dhours_to_hms(self, number):
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

    def equi_change(self):
        m, n, n_prime = 3.07420, 1.33589, 20.0383 / 3600 * (np.pi / 180)
        ut_year = "19" + self.plate_data[1][0:2]
        if "-" in self.plate_data[1]:
            split_data = self.plate_data[1].split("-")
            right_ascension, declination = split_data[0], "-" + split_data[1] 
        elif "+" in self.plate_data[1]:
            split_data = self.plate_data[1].split("+")
            right_ascension, declination = split_data[0], "+" + split_data[1]
        elif " " in self.plate_data[1]:
            split_data = self.plate_data[1].split(" ")
            right_ascension, declination = split_data[0], "+" + split_data[1]
        N = float(ut_year) - 1950
        right_ascension = self.change_ra(right_ascension) 
        declination = self.change_dec(declination)
        x = (((m + n * np.sin(right_ascension) * np.tan(declination)) * N) / 3600) * 15 * (np.pi/180)
        right_ascension = right_ascension + x
        declination = declination + (n_prime * np.cos(right_ascension)) * N
        self.plate_data[1] = [right_ascension, declination]

    def change_ra(self, right_ascension):
        hours = int(right_ascension[0:2])
        minutes = int(right_ascension[2:4]) / 60
        seconds = int(right_ascension[4:len(right_ascension)]) / 3600 
        total_radians = ((hours + minutes + seconds) * 15) * (np.pi / 15)
        return total_radians

    def change_dec(self, declination):
        degrees = int(declination[0:3])
        arc_seconds_in_deg = (int(declination[3:5]) / 3600)
        total_radians = (degrees + arc_seconds_in_deg) * (np.pi / 15)
        return total_radians

if __name__ == '__main__':
    sorter = Sorter("UJ 3684P P1 112  41602410-3000771017 343IIIaJ NONE   700AI3  1N")
    entries_s = sorter.check_invalid_entries()
    quality_s = sorter.check_plate_quality()
    if entries_s == False:
        print ("Plate Not Suitable: Missing Data") # break loop here
    elif entries_s == False:
        print ("Plate Not Suitable: Quality Is Too Low") # break loop here
    else:
        plate_data = sorter.return_plate_data()
        plate_data = Converter(-31, 149, plate_data).convert()
