import urllib.request
import pandas as pd
from collections import namedtuple
import json
import os

OUTDIR = 'data/gov_data'

link1 = 'https://data.gov.il/api/action/datastore_search?resource_id=9eedd26c-019b-433a-b28b-efcc98de378d&limit=10000000'
link2 = 'https://data.gov.il/api/action/datastore_search?resource_id=9eedd26c-019b-433a-b28b-efcc98de378d&limit=10000000'

DFholder = namedtuple("DFholder", "link name")
holder_labs = DFholder(link1, 'isolations')
holder_isolations = DFholder(link2, 'labs_tests')

holders = [holder_labs,holder_isolations]

for holder in holders:
    try:
        with urllib.request.urlopen(holder.link) as url:
            s = url.read()

        s = json.loads(s.decode('utf-8'))

        records = s["result"]["records"]
        df = pd.DataFrame(records).set_index("_id")

        outfile = holder.name+'.csv'
        outpath = os.path.join(OUTDIR,outfile)
        df.to_csv(outpath)
    except:
        pass


