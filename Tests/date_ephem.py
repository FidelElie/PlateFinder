import ephem

date = "1973/23/11 15:30:21"
ephem_date = ephem.Date(date)
print(ephem_date)
print(repr(ephem_date))
