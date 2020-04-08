import pandas as pd

# Paths and Dirs
WORLDMETER_DATA = r'D:\PycharmProjects\scrap_corona_history\DW\raw_data\worldmeter'
GOV_RESOURCE_PATH = r'D:\PycharmProjects\scrap_corona_history\resources\gov_resource.csv'
CUTOFF_DATE = '2020-02-10'

MAPPER_PATH = r'D:\PycharmProjects\scrap_corona_history\resources\csv\column_remapper.csv'
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]

URLS_PATH  = r'D:\PycharmProjects\scrap_corona_history\resources\csv\urls.csv'
urls = pd.read_csv(URLS_PATH, index_col ='id')
GOVERNMENT_RESPONSE_URL = urls.loc[4,'url']

POPULATION_CSV_PATH = r'D:\PycharmProjects\scrap_corona_history\DW\raw_data\population_data.csv'

RESULTS_PATH = r'D:\PycharmProjects\scrap_corona_history\DW\loaded_data\worldmeterdata_transform_and_loaded.csv'
