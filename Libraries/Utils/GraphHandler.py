from Libraries.Core.UnitChanger import angles_to_str
from Libraries.Utils.Auxilliary import WaveBand
import datetime
import matplotlib.pyplot as plt
import requests
from astropy.io import fits
from robobrowser import RoboBrowser
from numpy import pi, fliplr

class GraphHandler(WaveBand):
    """Class to plot and download fits images"""
    def __init__(self, plate_filter, ra, dec):
        WaveBand.__init__(self)
        self.browser = RoboBrowser(parser='html.parser')
        self.filter = plate_filter
        self.ra = ra
        self.dec = dec
        self.display_size = "30"
        self.filter_parameter = None

    def get_sky_survey(self):
        """Method to get link to download the fits file"""
        print ("Sending Download Request")
        self.browser.open('http://www-wfau.roe.ac.uk/sss/pixel.html')
        form = self.browser.get_form()
        form['coords'].value = angles_to_str(
            self.ra.split(" / ")[0], self.dec.split(" / ")[0])
        form['size'].value = self.display_size
        form['equinox'].value = "1"
        form['waveband'].value = self.choose_waveband()
        self.browser.submit_form(form)
        download_link = str(self.browser.find("a"))
        if download_link != None:
            download_link = download_link.split(" ")[1].split("\"")[1]
        return download_link

    def check_filter(self):
        """Method to check what code the plate uses for the filter"""
        if len(self.filter.strip()) == 1:
            print("Filter uses standard code")
            self.filter_parameter = self.filter.strip()
        else:
            print("Filter uses two character code")
            self.filter_parameter = self.filter.strip()[1]

    def choose_waveband(self):
        """Method to choose the waveband for the website"""
        filter_parameter = self.check_filter()
        dec_degree_value = float(self.dec.split(" / ")[1]) * (180 / pi)
        if dec_degree_value >= 0:
            print("Northen Hemisphere: Palomar")
            wave_band_key = self.palomar_survey()
        elif dec_degree_value < 0:
            print("Southern Hemisphere: UKST")
            wave_band_key = self.ukst_survey()
        return wave_band_key

    def palomar_survey(self):
        """Determines the waveband the palomar survey should use"""
        dec = float(self.dec.split(" / ")[1]) * (180 / pi)
        if dec >=  0.0 and dec <= 3.0:
            print ("Using POSS I Red -21.0 < dec < +3")
            key = "P"
        elif self.filter_parameter in self.blue_wave_band:
            print ("Using POSS I Red +2.0 < dec < +90")
            key = "A"
        elif self.filter_parameter in self.red_wave_band:
            print ("Using POSS II Blue +2.0 < dec < +90")
            key = "B"
        elif self.filter_parameter in self.i_red_wave_band:
            print ("Using POSS II Infared +2.0 < dec < +90")
            key = "N"
        return key

    def ukst_survey(self):
        """Determines the waveband the ukst survey should use"""
        if self.filter_parameter in self.blue_wave_band:
            print ("Using UKST Blue -90 < dec < +3")
            key = "J"
        elif self.filter_parameter in self.red_wave_band:
            print ("Using UKST Red -90 < dec < +3")
            key = "R"
        elif self.filter_parameter in self.i_red_wave_band:
            print ("Using UKST Infared -90 < dec < +3")
            key = "I"
        return key

    def plot_data(self, file_path, save_path):
        """Function To Plot the fits file data and save a png image"""
        print ("Plotting Image")
        try:
            hdu_list = fits.open(file_path, ignore_missing_end=True , memmap=True)
        except OSError:
            raise Exception("Error: file cannot be loaded, corrupted fits file")
        else:
            image_data = hdu_list[0].data
            hdu_list.close()
            x_midpoint = float(self.ra.split(" / ")[1])
            y_midpoint = float(self.dec.split(" / ")[1])
            arc_extent = ((float(self.display_size) / 2.0) / 60.0) * (pi / 180)
            plt.imshow(fliplr(image_data), cmap = 'gray', origin='lower',
            extent=[x_midpoint - arc_extent, x_midpoint + arc_extent,
            y_midpoint - arc_extent, y_midpoint + arc_extent])
            save_path = save_path + ".png"
            print("Saving Figure - {}".format(save_path))
            plt.savefig(save_path, dpi=300)

if __name__ == '__main__':
    pass
