from Libraries.Utils.BodyHandler import BodyHandler
from Libraries.Core.Converter import Converter
from Libraries.Utils.Auxilliary import Plate
from Libraries.Core.PlateComputation import PlateComputation
from Libraries.Utils.GraphHandler import GraphHandler
from Libraries.Utils.ExcelHandler import ExcelHandler
import Libraries.Core.UnitChanger as unit
from tqdm import tqdm

class PlateFinder(BodyHandler):
    """Class used to get the data from the bodies"""
    def __init__(self):
        BodyHandler.__init__(self)
        self.plates = []
        self.dates = []
        self.total_plates = []
        self.angles = None
        self.magnitudes = None
        self.uncertainty = None

    def check_body_list(self):
        """Checks if the body list is empty"""
        if self.chosen_bodies == None:
            raise Exception("No bodies found within list")

    def comp_or_graph(self):
        """Chooses what modules to run"""
        running_options = ["Plate Computation", "Plate Images", "Both"]
        while True:
            try:
                self.file_handler.list_options(running_options)
                c_or_g = int(
                    input("Enter Desired Number For What Modules You Would Like To Run: "))
            except (ValueError, UnboundLocalError):
                print("Please enter a valid number")
            else:
                if c_or_g < 1 or c_or_g > 3:
                    print("Please enter a number between 1 and 3")
                elif c_or_g == 1:
                    self.choose_file()
                    self.choose_body()
                    self.computation()
                    break
                elif c_or_g == 2:
                    self.get_fits()
                    break
                elif c_or_g == 3:
                    self.choose_file()
                    self.choose_body()
                    self.computation()
                    self.get_fits()
                    break

    def computation(self):
        """Computes the data for each body chosen"""
        print("\nCOMPUTATION MODULE")
        self.check_body_list()

        plates_skipped = self.sort_loop()

        self.file_handler.purge_cache()

        for i in range(0, len(self.chosen_bodies)):

            self.generate_ephemeris(self.chosen_bodies[i])

            print ("\nCALCULATING DATA FOR BODY {} of {}. {}".format(
                i + 1, len(self.chosen_bodies), self.chosen_bodies[i].upper()))

            results = self.compute_loop()
            if len([hits for hits in results[0] if hits is True]) == 0:
                print("File For Body {} Will Not Be Saved".format(self.chosen_bodies[i]))
            else:
                self.total_plates.append(True * len([hits for hits in results[0] if hits is True]))
                self.file_handler.save_results(self.chosen_bodies[i], self.plates, results[0], results[1], self.angles, plates_skipped, self.local_info, self.coordinates, self.magnitudes, self.uncertainty)

        if len(self.chosen_bodies) > 1:
            print ("Bodies were found on a total of {} plates".format(
                len(self.total_plates)))

    def sort_loop(self):
        """Checks for invalid plates, converts others to proper units"""
        null_plates = []
        print ("Sorting Plates Entries")
        for i in tqdm(range(0, len(self.plate_data))):
            sorter = Converter(self.coordinates['lon'], self.plate_data[i])
            entries_s = sorter.check_invalid_entries()
            if entries_s == False:
                null_plates.append(False)
                continue
            else:
                dates, suitability = sorter.convert()
                if suitability == False:
                    continue
                self.dates.append(dates)
                plate_class = Plate(*sorter.plate_data)
                self.plates.append(plate_class)
        print ("Total Number of Plates Skipped: {} out of {} total".format(len(null_plates),
        len(self.plate_data)))
        return len(null_plates)

    def generate_ephemeris(self, body):
        """Generates ephemeris data from JPL Horizons"""
        print ("\nGetting Ephemeris Data For {}".format(body))
        self.angles, self.magnitudes, self.uncertainty = self.file_handler.get_ephem_data(
            body, self.dates, self.coordinates)
        self.uncertainty = unit.change_uncertainties(self.uncertainty)
        for i in range(0, len(self.angles)):
            for j in range(0, len(self.angles[0])):
                if j == 0:
                    self.angles[i][j] = unit.convert_to_hours(unit.degrees_to_rads(self.angles[i][j]))
                elif j == 1:
                    self.angles[i][j] = unit.convert_to_deg(
                       unit.degrees_to_rads(self.angles[i][j]))

    def compute_loop(self):
        """Computes the data for a given body"""
        computer = PlateComputation()
        print ("Computing Plates")
        for i in tqdm(range(0, len(self.plates))):
            computer.compute_plate(self.plates[i], self.angles[i], float(self.magnitudes[i][0]))
        on_plate, on_plate_location = computer.finished(self.plates)
        return on_plate, on_plate_location

    def get_fits(self):
        """Computes the plotting of the sky using supercosmos"""
        print("\nGRAPHING MODULE")
        graphing_options = ["Downloading Fits File", "Pick Existing File", "Both"]
        while True:
            self.file_handler.list_options(graphing_options)
            try:
                d_or_g = int(input("Enter The Corresponding Number For How You Want The Graphing Module To Run: "))
            except (ValueError, UnboundLocalError):
                print("Please enter a valid number")
            else:
                if d_or_g < 1 or d_or_g > 3:
                    print("Please enter a number between 1 and 3")
                elif d_or_g == 1:
                    self.download_fits()
                    break
                elif d_or_g == 2:
                    self.existing_fits()
                    break
                elif d_or_g == 3:
                    self.download_fits()
                    self.existing_fits()
                    break

    def existing_fits(self):
        """Chooses and plots existing fits file"""
        fits_file, save_path = self.file_handler.choose_fits_file()
        Grapher.plot_data(fits_file, save_path)

    def download_fits(self):
        """Downloads ad plots fits file based on plate entry"""
        while True:
            try:
                download_amount = int(
                input("Please Enter The Number of Files to be downloaded : "))
            except (ValueError, UnboundLocalError):
                print("Please enter a valud number")
            else:
                if download_amount < 1:
                    print("Can't enter less than one")
                else:
                    loop_data = []
                    for i in range(download_amount):
                        data, file_name = self.file_handler.choose_content(self.file_handler.save_file_dir)
                        data_point = self.file_handler.choose_file_content(data)
                        body_name = file_name.split("-")[0].strip()
                        data_point.insert(0, body_name)
                        loop_data.append(data_point)
                        grapher = GraphHandler(
                            data_point[1], data_point[5], data_point[6])

                        link = grapher.get_sky_survey()
                        if link is None:
                            print("Error: Download Link Not Found")
                            continue

                        plate_number = data_point[2]
                        path, save_path = self.file_handler.download_fits_file(
                            link, body_name, plate_number)
                        grapher.plot_data(path, save_path)
                        self.file_handler.delete_file(path)
                    self.save_to_excel(loop_data)
                    break

    def save_to_excel(self, data):
        """Saves data of each plate to an excel file"""
        while True:
            print ("\n")
            self.file_handler.list_options(self.answers)
            try:
                save_to_excel = int(
                input("Save data to excel for experimental process?: "))
            except (ValueError, UnboundLocalError):
                print("Please enter a valud number")
            else:
                if save_to_excel < 1 or save_to_excel > 2:
                    print("Please enter a valid nunber of 1 or 2")
                elif save_to_excel == 1:
                    for i in range(0, len(data)):
                        del data[i][5:8]
                        del data[i][1]
                    excel_handler = ExcelHandler(data)
                    workbook = excel_handler.parse_data()
                    self.file_handler.save_excel_file(workbook)
                elif save_to_excel == 2:
                    print("No Excel file will be created")
                break
if __name__ == '__main__':
    pass
