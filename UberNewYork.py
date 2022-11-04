# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 09:38:07 2022

@author: Carolina
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir(r'D:\Educación\Cursos\Cursos Análisis de Datos\ProjectsDataAnalysis\UberNewYork\uber-pickups-in-new-york-city')

uber_15= pd.read_csv('uber-raw-data-janjune-15.csv', encoding='utf-8')
                  
uber_15.head(2) 

uber_15.shape

# --------------Prepare Data------------------

# Count and drop duplicates

uber_15.duplicated().sum()

uber_15.drop_duplicates(inplace=True)

uber_15.shape


# Which month have the max. Uber pickups in New York City?

uber_15.dtypes

# convert Pickup_date to datetime 

uber_15['Pickup_date'] = pd.to_datetime(uber_15['Pickup_date'], format = '%Y-%m-%d %H:%M:%S') 

uber_15['Pickup_date'].dtypes

uber_15['month'] = uber_15['Pickup_date'].dt.month

uber_15['month'].value_counts().plot(kind='bar')

# Total trips for each month and each weekdays

uber_15['weekday'] = uber_15['Pickup_date'].dt.day_name()
uber_15['day'] = uber_15['Pickup_date'].dt.day
uber_15['hour'] = uber_15['Pickup_date'].dt.hour
uber_15['month'] = uber_15['Pickup_date'].dt.month
uber_15['minute'] = uber_15['Pickup_date'].dt.minute

uber_15.head()

temp = uber_15.groupby(['month','weekday'], as_index=False).size()
temp.head()

temp['month'].unique()

dict_month = {1:'Jan', 2:'Feb', 3:'March', 4:'April', 5:'May', 6:'June'}

temp['month']=temp['month'].map(dict_month)
temp['month']

plt.figure(figsize=(12,8))
sns.barplot(x='month',y='size',hue='weekday',data=temp)

# Find out hourly rush in New York city in all days  

uber_15.groupby(['weekday', 'hour']).count()

summary = uber_15.groupby(['weekday', 'hour'], as_index=False).size()

summary

sns.pointplot(x='hour',y='size',hue='weekday',data=summary)


# Collect data and make it ready for the data analysis
 

import os

files = os.listdir(r'D:\Educación\Cursos\Cursos Análisis de Datos\ProjectsDataAnalysis\UberNewYork\uber-pickups-in-new-york-city')[-7:]

files

files.remove('uber-raw-data-janjune-15.csv')

path = r'D:\Educación\Cursos\Cursos Análisis de Datos\ProjectsDataAnalysis\UberNewYork\uber-pickups-in-new-york-city'

final = pd.DataFrame()

for file in files:
    current_df = pd.read_csv(path+'/'+file,encoding='utf-8')
    final=pd.concat([current_df,final])

final.head(2)

# Remove duplicate

final.duplicated().sum()

final.drop_duplicates(inplace=True)

# what location of New York City we are getting rush?

rush_uber = final.groupby(['Lat','Lon'],as_index=False).size()

import folium

basemap = folium.Map()

from folium.plugins import HeatMap

HeatMap(rush_uber).add_to(basemap)

basemap

# Examine rush on hour and weekday (Perform pair wise analysis)

final['Date/Time'] = pd.to_datetime(final['Date/Time'],format = '%m/%d/%Y %H:%M:%S')

final['weekday']=final['Date/Time'].dt.day
final['hour']=final['Date/Time'].dt.hour

final.head(3)

pivot = final.groupby(['weekday','hour']).size().unstack()

pivot

pivot.style.background_gradient()

# Automate the analysis

def gen_pivot_table(df,col1,col2):
    pivot = final.groupby([col1,col2]).size().unstack()
    return pivot.style.background_gradient()

gen_pivot_table(final,'weekday','hour')
    




