import os
import pandas as pd

from selenium import webdriver

resource_dir = 'resources'
data_dir = 'data'

refs_handle = os.path.join(resource_dir,'refs.txt')

mapper_path = os.path.join(resource_dir, 'column_remapper.csv')
mapper = pd.read_csv(mapper_path, index_col = 'key', usecols = ['key','value'])
column_remapper = mapper.iloc[:,0]

urls_path = os.path.join(resource_dir, 'urls.csv')
urls = pd.read_csv(urls_path, index_col = 'id')
wayback_machine_corona_url = urls.loc[1,'url']
url_pattern = urls.loc[2,'url']


chromedriver_path=r"C:\Users\roy\Desktop\chromedriver.exe"

# adding the incognito argument to our webdriver
option = webdriver.ChromeOptions()
option.add_argument('— incognito')
