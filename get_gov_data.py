import urllib.request
import pandas as pd
import json
import os

OUTDIR = r'D:\PycharmProjects\scrap_corona_history\data\gov_data'
RECORDS_LIMIT = 10000000

df = pd.read_csv('resources/gov_resource.csv')

df['datastore_structure'] = df['resource_id'].apply(lambda x: {'resource_id': x,'limit':RECORDS_LIMIT})\
                                              .apply(lambda x: str.encode(json.dumps(x)))

for _, entry in df.iterrows():
    response  = urllib.request.urlopen(entry["url"], entry['datastore_structure'])
    s = json.loads(response.read())
    records = s["result"]["records"]

    data = pd.DataFrame(records).set_index("_id")

    outfile = ".".join([entry['name'], 'csv'])
    outpath = os.path.join(OUTDIR,outfile)
    data.to_csv(outpath)

