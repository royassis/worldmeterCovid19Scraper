from settings import *
import glob
import re
import datetime


# --------------------
# Merge all seperate data files
# --------------------
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
disease_data = pd.concat(df_list, ignore_index=True, sort=False)
# Remove plus sign from "New Cases" col
disease_data['New Cases'] = disease_data['New Cases'].str.extract('(\d+)')
# Sort df by date
disease_data = disease_data.sort_values('date')
# Remove the totalrow
disease_data = disease_data[disease_data["Country"] != 'Total:']
# Get only reliable data (from 10.2 and so on)
cutoff_date = '2020-02-10'
disease_data = disease_data[disease_data["date"] >= cutoff_date]
#
disease_data['Country'] = disease_data['Country'].str.lower()
#
disease_data.columns = disease_data.columns.str.lower().str.replace("\s+", "_")

# --------------------
# Get world_population data from the web
# --------------------
world_population = pd.read_html(io=read_world_population_data.url,
                                match=read_world_population_data.match,
                                attrs = read_world_population_data.attrs)
world_population = world_population[0]

# Select and rename cols
world_population = world_population[read_world_population_data.cols]
world_population = world_population.rename(read_world_population_data.mapping, axis = 1)

# Fix countries col names
pat = r'(\[.*\])|(\(.*\))'
world_population['country'] = world_population['country'].str.replace(pat, '')\
                            .str.replace('\s+',' ')\
                            .str.strip()\
                            .str.lower()

# --------------------
# Join data and world_population data
# --------------------
all_data = disease_data.merge(world_population)
all_data['healthy_total'] = all_data['world_population'] - all_data['total_cases']
all_data = all_data[output_cols]

# --------------------
# # Output to dile
# --------------------
all_data.to_csv(outfile)




