import timeit
from functions import *
from selenium import webdriver


# create a new instance of Chrome
browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
browser.get(wayback_machine_corona_url)

# Handle a timeout
handle_timeout(browser, 50)

# The links that allready been downloaded are saved here, and should be exluded in this search
prev_refs = [line.rstrip('\n') for line in open(refs_handle)]

# Read all hrefs from html script
new_refs =  get_new_refs(browser,prev_refs,url_pattern)


# Iterate over hrefs and download tables from site
start = timeit.timeit()
errors = iterate_over_hrefs_and_write_to_file(new_refs)
end = timeit.timeit()
delta = end - start

# Write log to file
write_log(errors, delta, log_dir)

outpath = os.path.join(resource_dir, 'refs.txt')
update_ref_log(outpath,new_refs)



