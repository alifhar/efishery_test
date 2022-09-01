import sys
import json
import pandas as pd
import numpy as np

#Extract Data
json_file = sys.argv
arr = open(json_file[1])
data = json.load(arr)
df = pd.DataFrame(data)

#Clean and transform komoditas
df = (df.set_index(df.columns.drop('komoditas',1).tolist())['komoditas']
		.str.replace(' dan |dll|nasi|sotobayam|soto|usus|kepala|uduk|pecel|goreng/bakar|merah|hitam|ikn|food|ikan |laut|goreng|uduk|,|/|&|\.',' ', regex=True)
		.str.replace('cumi-cumi','cumi', regex=True)
		.str.replace('gurame','gurami', regex=True)
		.str.replace('kembug','kembung', regex=True)
		.str.replace('lelw|ikanlele|kele','lele', regex=True)
		.str.replace('man|emas','mas', regex=True)
		.str.replace('muajir|mujaer|mujir|majaer|jaer','mujair', regex=True)
		.str.replace('nilam|nilem|nilaem|nil$','nila', regex=True)
		.str.replace('tingkol|tngkol','tongkol', regex=True)
		.str.replace(' +',' ', regex=True)
		.str.replace('^ | $','', regex=True)
		.str.split(' ', expand=True)
		.stack()
		.reset_index()
		.rename(columns={0:'komoditas'})
		#.loc[:, df.columns] 
	)

#Clean berat
df = ( df.set_index(df.columns.drop('berat',1).tolist())['berat']
		.str.replace('\D',' ', regex=True)
		.str.replace(' +','-', regex=True)
		.str.replace('^-|-$','', regex=True)
		.str.split('-', expand=True)
		.reset_index()
	)

#Transform berat
df['berat'] = np.where(df['level_1']==0, df.loc[:,0], 
			   np.where(df['level_1']==1, df.loc[:,1],
			   np.where(df['level_1']==2, df.loc[:,2],
			   np.where(df['level_1']==3, df.loc[:,3],
			   np.where(df['level_1']==4, df.loc[:,4],
			   np.where(df['level_1']==5, df.loc[:,5],
			   np.where(df['level_1']==6, df.loc[:,6],
			   np.where(df['level_1']==7, df.loc[:,7],
			   df.loc[:,8]))))))))


#SUM(berat) group by komoditas
df['berat'] = df['berat'].fillna(df.loc[:,0])
df['berat'] = pd.to_numeric(df['berat'])
df = df[['komoditas','berat']].groupby(['komoditas'])['berat'].sum().reset_index().sort_values(by=['berat'], ascending=False)
df = df.reset_index().loc[:, df.columns]
df['berat'] = df['berat'].astype("int").astype("string") + "kg"

#Set index
df.index = df.index+1
df['komoditas'] = df['komoditas'].replace('', np.nan)
df.dropna()

#Print Data
print(df)
#df.to_excel('test.xlsx')

arr.close()
