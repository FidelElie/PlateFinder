
    @staticmethod
    def ephem_ra_to_rads(right_ascension):
        """Method to convert right ascension into radians (EPHEM)"""
        if ":" in right_ascension[0:2]:
            right_ascension = "0" + right_ascension
        right_ascension = right_ascension.replace(":","")
        hours = float(right_ascension[0:2]) * 15
        minutes = float(right_ascension[2:4]) / 4
        seconds = float(right_ascension[4:len(right_ascension)]) / 240
        total_radians = (hours + minutes + seconds) * ((np.pi) / 180)
        return total_radians
    
    @staticmethod
    def ephem_dec_to_rads(declination):
        """Method to convert declination into radians (EPHEM)"""
        if "-" not in declination:
            declination = "+" + declination
        declination = declination.replace(":","")
        degrees = float(declination[0:3])
        arc_minutes = float(declination[3:5]) / 60
        arc_seconds = float(declination[5:len(declination)]) / 3600 
        total_radians = (degrees + arc_minutes + arc_seconds) * (np.pi / 180)
        return total_radians

    @staticmethod
    def plate_ra_to_rads(right_ascension):
        """Method to convert right ascesnsion into radians"""
        hours = float(right_ascension[0:2])
        dec_mins = float(right_ascension[2:4] + "." + right_ascension[4:5])
        total_radians = ((15 * np.pi) / 180) * ((hours + dec_mins )/ 60.0)
        return total_radians

    @staticmethod
    def plate_dec_to_rads(declination):
        """Method to convert declination into radians"""
        degrees = float(declination[0:3])
        minutes  = (float(declination[3:5]) / 60) * 15
        total_radians = (degrees + minutes) * (np.pi / 180)
        return total_radians