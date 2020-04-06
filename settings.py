# Imports
import os
import pandas as pd
from selenium import webdriver
import logging.config


# Pandas options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Options
VERBOSE_LEVEL = 'INFO'

# Paths and Dirs
DATA_DIR = 'data'
LOG_DIR = 'logs'

CUTOFF_DATE = '2020-02-10'

RESOURCE_DIR = 'resources'
CHROMEDRIVER_PATH= os.path.join(RESOURCE_DIR, 'chromedriver.exe')
POPULATION_PATH = os.path.join(RESOURCE_DIR, 'population.csv')
URLS_PATH = os.path.join(RESOURCE_DIR, 'urls.csv')

RESULTS_DIR = 'results'
RESULTS_FILE = 'all_dates.csv'
RESULTS_PATH = os.path.join(RESULTS_DIR, RESULTS_FILE)

MAPPER_FILE = 'column_remapper.csv'
MAPPER_PATH = os.path.join(RESOURCE_DIR, MAPPER_FILE)

CONFIG_FILE = 'file.conf'
LOG_CONFIG_PATH = os.path.join(RESOURCE_DIR, CONFIG_FILE)


# Selenium options
options = webdriver.ChromeOptions()
options.add_argument('— incognito')
options.add_argument('--headless')


# Read CSV's
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]
urls = pd.read_csv(URLS_PATH, index_col ='id')

WAYBACK_MACHINE_CORONA_URL = urls.loc[7, 'url']
URL_REGEX_PATTERN = urls.loc[2, 'url']
GOVERNMENT_RESPONSE_URL = urls.loc[4,'url']

#https://web.archive.org/web/*/https://www.worldometers.info/coronavirus/
# Start error_logger
logging.config.fileConfig(fname=LOG_CONFIG_PATH, disable_existing_loggers=False)
error_logger = logging.getLogger('errorLogger')
verbose_logger = logging.getLogger('root')

verbose_logger.setLevel(VERBOSE_LEVEL)

