class Sorter(object):
    """Sifting, Checking And Rolling Out Plate Data"""
    def __init__(self, plate_string):
        self.plate_string = plate_string
        # gets all properties from indexing the string
        self.plate_filter = self.plate_string[0:2]
        self.plate_numb = self.plate_string[2:7]
        self.plate_suffix = self.plate_string[7:8]
        self.ra_and_dec = self.plate_string[20:30]
        self.date_of_exp = self.plate_string[30:36]
        self.time_of_exp = self.plate_string[36:40]
        self.exp_duration = self.plate_string[52:56]
        self.plate_data = self.set_plate_data()

    def set_plate_data(self):
        """Sets the data into a list"""
        return [self.plate_filter, self.plate_numb, self.ra_and_dec,
            self.date_of_exp, self.time_of_exp, self.exp_duration]

    def check_invalid_entries(self):
        """Checks for invalid plate entries"""
        empty_field = False
        invalid_gap = False
        suitability = True
        for i in range(len(self.plate_data)):
            if len(self.plate_data[i].strip()) == 0:
                empty_field = True
        for i in range(len(self.plate_data)):
            if " " in self.plate_data[i].strip():
                invalid_gap = True
        if empty_field == True or invalid_gap == True:
            suitability = False
        if self.plate_suffix.strip() != "":
            suitability = False
        if self.plate_filter == "HE" or self.plate_filter == "HA" or self.plate_filter == "O3" or self.plate_filter[-1] == "F" or self.plate_filter[-1] == "X" or self.plate_filter[-1] == "P" or self.plate_filter[-1] == "G":
            suitability = False
        return suitability
