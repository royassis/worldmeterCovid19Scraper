import pandas as pd
import glob
import re

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
    '.*\sCases'         : 'NewCases',
    '^Cases$'           : 'NewCases',
    '^Change.*Cases'    : 'NewCases'
}

for pat,str in conversion_dict.items():
    frame = frame.rename(columns=lambda x: re.sub(pat,str,x))