class Plate(object):
    """Plate Properties

    Properties -
    Plate Filter: Code for which one is used
    Plate Number: To Identify the plate
    Plate Survey: Letter or numerical code for survey plate belongs to
    Plate Ra: Plate Right Ascension
    Plate Dec: Plate Declination
    Plate Date: Universal Date of exposure
    Plate Time: Universal Time of Exposure
    Plate Duration: Duration of exposure
    """
    def __init__(self, plate_filter, plate_numb, ra_and_dec, date, time, duration):
        self.plate_filter = plate_filter
        self.plate_numb = plate_numb
        self.ra = ra_and_dec[0]
        self.dec = ra_and_dec[1]
        self.date = date
        self.time = time
        self.duration = duration

class WaveBand(object):
    """Holds the waveband information

    Properties-
    Blue Wave Band: Takes Codes U B J and Y
    Red Wave Band: Takes Codes R V and O
    Infared Wave Band: Takes Codes I W and Z
    """
    def __init__(self):
        self.blue_wave_band = ["U", "B", "J", "Y"]
        self.red_wave_band = ["R", "V", "O"]
        self.i_red_wave_band = ["I", "W", "Z"]

    @staticmethod
    def get_limiting_magnitude(plate_filter):
        if plate_filter == "OR":
            limiting_mag = 22.0
            nominal_exposure = 60.0
        else:
            if len(plate_filter.strip()) != 1:
                plate_code = plate_filter.strip()[1]
            else:
                plate_code = plate_filter.strip()
            if plate_code == "B" or plate_code == "V":
                limiting_mag = 21.0
                nominal_exposure = 60.0
            elif plate_code == "J":
                limiting_mag = 22.5
                nominal_exposure = 60.0
            elif plate_code == "I":
                limiting_mag = 19.5
                nominal_exposure = 90.0
            elif plate_code == "W" or plate_code == "Z":
                limiting_mag = "N/A"
                nominal_exposure = "N/A"
            elif plate_code == "U":
                limiting_mag = "N/A"
                nominal_exposure = 180.0
            elif plate_code == "R":
                limiting_mag = 21.5
                nominal_exposure = 75.0
            else:
                limiting_mag = "N/A"
                nominal_exposure = "N/A"

        return limiting_mag, nominal_exposure

class Bodies(object):
    """Holds body information"""
    def __init__(self, bodies_list, codes_list):
        self.bodies_list = bodies_list
        self.codes_list = codes_list

    def get_body_code(self, body_name):
        hits = []
        for i in range(0, len(self.bodies_list)):
            if body_name == self.bodies_list[i]:
                key = self.codes_list[i]
                hits.append(True)
            else:
                hits.append(False)
        if [False] * len(self.bodies_list) == hits:
            return body_name
        else:
            print ("Found Standard Body Code")
            return key

if __name__ == '__main__':
    pass
