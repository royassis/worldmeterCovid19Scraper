from settings import *
import glob
import re
import pprint
import datetime


pp = pprint.PrettyPrinter(indent=4)

conversion_dict= column_remapper.to_dict()

# Iterate and read csv files into df
all_files = glob.glob(data_dir + "/*.csv")
df_list = []

for filename in all_files:

    # Discard first column due to it contains id information
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,0:]

    # Iterate over column mapper and rename columns names to desired names
    for pat, str in conversion_dict.items():
        df = df.rename(columns=lambda x: re.sub(pat, str, x, flags=re.IGNORECASE))

    # Convert the filename which contains a date format to a date object and append as a column
    extracted_date = re.search("\w\w\w-\d\d-\d\d\d\d", filename).group()
    date_object = datetime.datetime.strptime(extracted_date, "%b-%d-%Y").date()
    df["date"] = date_object
    df["date"] = pd.to_datetime(df["date"])

    # Append to df list
    df_list.append(df)

# Join df from all dates
frame = pd.concat(df_list, ignore_index=True, sort=False)
# Remove plus sign from "New Cases" col
frame['New Cases'] = frame['New Cases'].str.extract('(\d+)')
# Sort df by date
frame = frame.sort_values('date')
# Remove the totalrow
frame = frame[frame["Country"] != 'Total:']

