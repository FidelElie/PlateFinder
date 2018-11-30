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