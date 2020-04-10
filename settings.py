import pandas as pd
import os

current_dir = os.path.dirname(__file__)

# Paths and Dirs
WORLDMETER_DATA = os.path.join(current_dir,'DW/raw_data/worldmeter')
GOV_RESOURCE_PATH = os.path.join(current_dir,'resources/csv/gov_resource.csv')
CUTOFF_DATE = '2020-02-10'

MAPPER_PATH = os.path.join(current_dir,'resources/csv/column_remapper.csv')
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]

URLS_PATH  = os.path.join(current_dir,'resources/csv/urls.csv')
urls = pd.read_csv(URLS_PATH, index_col ='id')
GOVERNMENT_RESPONSE_URL = urls.loc[4,'url']

POPULATION_CSV_PATH = os.path.join(current_dir,'DW/raw_data/population_data.csv')

GOV_DATE_RESULTS_DIR = os.path.join(current_dir,'DW/loaded_data','all_dates.csv')
RESULTS_PATH = os.path.join(GOV_DATE_RESULTS_DIR,'all_dates.csv')
RESULTS_PATH_SEIR = os.path.join(GOV_DATE_RESULTS_DIR,'all_dates_seir.csv')

GOV_DATE_PATH = os.path.join(current_dir,'DW/raw_data/gov_data')