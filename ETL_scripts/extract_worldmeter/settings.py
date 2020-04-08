# Imports
import os
from selenium import webdriver
import logging.config
from datetime import date

# Paths and Dirs
DATA_DIR = 'raw_data'
LOG_DIR = 'logs'
RESOURCE_DIR = 'resources'

OUTPUT_PATH = r'D:\PycharmProjects\scrap_corona_history\DW\raw_data\worldmeter'

SITE_URL = 'https://www.worldometers.info/coronavirus/'
WAYBACK_URL_BASE = r'https://web.archive.org/web'
WAYBACK_FULLPATH = WAYBACK_URL_BASE + "/*/" + SITE_URL

URL_REGEX_PATTERN = WAYBACK_URL_BASE + "/\d{8}/" + SITE_URL

# Selenium options
CHROMEDRIVER_PATH= os.path.join(r'D:\PycharmProjects\scrap_corona_history\ETL_scripts\extract_worldmeter\resources\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('— incognito')
options.add_argument('--headless')


# Exluded urls
EXLUDED_URLS_PATH = r'D:\PycharmProjects\scrap_corona_history\ETL_scripts\extract_worldmeter\resources\excluded_urls.csv'
with open(EXLUDED_URLS_PATH) as f:
    excluded_urls = f.read().splitlines()

# Start logger
VERBOSE_LEVEL = logging.INFO
logging.basicConfig(level=VERBOSE_LEVEL)

# Date
todays_date = date.today().strftime("%Y%m%d")

