import pandas as pd
import glob
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

path = r'data'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,1:]
    li.append(df)

li[-1].columns

frame = pd.concat(li[:-10], axis=0, ignore_index=True,sort=True)


conversion_dict={
    '.*\sCases'             : 'New Cases',
    '^Cases$'               : 'New Cases',
    '^Change.*Cases.*'      : 'New Cases',
    '^New Today$'           : 'New Cases',
    '^Change Today$'        : 'New Cases',

    'ActiveCases'           : 'Total Cases',
    'TotalCases'            : 'Total Cases',

    '.*\sDeaths'            : 'Total Deaths',
    '^TotalDeaths$'         : 'Total Deaths',

    '^Change.*Deaths.*'     : 'New Deaths',

    'Serious.*,.*Critical'  : 'Serious_Critical',

    'TotalRecovered'        : 'Total Recovered'

}

for pat,str in conversion_dict.items():
    frame = frame.rename(columns=lambda x: re.sub(pat,str,x, flags=re.IGNORECASE))

pp.pprint(set(frame.columns))