import os
import time

last_mod_date = os.path.getmtime("Ephemeris Cache")
diff_mod = (time.time() - last_mod_date) / 3600
if diff_mod > 1.0:
    print ("Files being purged")
