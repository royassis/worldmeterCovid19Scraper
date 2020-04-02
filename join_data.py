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
# Get only reliable data (from 10.2 and so on)
cutoff_date = '2020-02-10'
frame = frame[frame["date"] >= cutoff_date]
#
frame['Country'] = frame['Country'].str.lower()
#
frame.columns = frame.columns.str.lower().str.replace("\s+","_")

# Get population data
world_pop = pd.read_html(population_data)
world_pop = world_pop[0]
world_pop = world_pop[['Country (or dependent territory)','Population']]
world_pop = world_pop.rename({'Country (or dependent territory)':'country',
                'Population':'population'}, axis = 1)
world_pop = world_pop[['country','population']]

# Fix countries names - get strings not inclosed in brackets or parentheses
pat = r'(\[.*\])|(\(.*\))'
world_pop['country'] = world_pop['country'].str.replace(pat,'')\
                            .str.replace('\s+',' ')\
                            .str.strip()\
                            .str.lower()

# Join data
frame = frame.merge(world_pop)
frame['healthy_total'] = frame['population'] - frame['total_cases']
cols = ['country','date','total_cases','total_deaths','total_recovered','serious_critical','population','healthy_total']
frame = frame[cols]

# Output to dile
outfile = 'all_dates.csv'
frame.to_csv(outfile)
