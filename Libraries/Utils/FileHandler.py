import os
import time
import datetime
import gzip
import shutil
from pathlib import Path
import requests
import csv
from tqdm import tqdm
from astroquery.jplhorizons import Horizons
from Libraries.Utils.Auxilliary import Bodies

class FileHandler(object):
    """Handles file manipulation, data parsing and saving"""

    plate_url_file = "Plate Locals.txt"
    dir_file = None

    def __init__(self):
        """Initialises All Directories and File Paths and Plate Data"""
        if os.path.isdir("Exports") == False:
            os.mkdir("Exports")
        if os.path.isdir("Ephemeris Cache") == False:
            os.mkdir("Ephemeris Cache")
        os.chdir("Ephemeris Cache")
        if os.path.isdir("Container") == False:
            os.mkdir("Container")
        os.chdir("..")
        self.temp_files = Path("Ephemeris Cache/Container")
        self.ext_file_dir = Path("Imports")
        os.chdir("Imports")
        if os.path.isdir("Plate Files") == False:
            os.mkdir("Plates Files")
        os.chdir("..")
        self.plate_save_dir = Path("Imports/Plate Files")
        self.ephem_files = Path("Ephemeris Cache")
        os.chdir("Exports")
        if os.path.isdir("Plate Saves") == False:
            os.mkdir("Plate Saves")
        if os.path.isdir("Fits Files") == False:
            os.mkdir("Fits Files")
        if os.path.isdir("Fits Images") == False:
            os.mkdir("Fits Images")
        if os.path.isdir("Excel Files") == False:
            os.mkdir("Excel Files")
        self.save_file_dir = Path("Exports/Plate Saves")
        self.save_fits_file = Path("Exports/Fits Files")
        self.save_fits_images = Path("Exports/Fits Images")
        self.save_excel = Path("Exports/Excel Files")
        os.chdir("..")
        self.plate_titles, self.plate_urls, self.plate_coordinates = self.resolve_plate()

    def get_body_list(self):
        """Reads list of bodies containted in External/Body List"""
        body_list_file_name = "Body List.txt"
        body_list_file_path = os.path.join(
            self.ext_file_dir, body_list_file_name)
        with open(body_list_file_path, "r") as body_list:
            data = [line.replace("\n","").split(" ") for line in body_list.readlines()]
            bodies = [line[0] for line in data]
            codes = [line[1] for line in data]

        if len(bodies) != len(codes):
            raise Exception("Error Missing Body Code in Body List File")
        bodies_list = [bodies, codes]

        return bodies_list

    def resolve_plate(self):
        """Retrives the plate data contained in External/Plate Locals"""
        with open(os.path.join(self.ext_file_dir, self.plate_url_file), 'r') as plate_urls:
            file_data = plate_urls.readlines()
            plate_file_title = [file_data[i].replace("\n","") for i in range(0, len(file_data), 3)]
            plate_file_urls = [file_data[i].replace("\n","") for i in range(1, len(file_data), 3)]
            plate_file_coords = [file_data[i].replace("\n","") for i in range(2, len(file_data), 3)]
        return plate_file_title, plate_file_urls, plate_file_coords

    def plate_download(self):
        """Download the plate files from the internet if required"""
        error_checker = []
        if len(os.listdir(self.plate_save_dir)) != len(self.plate_titles):
            print ("Downloading Plate Files")
            while len(os.listdir(self.plate_save_dir)) != len(self.plate_titles):
                for i in range(0, len(self.plate_urls)):
                    url_string = self.plate_urls[i].split("/")[-1].replace(
                        ".lis",".txt")
                    save_file_name = "{}".format(url_string)
                    try:
                        r = requests.get(self.plate_urls[i])
                    except ConnectionError:
                        print ("Connection Error : Download of file {} failed".format(save_file_name))
                        error_checker.append(False)
                    except TimeoutError:
                        print ("Timeout Error: Download of file {} failed".format(save_file_name))
                        error_checker.append(False)
                    print ("Saving Plate Catalog: {}. {}".format(
                        i + 1, save_file_name))
                    file_path = os.path.join(
                        self.plate_save_dir, save_file_name)
                    with open(file_path, "w") as save_file:
                        save_file.write("{}\n".format(self.plate_titles[i]))
                        save_file.write("{}\n".format(
                            self.plate_coordinates[i]))
                        for data in tqdm(r.text):
                            save_file.write(data)
                if len(error_checker) >= 2:
                    print("Error: All Files could not be downloaded only {} files were downloaded".format(
                        len(os.listdir(self.plate_save_dir))))
                    break
                if len(os.listdir(self.plate_save_dir)) == len(self.plate_titles):
                    print ("All Catalogues have been downladed successfully")
        else:
            print ("All plate files are present")

    def dir_unpack(self, dir_name):
        """Unpacks any directories' contents for user"""
        dir_contents = os.listdir(dir_name)
        for i, item in enumerate(dir_contents):
               print("{}. {}".format(i + 1, item)),
        return dir_contents

    def create_dir(self, file_name):
        """Creates subdirectory to hold multiple batched files"""
        dir_name = "{} Results - {}".format(
            file_name.replace(".txt","").title(),
        str(datetime.datetime.now()).replace("-",",").replace(":",","))
        folder_path = os.path.join(self.save_file_dir, dir_name)
        os.mkdir(folder_path)
        self.save_file_dir = folder_path

    def choose_content(self, dir_name):
        """The user can choose what is loaded into the programme"""
        print ("\nPICKING PLATE FILE TO BE LOADED")
        while True:
            files = self.dir_unpack(dir_name)
            if len(files) == 0:
                print("No Files Found In Directory")
            try:
                chosen_file = int(
                    input("Input Number corresponding to chosen file 1 to {}: ".format(len(files))))
            except (ValueError, UnboundLocalError):
                print ("Please enter a valid answer")
            else:
                if chosen_file < 1:
                    print ("Please Enter A Valid Number Between 1 and {}".format(len(files)))
                elif chosen_file > len(files):
                    print ("Please Enter A Valid Number Between 1 and {}".format(len(files)))
                else:
                    dir_file = files[chosen_file - 1]
                    possible_file_path1 = os.path.join(self.plate_save_dir, dir_file)
                    possible_file_path2 = os.path.join(self.save_file_dir,  dir_file)
                    if os.path.isdir(possible_file_path1) == True or os.path.isdir(possible_file_path2) == True:
                        if dir_name == self.plate_save_dir:
                            self.plate_save_dir = possible_file_path1
                            dir_name = self.plate_save_dir
                            print ("Moving into directory: {}".format(possible_file_path1))
                        elif dir_name == self.save_file_dir:
                            self.save_file_dir = possible_file_path2
                            dir_name = self.save_file_dir
                            print ("Moving into directory: {}".format(possible_file_path2))
                    else:
                        break
        if dir_name == self.plate_save_dir:
            self.dir_file = dir_file
            data, coordinates, info_string = self.manipulate_plate_file(dir_file)
            return data, coordinates, info_string
        elif dir_name == self.save_file_dir:
            data = self.get_results_data(dir_file)
            return data, dir_file

    def get_ephem_data(self, body, dates, coordinates):
        """Determins how the ephemeris data is retrieved and used"""
        cached_files = [item for item in os.listdir(self.ephem_files) if os.path.isfile(os.path.join(self.ephem_files ,item)) is True]
        file_present = False
        for files in cached_files:
            if files == "{} {}".format(body, self.dir_file):
                file_present = True
        if file_present == True:
            print ("Cached File Present")
            ephemeris_data = self.access_cache(body)
        else:
            print ("File Will Be Downloaded")
            ephemeris_data = self.download_ephemeris_data(body, dates, coordinates)
        ephemeris_data = [line.split(" ") for line in ephemeris_data]
        anlges_data = [line[0:2] for line in ephemeris_data]
        mag_data = [line[2:3] for line in ephemeris_data]
        uncertainty_data = [line[3:5] for line in ephemeris_data]
        return anlges_data, mag_data, uncertainty_data

    def download_ephemeris_data(self, body, dates, coordinates):
        """Downloads ephemeris data by querying the JPL Horizons site"""
        bodies_class = Bodies(*self.get_body_list())
        bodykey = bodies_class.get_body_code(body)
        uncertainties = []
        downloaded_data = []
        log_file = "Log.txt"
        for i in tqdm(range(0, len(dates), 380)):
            jpl_horizon = Horizons(
                id=bodykey, location=coordinates, epochs=dates[i: i + 380], id_type='id')
            eph = jpl_horizon.ephemerides(
                quantities='1,9,36', get_raw_response=True, refsystem='B1950',
                refraction = True).split("\n")

            for i in range(0, len(eph)):
                if "$$SOE" in eph[i]:
                    lower_bound = i
                if "$$EOE" in eph[i]:
                    upper_bound = i
                    data_points = eph[lower_bound + 1:upper_bound]
                    break
            try:
                for i in range(0, len(data_points)):
                    if len(data_points[i]) == 10:
                        uncertainties = [data.strip() for data in data_points[i].split(",")[8:10]]
                    else:
                        uncertainties = [data.strip() for data in data_points[i].split(",")[7:9]]
                    data_points[i] = [data.strip() for data in data_points[i].split(",")[4:7]]
                    data_points[i] += uncertainties
                    downloaded_data.append(" ".join(data_points[i]))
            except UnboundLocalError:
                with open(os.path.join(self.temp_files, log_file)) as error_logger:
                    for line in eph:
                        logging.write("{}\n".format(line))
                    raise Exception("Problem With Loading Ephemeris Data, Check Log.txt File For More Details")

        with open(os.path.join(self.temp_files, log_file), "w") as logging:
            print ("Writing Ephemeris Log")
            for line in eph:
                logging.write("{}\n".format(line))

        self.cache_ephemeris_data(body, downloaded_data)

        return downloaded_data

    def cache_ephemeris_data(self, body, data_stream):
        """Caches any ephemeris data downloaded for future use"""
        print ("Caching Ephermeris Data")
        cache_file_name = "{} {}".format(body, self.dir_file)
        cache_file_path = os.path.join(self.ephem_files, cache_file_name)
        with open(cache_file_path, "w") as cache_file:
            for line in data_stream:
                cache_file.write("{}\n".format(line))

    def access_cache(self, body):
        """Acces cache if an existing cache file is found"""
        print("Loading Cached File")
        cache_file_name = "{} {}".format(body, self.dir_file)
        cache_file_path = os.path.join(self.ephem_files, cache_file_name)
        with open(cache_file_path, "r") as cache_file:
            data = [line.replace("\n", "") for line in cache_file.readlines()]
        return data

    def purge_cache(self):
        """Purges cached files, so files can be updated"""
        print("\n")
        cache_dir_contents = [item for item in os.listdir(self.ephem_files) if os.path.isfile(os.path.join(self.ephem_files ,item)) is True]
        if len(cache_dir_contents) == 0:
            print("No Files Found TO Be Purged")
        else:
            last_dir_mod_date = os.path.getmtime(self.ephem_files)
            # purges the cache after an hour of time has passed without edit
            time_difference = (time.time() - last_dir_mod_date) / 3600
            if time_difference > 1.0:
                print("Refreshing Cache: Purging Cache Files")
                self.purge_cache_files(cache_dir_contents)
            else:
                purging_options = ["Purge Cache Files",
                "Keep Current Cache Files"]
                self.list_options(purging_options)
                while True:
                    try:
                        manual_purge = int(input("Please enter the number   corresponding for desired option: "))
                    except (ValueError, UnboundLocalError):
                        print ("Please enter a valid number")
                    else:
                        if manual_purge < 1 or manual_purge > 2:
                            print ("Please enter a number of 1 or 2")
                        elif manual_purge == 1:
                            print ("Purging cache files")
                            self.purge_cache_files(cache_dir_contents)
                        elif manual_purge == 2:
                            print ("No Cache files will be deleted")
                        break

    def purge_cache_files(self, cache_files):
        """Puches files in directory"""
        for i in range(0, len(cache_files)):
            file_path = os.path.join(self.ephem_files, cache_files[i])
            self.delete_file(file_path)

    def manipulate_plate_file(self, dir_file):
        """Retrieves all the data from a given plate file"""
        with open(os.path.join(self.plate_save_dir, dir_file), "r")  as plate_file:
            data = plate_file.readlines()
            data = [line.replace("\n","") for line in data]
            info_string = data[0]
            print("File Chosen: {} - {}".format(dir_file, info_string))
            del data[0]

            coordinates = [float(point) for point in data[0].split(" ")]
            coordinates = {'lon': coordinates[1], 'lat': coordinates[0], 'elevation': coordinates[2]}
            del data[0]
        return data, coordinates, info_string

    def get_results_data(self, dir_file):
        """Retrives data plate results file"""
        with open(os.path.join(self.save_file_dir, dir_file), "r") as results_file:
            data = results_file.readlines()
            data = [line.replace("\n","") for line in data]
            del data[0:9]
        return data

    def save_results(self, body, plates, plate_hits, body_loc_on_plate,
    body_coordinates, skipped_plates, local_info, coordinates, body_mags,
    uncertainties):
        """Saves results of computation to a file in Plate Save dir"""
        date = str(datetime.datetime.now()).replace("-",",").replace(":",",")
        file_name = "{} - {}.txt".format(body.title(), date)
        if "/" in file_name:
            file_name = file_name.replace("/",",")
        print ("Saving data to file : {} located in outputs directory".format(file_name))
        with open(os.path.join(self.save_file_dir, file_name), "w") as results_file:
            results_file.write("Body Tracked: {}\n".format(body))
            results_file.write("Plate Origin: {}\n".format(local_info))
            results_file.write("Observatory Coordinates:{} Lat {} Lon {} Elevation\n".format(coordinates['lat'], coordinates['lon'],
            coordinates['elevation']))
            results_file.write("Total Number Of Plates Checked: {}\n".format(len(plates)))
            results_file.write("Number Of Rejected Plates (Not Checked): {}\n".format(skipped_plates))
            results_file.write("Number Of Plates The Body Was Found On: {}\n".format(
                len([hits for hits in plate_hits if hits is True])))
            results_file.write("Plates that are supplied are said to contain the body: B and P denote Body and Plate Respectively\n\n")
            results_file.write("P Filter | P Numb | P Exp (Mins) | P X Coord (mm) | P Y Coord (mm) | B Mag | B RA (H:M:S / Radians) | B DEC (DEG:M:S / Radians) | B X, Y Uncertainties\n")
            for i in range(len(plates)):
                if plate_hits[i] == True:
                    results_file.write("{} | {} | {} | {} | {} | {} | {} / {} | {} / {} | {}\n".format(plates[i].plate_filter, plates[i].plate_numb, plates[i].duration, body_loc_on_plate[i][0], body_loc_on_plate[i][1], body_mags[i][0], body_coordinates[i][0], repr(body_coordinates[i][0]),body_coordinates[i][1], repr(body_coordinates[i][1]), " , ".join(uncertainties[i]) ))

    def read_body_files(self):
        """Choose which file of bodies to load"""
        body_file_directory = "Body Files"
        dir_path = os.path.join(self.ext_file_dir, body_file_directory)
        if len(os.listdir(dir_path)) == 0:
            return None
        else:
            print("Files To Choose From")
            body_cat_files = self.dir_unpack(dir_path)
            while True:
                try:
                    chosen_file = int(input("Enter Number for File chosen: "))
                except (ValueError, UnboundLocalError):
                    print("Please enter a valid number between 1 and {}".format(len(body_cat_files)))
                else:
                    if chosen_file < 1 or chosen_file > len(body_cat_files):
                        print ("Please enter a number in the range 1 to {}".format(len(body_cat_files)))
                    else:
                        file_name_chosen = body_cat_files[chosen_file - 1]
                        for i in range(len(body_cat_files)):
                            body_cat_files[i] = os.path.join(dir_path, body_cat_files[i])
                        with open(body_cat_files[chosen_file - 1], "r") as body_file:
                            bodies = body_file.readlines()
                            bodies = [bodies[i].replace("\n","") for i in range(len(bodies))]
                            break
            return bodies, file_name_chosen

    def unpack_file(self, file_contents):
        """Unpacks the contents of a file"""
        for i, item in enumerate(file_contents):
            print ("{}. Plate Number: {}".format(i + 1, item.split(" | ")[1]))

    def choose_file_content(self, file_contents):
        """Choose what data point in saved results file is chosen"""
        self.unpack_file(file_contents)
        while True:
            try:
                data_point = int(input("Please enter number for data point: "))
            except (ValueError, UnboundLocalError):
                print("Please enter a valid number")
            else:
                if data_point < 1 or data_point > len(file_contents):
                    print("Please enter a number between 1 and {}".format(
                        len(file_contents)))
                else:
                    data_string = file_contents[data_point - 1].split(" | ")
                    del data_string[5]
                    del data_string[2]
                    break
        return data_string

    def download_fits_file(self, url, body, plate_number):
        """Download the fits file from the sky cosmos website"""
        print("Downloading File")
        r = requests.get(url, stream = True)
        file_name = "{}-{}".format(body.title(), plate_number)
        path = os.path.join(self.save_fits_file, file_name)
        if r.status_code == 200:
            with open(path, 'wb') as fits_file:
                r.raw.decode_content = True
                gzip_file = gzip.GzipFile(fileobj=r.raw)
                shutil.copyfileobj(gzip_file, fits_file)
        else:
            raise FileDownloadError("Fits File Failed to be Downloded")
        save_path = os.path.join(self.save_fits_images, file_name)
        return path, save_path

    def choose_fits_file(self):
        """Chooses existing fits files that are saved in Fits Files"""
        while True:
            fits_files = self.dir_unpack(self.save_fits_file)
            if len(fits_files) == 0:
                print("No Files found in directory")
                break
            else:
                try:
                    chosen_fits = int(
                        input("Please enter number for desired fits file: "))
                except (ValueError, UnboundLocalError):
                    print ("Please enter a valid number")
                else:
                    if chosen_fits <1 or chosen_fits > len(fits_files):
                        print ("Enter a valid number between 1 and {}".format(len(fits_files)))
                    else:
                        fits_file = os.path.join(self.save_fits_file, fits_files[chosen_fits- 1])
                        if os.path.isdir(fits_file) == True:
                            self.save_fits_file = fits_file
                            print("Moving into Directory: {}".format(fits_file))
                        else:
                            save_path = os.path.join(self.save_fits_images, fits_files[chosen_fits - 1])
                            break
        return fits_file, save_path

    def save_excel_file(self, excel_data):
        """Saves excel file to the Excel Files Directory"""
        file_name = "{}.xlsx".format(str(datetime.datetime.now()).replace(":",",").replace("-",","))
        file_path = os.path.join(self.save_excel, file_name)
        excel_data.save(file_path)
        print ("Saving Excel File As {} in Excel Files Directory".format(
            file_name))

    def delete_file(self, file_path):
        """Deletes fits file after it has been plotted"""
        os.remove(file_path)

    @staticmethod
    def list_options(options):
        """Lists numbered options"""
        for i, option in enumerate(options):
            print ("{} - {}".format(i + 1, option)),

if __name__ == '__main__':
    pass
