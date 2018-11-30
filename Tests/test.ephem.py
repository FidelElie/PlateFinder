import ephem 
from Libraries.Sorter import Converter

if __name__== '__main__':
    # sorter = Converter(- 31, 149, "UJ 3684P P1 112  41602410-3000771017 343IIIaJ NONE   700AI3  1N")
    # entries_s = sorter.check_invalid_entries()
    # if entries_s == False:
    #     print ("Plate Not Suitable: Missing Data")
    # elif entries_s == False:
    #     print ("Plate Not Suitable: Quality Is Too Low")
    # else:
    #     plate_data = sorter.convert()

    # print (plate_data)

    # time_of_exp = plate_data[3] 
    # date_of_exp = plate_data[2]
    # exp_duration = plate_data[4]
    # string_change = []
    # for i in range(0,len(date_of_exp)):
    #     string_change.append(date_of_exp[i])
    #     if i == 1 or i == 3:
    #         string_change.append("/")

    # date_of_exp = "19" + "".join(string_change)
    # half_time_of_exp = time_of_exp + (exp_duration / (3600 * 2))
    # half_time_of_exp = str(sorter.dhours_to_hms(half_time_of_exp))
    # total_date = date_of_exp + " " + half_time_of_exp
    # """Setting Ephem"""
    # # sets the observer location and the date
    # observatory = ephem.Observer()
    # observatory.lat, observatory.lon = -31, 149
    # observatory.date = total_date
    # observatory.epoch = '1950'
    # # print (total_date)
    # # computes the data
    # # mars = ephem.Mars()
    # mars = ephem.Mars(observatory)
    # # print (values)
    # print (mars.ra.norm, mars.dec.norm)

    mars = ephem.Mars()
    mars.compute("2018/10/03")
    print(mars.ra.norm, mars.dec.norm)
