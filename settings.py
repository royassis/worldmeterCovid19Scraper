import os
import pandas as pd
from selenium import webdriver

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

resource_dir = 'resources'
data_dir = 'data'
log_dir = 'logs'

chromedriver_path=r"C:\Users\roy\Desktop\chromedriver.exe"
option = webdriver.ChromeOptions()
option.add_argument('— incognito')

hrefs_path = os.path.join(resource_dir, 'refs.csv')
hrefs = pd.read_csv(hrefs_path, index_col ='id')

mapper_path = os.path.join(resource_dir, 'column_remapper.csv')
mapper = pd.read_csv(mapper_path, index_col = 'key', usecols = ['key','value'])
column_remapper = mapper.iloc[:,0]

urls_path = os.path.join(resource_dir, 'urls.csv')
urls = pd.read_csv(urls_path, index_col = 'id')
wayback_machine_corona_url = urls.loc[1,'url']
url_pattern = urls.loc[2,'url']



