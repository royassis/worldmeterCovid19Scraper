import pandas as pd
import os.path
import re
from timeit import default_timer as timer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


option = webdriver.ChromeOptions()
option.add_argument('— incognito')

browser = webdriver.Chrome(executable_path=r"C:\Users\roy\Desktop\chromedriver.exe", chrome_options=option)

url = 'https://web.archive.org/web/20200101000000*/https://www.worldometers.info/coronavirus/'
browser.get(url)

# timeout = 20
# try:
#     WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class=’avatar width-full rounded-2']")))
# except TimeoutException:
#     print("Timed out waiting for page to load")
#     browser.quit()


# Read all hrefs from html script
elems = browser.find_elements_by_xpath("//a[@href]")
refs = []
for elem in elems:
    ref = elem.get_attribute("href")
    pat = r'https://web.archive.org/web/\d+/https://www.worldometers.info/coronavirus/'
    match = re.search(pat,ref)
    if match:

        refs.append(match.group())

# Iterate over hrefs and download tables from site
errors=[]
data_dir = 'data'
start = timer()

for i,ref in enumerate(refs):

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

# Write erros to file
errors = "\n".join(errors)
with open('errors.txt', 'w') as filehandle:
    filehandle.writelines(f"errors:\n {errors}\n")
    filehandle.writelines('\n---------------------\n')
    filehandle.writelines(f"time elapsed in seconds: {end-start}")




import glob

path = r'data'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,1:]
    li.append(df)

[df.shape for df in li]
frame = pd.concat(li[:-10], axis=0, ignore_index=True,sort=True)