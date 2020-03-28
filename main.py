import pandas as pd
import os.path
import re
from datetime import date
from timeit import default_timer as timer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# adding the incognito argument to our webdriver
option = webdriver.ChromeOptions()
option.add_argument('— incognito')

# create a new instance of Chrome
browser = webdriver.Chrome(executable_path=r"C:\Users\roy\Desktop\chromedriver.exe", chrome_options=option)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
url = 'https://web.archive.org/web/20200101000000*/https://www.worldometers.info/coronavirus/'
browser.get(url)

# Handle a timeout
timeout = 50
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='search-toolbar-logo']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# The links that allready been downloaded are saved here, and should be exluded in this search
prev_refs = []
with open('refs.txt', 'r') as filehandle:
    prev_refs.append(filehandle.readline())

# Read all hrefs from html script
elems = browser.find_elements_by_xpath("//a[@href]")
refs = []
for elem in elems:
    ref = elem.get_attribute("href")
    pat = r'https://web.archive.org/web/\d+/https://www.worldometers.info/coronavirus/'
    match = re.search(pat,ref)
    if match:

        refs.append(match.group())

new_refs =  set(refs) - set(prev_refs)

# Iterate over hrefs and download tables from site
errors=[]
data_dir = 'data'
start = timer()

for i,ref in enumerate(new_refs):

    print(f"this is iteration {i+1} from {len(refs)}, "
          f"elapsed time in seconds is: {timer()-start}")

    try:
        data = pd.read_html(ref)
        date = "-".join(data[1][1].to_list())
        df = data[-1]
        df['ref'] = ref
        df['date'] = re.search("\d+",ref).group()

        outfile = date+'.csv'
        outpath = os.path.join(data_dir, outfile)
        df.to_csv(outpath)
    except:
        errors.append(ref)

end = timer()

# Write log to file
errors = "\n".join(errors)
date_str = date.today().strftime("%d/%m/%Y")
outfile = 'log_'+date_str+'.txt'
with open(outfile, 'w') as filehandle:
    filehandle.writelines(f"errors:\n {errors}\n")
    filehandle.writelines('\n---------------------\n')
    filehandle.writelines(f"time elapsed in seconds: {end-start}")

# Update refs files
outfile = 'refs.txt'
new_refs = "\n".join(new_refs)
with open(outfile, 'a') as filehandle:
    filehandle.write('\n')
    filehandle.write(new_refs)




