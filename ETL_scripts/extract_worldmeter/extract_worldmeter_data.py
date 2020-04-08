from ETL_scripts.extract_worldmeter.utils.functions import *
from selenium import webdriver

# create a new instance of Chrome
logging.info('>>Opening chromium in background')
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
logging.info(f'>>Connecting to URL..waiting for response')
browser.get(WAYBACK_FULLPATH)

# Handle a timeout
timeout_get_request(browser, 50)

# Get only new raw_data
logging.info('>>Checking for new links in URL')
prev_urls = get_prev_urls(OUTPUT_DIR)
all_urls = get_all_urls_matching_regex(browser, URL_REGEX_PATTERN)
new_urls = get_fresh_urls(all_urls, prev_urls, excluded_urls)

# Iterate over hrefs and download tables from site
if new_urls:
    logging.info(f'>>Downloading data from links: {len(new_urls)} files')
    download_csv_from_all_urls(new_urls)
else:
    logging.info('>>No new links')


logging.info('>>Quitting chromium')
logging.info('>>End program')
browser.quit()
