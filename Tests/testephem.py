import ephem
# string = "-2360"
# string = string + "23"
# mod_string = []
# for i in range(0, len(string)):
#     if (i == 2 or i == 4):
#         mod_string.append(":")
#     mod_string.append(string[i])
# new_string = "".join(mod_string)

# print(new_string)

# ra = ephem.hours(new_string)

# print (ra)

test_string = "19730720"
mod_string = []
for i in range(0, len(test_string)):
    if (i == 4 or i == 6):
        mod_string.append("/")
    mod_string.append(test_string[i])
new_string = "".join(mod_string)

print(new_string)

date = ephem.Date(new_string)
print (date + 1)
print (repr(date))

