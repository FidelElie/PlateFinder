from Libraries.Core.CoordinateSystems import to_tangent_proj
import Libraries.Core.UnitChanger as unit
from Libraries.Utils.FileHandler import FileHandler
from Libraries.Utils.Auxilliary import WaveBand
from numpy import log10

class PlateComputation(object):
    """Handles computation of plate data points"""

    plate_size = 6.0 * (unit.use_pi() / 180.0)

    def __init__(self):
        self.plate_hits = []
        self.location_on_plate = []

    def compute_plate(self, plate, ra_and_dec, body_mag):
        """Computes the data for a specific plate"""
        body_ra = ra_and_dec[0]
        body_dec = ra_and_dec[1]
        xi, eta, suitability1 = to_tangent_proj(
            body_ra, body_dec, plate.ra, plate.dec)
        suitability2 = self.check_limiting_mag(plate, body_mag)
        if suitability1 == False or suitability2 == False:
            self.plate_hits.append(False)
        else:
            self.plate_hits.append(self.check_on_plate(xi, eta))
        self.location_on_plate.append(unit.angle_to_mm(xi, eta))

    def check_limiting_mag(self, plate, body_mag):
        exposure_time = plate.duration
        plate_limit, plate_nominal_exp = WaveBand.get_limiting_magnitude(plate.plate_filter)
        if plate_limit == "N/A" or plate_nominal_exp == "N/A":
            suitability = True
        else:
            exp_ratio = exposure_time / plate_nominal_exp
            if exp_ratio == 0.0:
                suitability = True
            else:
                log_exp_ratio = log10(exp_ratio)
                magnitude_difference = log_exp_ratio * 1.25
                limiting_magnitude = plate_limit + magnitude_difference
                if body_mag > limiting_magnitude:
                    suitability = False
                else:
                    suitability = True

        return suitability

    def check_on_plate(self, xi , eta):
        """Determines whether the coordinates are on the plate"""
        if abs(xi) < self.plate_size / 2.0 and abs(eta) < self.plate_size / 2.0:
            on_plate = True
        else:
            on_plate = False
        return on_plate

    def finished(self, plates):
        """Returns finishing data about the body"""
        print ("Body was located on a total of {} plates".format(
            len([hits for hits in self.plate_hits if hits is True])))
        return self.plate_hits, self.location_on_plate

if __name__ == '__main__':
    pass
