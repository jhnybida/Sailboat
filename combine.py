import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

df_YW = pd.read_csv('YW.csv')
df_SBD = pd.read_csv('SBD.csv')

df_YW['NAME'] = ''

for i in range(min(df_YW.Length),max(df_YW.Length)):
	boatnames = df_SBD.loc[(df_SBD.LOA.astype(float) > float(i-5)) & (df_SBD.LOA.astype(float) < float(i+5))].Name
	df_YW.loc[df_YW.Length.astype(int) == i,'NAME'] = df_YW.loc[df_YW.Length.astype(int) == i].MakeModel.map(lambda x: process.extractOne(x,boatnames, scorer=fuzz.token_set_ratio))
	print(i,end=',')

# split up name and score
df_YW['SCORE'] = df_YW.NAME.str[:-1].str.split(',').str[1]
df_YW['NAME'] = df_YW.NAME.str[1:].str.split(',').str[0]
df_YW['NAME'] = df_YW['NAME'].str[1:-1]						# remove '' from start and end of string

df_YW.loc[df_YW.SCORE.astype(float) < 90,'NAME'] = ''

df_YW = df_YW.merge(df_SBD, left_on='NAME', right_on='Name', how='left')

df_YW.set_index('ID',inplace=True)

df_YW.drop(['NAME','SCORE'],inplace=True,axis=1)

df_YW.to_csv('JOINED.csv')