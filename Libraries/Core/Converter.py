import Libraries.Core.UnitChanger as unit
from Libraries.Core.Sorter import Sorter

class Converter(Sorter):
    """Class to convert plate properties into required formats"""
    def __init__(self, longitude, plate_string):
        Sorter.__init__(self, plate_string)
        self.longitude = longitude
        self.julian_date = None

    def convert(self):
        """Goes throught the conversion prodecure calling methods"""
        self.format_string()
        self.convert_exposure_time()
        suitability = self.gst_to_ut()
        self.create_julian_float()
        self.angle_change()
        return self.julian_date, suitability

    def format_string(self):
        """Formats the date String"""
        self.plate_data[3] = unit.manipulate_string(self.plate_data[3], "date")

    def create_julian_float(self):
        """Creates a Julian FLoat based on the time and date provided"""
        # dub_julian_date = unit.convert_to_jul(
        #     self.plate_data[3], unit.dhours_to_hms(self.plate_data[4]))
        # julian_date = unit.standard_julian(dub_julian_date)
        time = self.plate_data[4] - 12
        day_fraction = time / 12
        dub_julian_date = unit.convert_to_jul(self.plate_data[3])
        julian_date = unit.standard_julian(dub_julian_date) + day_fraction

        self.julian_date = julian_date

    def angle_change(self):
        """Changes the units of the right ascesion and declination"""
        if "-" in self.plate_data[2]:
            split_data = self.plate_data[2].split("-")
            right_ascension, declination = split_data[0], "-" + split_data[1]
        elif "+" in self.plate_data[2]:
            split_data = self.plate_data[2].split("+")
            right_ascension, declination = split_data[0], "+" + split_data[1]
        elif " " in self.plate_data[2]:
            split_data = self.plate_data[2].split(" ")
            right_ascension, declination = split_data[0], "+" + split_data[1]

        right_ascension = unit.manipulate_string(right_ascension, "angle:ra")
        ra = unit.convert_to_hours(right_ascension)
        declination = unit.manipulate_string(declination, "angle:dec")
        dec = unit.convert_to_deg(declination)

        self.plate_data[2] = [ra, dec]

    def gst_to_ut(self):
        """Converts Greenwich Sidereal Time(GST) to Universal Time(UT)"""
        suitability = True
        lst_time = self.plate_data[4]
        ut_date = self.plate_data[3]
        dub_julian_date = unit.convert_to_jul(ut_date)
        julian_date = unit.standard_julian(dub_julian_date)

        s = julian_date - 2451545.0
        t = s / 36525.0
        t0 = 6.697374558 + (2400.051336 * t) + (0.000025862 * (t**2))
        if t0 > 24.0:
            while t0 > 24.0:
                t0 -= 24.0
        elif t0 < 0.0:
            while t0 < 0.0:
                t0 += 24.0
        gst_in_dhours = self.lst_to_gst(lst_time)
        gst_in_dhours -= t0
        if gst_in_dhours > 24.0:
            gst_in_dhours -= 24.0
        elif gst_in_dhours < 0.0:
            gst_in_dhours += 24.0
        ut_time_dec = gst_in_dhours * 0.9972695663
        if ut_time_dec > 0.0 and ut_time_dec < unit.hms_to_dhours("000356"):
            suitability = False
        self.plate_data[4] = ut_time_dec
        return suitability

    def lst_to_gst(self, time):
        """Converts Local Sidereal Time to Greenwich Sidereal Time"""
        half_exp_time_hours = (self.plate_data[5] / 2) / 60

        time_plus_half_exp = unit.hms_to_dhours(time) + half_exp_time_hours
        longitude_in_h = self.longitude / 15.0

        time_plus_half_exp -= longitude_in_h
        if time_plus_half_exp > 24.0:
            time_plus_half_exp -= 24.0
        elif time_plus_half_exp < 0.0:
            time_plus_half_exp += 24.0

        return time_plus_half_exp

    def convert_exposure_time(self):
        """Converts the exposure time to minutes rather than tenths of"""
        exp_time = self.plate_data[5]
        exp_time_in_secs = unit.tenths_to_seconds(exp_time)
        exp_time_in_mins = exp_time_in_secs / 60
        self.plate_data[5] = exp_time_in_mins

if __name__ == '__main__':
    pass
