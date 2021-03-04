import pandas as pd
import numpy as np
#load the first file, delete the column which we don`t want. Change the columns` name according our common sense
#contain temp, humidity, sunhour, wind speed
df1 = pd.read_csv("C:\\Users\\莫笙\\OneDrive\\文档\\2020 Fall\BIO3SA3\\temperature_dataframe.csv")
df1 = df1.rename(columns={"Cites":"City","Date":"Day",'Unnamed: 2':'Regions'})
#print(df1)
df1 = df1.drop(df1.columns[0:2],axis = 1)
df1 = df1.drop(df1.columns[2:4],axis = 1)


#build time transform dic, we want to view date as continuous variable
Time_transform = {}
Time_list = df1['Day'].unique()
i = 1
for time in Time_list:
    Time_transform[time] = i
    i = i+1
print(Time_transform)

saved_date = [32,39,46,53,60]
#search the regions column. This column actually contain the region for each country,
#however, we want to focus on city, this column is badly affecting us, so we only want to save the row with NaN value
#or we save the row with same 'Regions' and 'City', like beijing.
for index , row in df1.iterrows():
    df1.loc[index,('Day')] = Time_transform[row['Day']]
    if row['Regions'] is not np.nan and row['Regions'] != row['City']:
        df1 = df1.drop(index)
    elif Time_transform[row['Day']] not in saved_date:
        df1 = df1.drop(index)

#find out if we have successed
print(sum(df1['Regions'].isna()))
#their is no problem, then we can delete 'regions' column
df1 = df1.drop('Regions',axis = 1)
#fill the blank with zero if blank exist
df1.fillna(0)
df1
#rename day so that it start at 1
#We accidentally replace the day 60 to 30, which should be 28. We fixed it in R studio
df2 = df1.replace({'Day' : {32:1, 39:7, 46:14, 53:21, 60:30}})

#load the second document
#contain population
df3 = pd.read_csv("C:\\Users\\莫笙\\OneDrive\\文档\\2020 Fall\\BIO3SA3\\covid(1)\\worldometer_data.csv")
df3 = df3[['Country/Region','Population']]  #select columns
df3 = df3.rename(columns = {'Country/Region':'Country'})  #Change columns` name
df3 = df3.dropna()   #delete the row with NaN Population
#the value of populaiton is too high, it is necessary to scale down the value, we use log(population) instead of population
for index , row in df3.iterrows():
    df3.loc[index,('Population')] = np.log(int(row['Population']))
df3

#merge df2 and df3
df_merge_1 = pd.merge(df2,df3,on=['Country'])
#print(sum(df_merge_1['Date'].isna()))
df_merge_1

#output excel document
df_merge_1.to_excel(r'C:\Users\莫笙\OneDrive\文档\2020 Fall\BIO3SA3\Final\NEW\Covid_data1.xlsx', index = False)
#save it as .csv and then import in R studio for further process and analysis
