# Imports
import os
from selenium import webdriver
import logging.config
from datetime import date

# Paths and Dirs
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
LOG_CONFIG_PATH = r"ETL_scripts/extract_worldmeter/resources/"
LOG_FILENAME = "logger.conf"
os.chmod(LOG_CONFIG_PATH, 0o777)
VERBOSE_LEVEL = 'INFO'
logging.config.fileConfig(fname=LOG_CONFIG_PATH, disable_existing_loggers=True)
logger = logging.getLogger('errorLogger')
logger.handlers[1].setLevel(VERBOSE_LEVEL)

# Date
todays_date = date.today().strftime("%Y%m%d")

