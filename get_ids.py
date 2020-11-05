import numpy as np
import pandas as pd

#create master dataframe from imdb zip file
df = pd.read_csv('title.basics.tsv.gz', sep='\t',low_memory=False)

#filter dataframe for relevant entries
movies_df = df.loc[((df['titleType'] == 'movie') | 
                    (df['titleType'] == 'tvMovie')) & 
                    (df['isAdult'] == 0) & 
                    (df['startYear'] > '1950')]

#create np array of unique title url codes
title_codes = movies_df.tconst.unique()
