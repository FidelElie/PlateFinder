from robobrowser import RoboBrowser
import requests
import gzip
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import shutil

def unzip(url):
    r = requests.get(url, stream = True)
    print (r.url)
    file_name = r.url.split("/")[-1].replace(".gz","")
    if r.status_code == 200:
        path = "test.fits"
        with open(path, 'wb') as f:
            r.raw.decode_content = True 
            gzip_file = gzip.GzipFile(fileobj=r.raw)
            shutil.copyfileobj(gzip_file, f)
    return r.content

def browser_stuff():
    browser = RoboBrowser(parser='html.parser')
    browser.open('http://www-wfau.roe.ac.uk/sss/pixel.html')
    form = browser.get_form()
    form['coords'].value = "00 05 53.9 -34 45 08"
    form['size'].value = "15"
    form['equinox'].value = "1"
    print(form['waveband'].options)
    browser.submit_form(form)
    download_link = str(browser.find("a"))
    download_link = download_link.split(" ")[1].split("\"")[1]
    return download_link

if __name__ == '__main__':
    x = browser_stuff()
    # file_used = unzip(x)
    # print (file_used())
    # print(file_data)
    # hdu_list = fits.open("test.fits", ignore_missing_end=True)
    # image_data = hdu_list[0].data
    # plt.imshow(image_data, cmap='gray')
    # plt.colorbar()
    # plt.show()


