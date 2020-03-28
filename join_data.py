import pandas as pd
import glob
import re
import pprint
import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pp = pprint.PrettyPrinter(indent=4)

mapper_path = r'D:\PycharmProjects\scrap_corona_history\resources\column_remapper2.csv'
mapper = pd.read_csv(mapper_path, index_col = 'key', usecols = ['key','value'])
mapper = mapper.iloc[:,0]

conversion_dict= mapper.to_dict()


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

# Join df from all dates
frame = pd.concat(li, ignore_index=True, sort=False)
# Remove plus sign from "New Cases" col
frame['New Cases'] = frame['New Cases'].str.extract('(\d+)')
# Sort df by date
frame = frame.sort_values('date')
# Remove the totalrow
frame = frame[frame["Country"] != 'Total:']

