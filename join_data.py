import pandas as pd
import glob

path = r'data'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=[0], header=0)
    df = df.iloc[:,1:]
    li.append(df)

[df.shape for df in li]
frame = pd.concat(li[:-10], axis=0, ignore_index=True,sort=True)