import re
from datetime import date
from timeit import default_timer as timer
from settings import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# create a new instance of Chrome
browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
browser.get(wayback_machine_corona_url)

# Handle a timeout
timeout = 50
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='search-toolbar-logo']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# The links that allready been downloaded are saved here, and should be exluded in this search
prev_refs = [line.rstrip('\n') for line in open(refs_handle)]

# Read all hrefs from html script
elems = browser.find_elements_by_xpath("//a[@href]")
refs = []
for elem in elems:
    ref = elem.get_attribute("href")
    match = re.search(url_pattern,ref)
    if match:
        refs.append(match.group())

new_refs =  set(refs) - set(prev_refs)

# Iterate over hrefs and download tables from site
errors=[]
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
log_dir = 'logs'
errors = "\n".join(errors)
date_str = date.today().strftime("%d%m%Y")
outfile = date_str+'.txt'
outpath = os.path.join(log_dir,outfile)
with open(outpath, 'w+') as filehandle:
    filehandle.writelines(f"errors:{errors}")
    filehandle.writelines('\n---------------------\n')
    filehandle.writelines(f"time elapsed in seconds: {end-start}")
    filehandle.writelines('\n---------------------\n')

# Update refs files
outpath = r'resources\refs.txt'
new_refs = "\n".join(new_refs)
with open(outpath, 'a') as filehandle:
    filehandle.write(new_refs)




