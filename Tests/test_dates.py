from datetime import datetime
import numpy as np

"""
Code block for datetime manipulation and template for custom input
"""
print ("Date Format: Year/Month/Day Hour:Minute:Second")
while True:
    # both values will only have to be changed to inputs for the custom aspect.
    date_string_start = "1984/12/21 15:00" 
    date_string_end = "1994/12/21 15:00"
    if len(date_string_start.split(" ")[1]) != 3:
        date_string_start = date_string_start + ":00"
    if len(date_string_end.split(" ")[1]) != 3:
        date_string_end = date_string_end + ":00"
    try:
        date_string_start = datetime.strptime(date_string_start, '%Y/%m/%d %H:%M:%S')
        date_string_end = datetime.strptime(date_string_end, '%Y/%m/%d %H:%M:%S')
        break
    except ValueError:
        print ("Please enter date in format 'Year/Month/Day Hour:Minute:Second Eg: 1996/10/11 07:00:00'")
"""
Code block for a user defined timestep
"""
while True:
    desired_step = input("Enter Time Desired Step : ").split(" ")
    time_values = []
    if len(desired_step) == 1:
        desired_step.append("Seconds")
    for i in range(1, len(desired_step), 2):
        try:
            int(desired_step[i - 1])
        except ValueError:
            print ("Invalid Parameter given for timestep")
        else:
            if desired_step[i].lower() == "days":
                time_values.append(int(desired_step[i - 1]) * 86400)
            elif desired_step[i].lower() == "minutes" or desired_step[i] == "mins" or desired_step[i] == "m":
                time_values.append(int(desired_step[i - 1]) * 3600)
            elif desired_step[i].lower() == "seconds" or desired_step[i] == "s":
                time_values.append(int(desired_step[i - 1]))
            else:
                print ("Error in entering time step please try again")
                break
    if len(time_values) == len(desired_step) / 2:
        time_step = sum(time_values)
        break
"""
Code block for creating array of datetimes
"""
#Kept these lines as an example of unpacking parameters to a function
# starting_date = datetime(*start_datetime)
# ending_date = datetime(*end_datetime)
         
time_interval = datetime.timedelta(seconds=time_step)

dates = []

# printing the starting date back in the entered format
# print(starting_date.strftime('%Y/%m/%d %H:%M:%S'))

while starting_date < ending_date:
    dates.append(starting_date.strftime('%Y/%m/%d %H:%M:%S'))
    starting_date += time_interval

dates = np.asarray(result)

