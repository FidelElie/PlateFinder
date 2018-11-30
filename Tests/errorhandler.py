answers = ["Yes", "No"]
# list options numerically
list_options(answers)
while True:
    try:
        desired_option = int(input("Enter number corresponding to desired option: "))
    except (ValueError, UnboundLocalError):
        print ("Please enter a valid number")
    else:
        if desired_option < 1 or desired_option > 2:
            print ("Please enter a valid number of 1 or 2")
        else:
            # do something then
            break
