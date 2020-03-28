import pandas as pd
import glob
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

conversion_dict={
    '^Cases$'               : 'New Cases',
    '^Change \(cases\)$'    : 'New Cases',
    '^Change \(deaths\)$'   : 'New Deaths',
    '^Change Today$'        : 'New Cases',
    '^Deaths$'              : 'Total Deaths',
    '^Feb.*Cases$'          : 'New Cases',
    '^Feb.*Deaths$'         : 'New Deaths',
    '^New Today$'           : 'New Cases',
    '^NewCases$'            : 'New Cases',
    '^NewDeaths'            : 'New Deaths',
    'Serious.*,.*Critical'  : 'Serious_Critical',
    r'^Today\'s Deaths$'    : 'New Deaths',
    '^TotalCases$'          : 'Total Cases',
    '^TotalDeaths$'         : 'Total Deaths',
    'TotalRecovered'        : 'Total Recovered',
    '^Total Severe$'        : 'Serious_Critical',
    '^Total Critical'       : 'Serious_Critical'
}


# Iterate and read csv files into df
path = r'data'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,1:]

    # Rename columns
    for pat, str in conversion_dict.items():
        df = df.rename(columns=lambda x: re.sub(pat, str, x, flags=re.IGNORECASE))

    # Append to df list
    li.append(df)

pp.pprint([df.columns.to_list()for df in li])
print(*[df.columns.to_list()for df in li[-4:]], sep='\n\n')

frame = pd.concat(li, ignore_index=True, sort=False)

[df.shape for df in li]

pp.pprint(set(frame.columns))