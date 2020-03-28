import pandas as pd
import glob
import re
import pprint
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

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
    '^Total Critical'       : 'Serious_Critical',
    '^Country,.*Other$'     : 'Country',
    '^Country,.*Territory'  : 'Country',
    '^Total Cured$'             : 'Total Recovered'
}


# Iterate and read csv files into df
path = r'data'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,0:]
    # Rename columns
    for pat, str in conversion_dict.items():
        df = df.rename(columns=lambda x: re.sub(pat, str, x, flags=re.IGNORECASE))

    extracted_date = re.search("\w\w\w-\d\d-\d\d\d\d", filename).group()
    date_object = datetime.datetime.strptime(extracted_date, "%b-%d-%Y").date()
    df["date"] = date_object
    df["date"] = pd.to_datetime(df["date"])

    # Append to df list
    li.append(df)


frame = pd.concat(li, ignore_index=True, sort=False)


(frame[frame.Country == 'Israel']).sort_values('date')