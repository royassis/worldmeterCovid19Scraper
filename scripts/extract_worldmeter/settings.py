# Imports
import os
from selenium import webdriver
import logging.config
from datetime import date

# Paths and Dirs
DATA_DIR = 'raw_data'
LOG_DIR = 'logs'
RESOURCE_DIR = 'resources'

OUTPUT_DIR = os.path.join(DATA_DIR,'worldmeter')

SITE_URL = 'https://www.worldometers.info/coronavirus/'
WAYBACK_URL = r'https://web.archive.org/web'
FULLPATH = WAYBACK_URL+"/*/"+SITE_URL

URL_REGEX_PATTERN = WAYBACK_URL+"\d{8}"+SITE_URL

LOGGER_CONFIG_FILE = 'file.conf'
LOG_CONFIG_PATH = os.path.join(RESOURCE_DIR, LOGGER_CONFIG_FILE)


# Selenium options
CHROMEDRIVER_PATH= os.path.join(RESOURCE_DIR, 'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('— incognito')
options.add_argument('--headless')


# Exluded urls
EXLUDED_URLS_FILE = 'excluded_urls.csv'
EXLUDED_URLS_PATH = os.path.join(RESOURCE_DIR,EXLUDED_URLS_FILE)

# Start logger
VERBOSE_LEVEL = 'INFO'

logging.config.fileConfig(fname=LOG_CONFIG_PATH, disable_existing_loggers=True)
logger = logging.getLogger('errorLogger')
logger.handlers[1].setLevel(VERBOSE_LEVEL)

# Date
todays_date = date.today().strftime("%Y%m%d")


