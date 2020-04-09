# Imports
import os
from selenium import webdriver
import logging.config
from datetime import date
import pathlib

# Paths and Dirs
RESOURCE_PATH = 'resources'
OUTPUT_PATH = r'D:\PycharmProjects\scrap_corona_history\DW\raw_data\worldmeter'

SITE_URL = 'https://www.worldometers.info/coronavirus/'
WAYBACK_URL_BASE = r'https://web.archive.org/web'
WAYBACK_FULLPATH = WAYBACK_URL_BASE + "/*/" + SITE_URL
URL_REGEX_PATTERN = WAYBACK_URL_BASE + "/\d{8}/" + SITE_URL

# Selenium options
CHROMEDRIVER_PATH= os.path.join(RESOURCE_PATH,'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('— incognito')
options.add_argument('--headless')


# Exluded urls
EXLUDED_URLS_PATH = os.path.join(RESOURCE_PATH,'excluded_urls.csv')
with open(EXLUDED_URLS_PATH) as f:
    excluded_urls = f.read().splitlines()

# Start logger
CONFIG_PATH = os.path.join(RESOURCE_PATH,'logger.conf')
# VERBOSE_LEVEL = logging.INFO
# logging.basicConfig(level=VERBOSE_LEVEL)
logging.config.fileConfig(fname=CONFIG_PATH, disable_existing_loggers=False)


# Date
todays_date = date.today().strftime("%Y%m%d")

