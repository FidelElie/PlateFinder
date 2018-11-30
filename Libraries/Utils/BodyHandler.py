from Libraries.Utils.FileHandler import FileHandler
from Libraries.Utils.Auxilliary import Bodies

class BodyHandler(object):
    """Class to determine which bodies are chosen"""

    plate_data = None
    coordinates = None
    local_info = None
    chosen_bodies = None

    def __init__(self):
        self.file_handler = FileHandler()
        self.default_bodies = self.file_handler.get_body_list()[0]
        self.answers = ["Yes", "No"]

    def choose_file(self):
        self.file_handler.plate_download()
        plate_data, coordinates, title = self.file_handler.choose_content(self.file_handler.plate_save_dir)
        self.plate_data = plate_data
        self.coordinates = coordinates
        self.local_info = title

    def choose_body(self):
        """Determines if bodies are loaded from default or a file"""
        print ("\nPICKING BODIES TO BE COMPUTED:")
        while True:
            input_methods = ["Pick From Body List", "Load A Body File"]
            try:
                self.file_handler.list_options(input_methods)
                input_choice = int(input("Enter Number Corresponding To Desired Method For Loading Bodies: "))
            except (ValueError, UnboundLocalError):
                print("Please Enter A Valid Answer Number Between 1 and 2")
            else:
                if input_choice < 1 or input_choice > 2:
                    print ("Enter A Number Between 1 - 2")
                elif input_choice == 1:
                    print ("\nChoosing From Bodies List")
                    body_list = self.choose_from_list()
                    break
                elif input_choice == 2:
                    print ("\nLoading Bodies From File")
                    body_list = self.choose_from_file()
                    if body_list == None:
                        print ("No Files Found")
                    else:
                        break
        self.chosen_bodies = body_list

    def choose_from_list(self):
        """Method for default bodies to be chosen"""
        self.file_handler.list_options(self.default_bodies)
        bodies_chosen = []
        i = 1
        while True:
            if i > 1:
                print("Bodies Chosen: {}".format(",".join(bodies_chosen)))
            while True:
                try:
                    choose_body = int(
                        input("Input 1-5 for desired body, Enter 6 to list bodies, Enter 7 to exit : "))
                except (ValueError, UnboundLocalError):
                    print("Please Enter A Valid Number Between 1 and 7")
                else:
                    if choose_body < 1 or choose_body > 7:
                        print ("Enter a number between 1 and 7")
                    elif choose_body >= 1 and choose_body <= 5:
                        bodies_chosen.append(self.default_bodies[choose_body - 1])
                        break
                    elif choose_body == 6:
                        self.file_handler.list_options(self.default_bodies)
                    elif choose_body == 7:
                        break
            if len(bodies_chosen) == 0:
                print ("Please enter at least one body to be computed")
            elif self.yes_or_no() == True:
                break
            else:
                i += 1
        return bodies_chosen

    def choose_from_file(self):
        """Loads bodies from a file in External/Body Files dir"""
        while True:
            loaded_bodies, dir_name = self.file_handler.read_body_files()
            if loaded_bodies == None:
                chosen_bodies = None
                break
            else:
                if len(loaded_bodies) > 5:
                    maniup_options = ["Load All Bodies", "Filter List"]
                    while True:
                        self.file_handler.list_options(maniup_options)
                        try:
                            choose_some = int(input("Enter Number Corresponding To What Bodies Should Be Loaded: "))
                        except (ValueError, UnboundLocalError):
                            print("Please Enter A Valid Number")
                        else:
                            if choose_some < 1 or choose_some > 2:
                                print("Please Enter Either Numbers 1 or 2")
                            elif choose_some == 1:
                                print("Here")
                                chosen_bodies = loaded_bodies
                            elif choose_some == 2:
                                chosen_bodies = self.mod_body_list(loaded_bodies)
                            break
                else:
                    chosen_bodies = loaded_bodies
                break
        if len(chosen_bodies) > 1:
            print ("Creating Directory to hold bodies results")
            self.file_handler.create_dir(dir_name)
        return chosen_bodies

    def mod_body_list(self, loaded_bodies):
        """Modifies body list given, if more than 5 bodies loaded"""
        mod_options = ["Range : Range Of Bodies In File", "Comma Seperated : Multiple Bodies Throughout File", "Singular : One Body From File"]
        mod_strings = ["range", "comma", "singular"]
        while True:
            self.file_handler.list_options(mod_options)
            try:
                enter_method = int(input("Enter number corresponding to what choice you would like: "))
            except (ValueError, UnboundLocalError):
                print("Please enter a number between 1 and 3")
            else:
                if enter_method < 1 or enter_method > 3:
                    print("Please enter a number between 1 and 3")
                elif enter_method == 1:
                    mod_bodies = self.mod_method(mod_strings[enter_method - 1], loaded_bodies)
                    break
                elif enter_method == 2:
                    mod_bodies = self.mod_method(mod_strings[enter_method - 1], loaded_bodies)
                    break
                elif enter_method == 3:
                    mod_bodies = self.mod_method(mod_strings[enter_method - 1], loaded_bodies)
                    break
        return mod_bodies

    def mod_method(self, identifier, loaded_bodies):
        """Determins what modification method is used and applies it"""
        while True:
            self.file_handler.list_options(
                [body.split(",")[0] for body in loaded_bodies])
            if identifier == "range":
                chosen_range = input("Enter chosen range number seperated By a - : ").replace(" ","").split("-")
                if len(chosen_range) < 2 or len(chosen_range) > 2:
                    print("No range entered")
                else:
                    try:
                        int_range = [int(numb) for numb in chosen_range]
                    except (ValueError, UnboundLocalError):
                        print("Error Not all range entries were numbers")
                    else:
                        range_list = [min(int_range) - 1, max(int_range) -1]
                        range_numbs = [i for i in range(range_list[0], range_list[1])]
                        try:
                            mod_bodies = [loaded_bodies[i] for i in range_numbs]
                        except IndexError:
                            print("Error: invalid number entered")
                        else:
                            break
            elif identifier == "comma":
                chosen_numbs = input("Enter chosen number seperated by a comma: ").replace(" ","").split(",")
                if len(chosen_numbs) < 1 or len(chosen_numbs) > len(loaded_bodies):
                    print ("Please enter a valid amount of numbers")
                else:
                    try:
                        list_numbs = [(int(numb) - 1) for numb in chosen_numbs]
                    except (ValueError, UnboundLocalError):
                        print("Error not all values are numbers")
                    else:
                        try:
                            mod_bodies = [loaded_bodies[i] for i in list_numbs]
                        except IndexError:
                            print("Error: invalid number entered")
                        else:
                            break
            elif identifier == "singular":
                try:
                    chosen_numb = int(input("Enter number for chosen body: "))
                except (ValueError, UnboundLocalError):
                    print("Please enter a valid number")
                else:
                    if chosen_numb < 1 or chosen_numb > len(loaded_bodies):
                        print("Please enter a valid number between 1 and {}".format(len(loaded_bodies)))
                    else:
                        mod_bodies = [loaded_bodies[chosen_numb - 1]]
                        break
        return mod_bodies

    def yes_or_no(self):
        """Answer yes or no to questions"""
        self.file_handler.list_options(self.answers)
        while True:
            try:
                finished = int(input("Finished? Enter Number: "))
            except (ValueError, UnboundLocalError):
                print("Please Enter 1 for Yes and 2 for No")
            else:
                if finished < 1 or finished > 2:
                    print ("Please Enter a number between 1 and 2")
                elif finished == 1:
                    answer = True
                    break
                elif finished == 2:
                    answer = False
                    break
        return answer

if __name__ == '__main__':
    pass
