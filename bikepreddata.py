# -*- coding: utf-8 -*-
"""BikePredData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_K4OZ4iarFgpSd9dQa6fk1PjnCJaXpwJ
"""

# !pip install pyproj
# !pip install geopy


import numpy as np
import pandas as pd
import os

# from pyproj import Proj, transform

# import geopy
# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter

pd.set_option("max_columns",64)
df=pd.read_csv("BikePedCrash.csv")
# print(df.head(3))
# print(df.columns)

# to remove duplicate columns like 'OBJECTID','Longitude','Latitude'
# print(df.shape)
df=df.T.drop_duplicates() # we first transpose the data and then drop the dupliacte rows .Again transpose the data
df=df.T
# print(df.shape)

# print(df.columns)

# """Columns "BikeAgeGrp" had inconsistent values, so we are dropping that coulmn, and creating a new columns again "BikeAgeGrp" based on BikeAge columns using conditions"""
df.drop(columns=["BikeAgeGrp"],inplace=True)

# Dividing the dataframe into two parts , based on age values

filer_condition=df.loc[(df['BikeAge']=="Unknown")|(df['BikeAge']=="70+")].index
df_filter=df.drop(filer_condition)
df_filter['BikeAge']=df_filter['BikeAge'].astype('int')

# create a list of our conditions
conditions = [
    (df_filter['BikeAge']>= 0) & (df_filter['BikeAge'] <= 20),
    (df_filter['BikeAge']>= 21)& (df_filter['BikeAge'] <= 30),
    (df_filter['BikeAge'] >= 31) & (df_filter['BikeAge'] <= 40),
    (df_filter['BikeAge'] >= 41) & (df_filter['BikeAge'] <= 50),
    (df_filter['BikeAge'] >= 51) & (df_filter['BikeAge'] <= 60),
    (df_filter['BikeAge'] >= 61) & (df_filter['BikeAge'] <= 70),
    (df_filter['BikeAge'] > 70) & (df_filter['BikeAge'] !=999 ),
     (df_filter['BikeAge'] == 999)]

# create a list of the values we want to assign for each condition
values = ['0-20', '21-30', '31-40', '41-50','51-60','61-70','70+',"Unknown"]

# create a new column and use np.select to assign values to it using our lists as arguments
df_filter['BikeAgeGrp'] = np.select(conditions, values)

# display updated DataFrame
# df_filter.head()

filer_condition=df.loc[(df['BikeAge']=="Unknown")|(df['BikeAge']=="70+")].index
df_another_filter=df.loc[filer_condition,:]

print(df_another_filter.shape)
# create a list of our conditions
conditions = [
    (df_another_filter['BikeAge']=="Unknown") ,
    (df_another_filter['BikeAge']=="70+")]

# create a list of the values we want to assign for each condition
values = ["Unknown","70+"]

# create a new column and use np.select to assign values to it using our lists as arguments
df_another_filter['BikeAgeGrp'] = np.select(conditions, values)

# display updated DataFrame
# df_another_filter.tail()

# concatenating the two dataframes to get a single dataframe
df=pd.concat([df_another_filter,df_filter],axis=0)

# sns.countplot("BikeAgeGrp", data=df)
# plt.xlabel('Age Groups')
# plt.ylabel('Number of accidents')
# plt.show()

# print(df["TraffCntrl"].value_counts())
# x=df["TraffCntrl"].value_counts().sort_values(ascending=False)
# plt.figure(figsize=(30,15))
# plt.xticks(rotation=45, fontsize=15,horizontalalignment='right')
# sns.barplot(x.index,x.values)
# plt.xlabel('Traffic Control System')
# plt.ylabel('Number of accidents')
# plt.show()

# !pip install plotly_express

import plotly_express as px
# fig=px.scatter_mapbox(df, lat="Y", lon="X", zoom=10,mapbox_style="carto-positron",
#                       hover_name="County",color="AmbulanceR",animation_frame="CrashYear")
# fig.show()

# df["BikeAlcDrg"].value_counts()

# df["BikeAlcFlg"].value_counts()

#''' highlighting the values where the accidents are high by grouping of Bike Race and Bike sex based on user defiend cutoff value'''

# m=df.groupby(["BikeRace","BikeSex"]).size()
# m=m.unstack()
# def color_extreme_cutoff_value(val,cutoff):
#     color = 'red' if val > cutoff else 'black'
#     return 'color: %s' % color
# m.style.applymap(color_extreme_cutoff_value,cutoff=1000)

#  """Highlight the entire row in Yellow where Column Female or Male value is greater than 1000"""

# m=df.groupby(["BikeRace","BikeSex"]).size()
# m=m.unstack()
# def highlight_greaterthan_cutoff(m,cutoff):
#     if m["Female"] > cutoff or m["Male"] > cutoff:
#         return ['background-color: yellow']*len(m) #len(m) is the length of columns , Total 3 columns
#     else:
#         return ['background-color: white']*len(m)


#     m.style.apply(highlight_greaterthan_cutoff, axis=1,cutoff=1000)

"""**Building a Dashboard on Streamlit**"""

#!pip install streamlit # install the library

import streamlit as st

st.title("Bicyclist and pedestrian crashes that occurred in North Carolina between years 2007 through 2019")
st.markdown("""
The purpose of this dashboard is to allow users to view the locations of crashes involving 
bicyclists and pedestrians in North Carolina. 
The data comes from police-reported bicycle-motor vehicle and pedestrian-motor vehicle collisions 
that occurred on the public roadway network, public vehicular areas and private properties (if reported)
 from January 2007 through December 2019.

The dashboard can be used to understand the underlying causes of
 crashes and if used and understood effectively can be used to prevent the further crashes
""")

# st.markdown("## " + 'Total Accidents caused by Various Reasons')	
# st.markdown("#### " +"What Reasons would you like to see?")

selected_metrics = st.sidebar.selectbox(
    label="What Reasons would you like to see?", 
    options=['Accidents by Year and Location',
             'Accidents GroupedBy Biker Race and Gender',
             'Accidents by Bikers Age Group',
             "Accidents by month"]
)

st.write('You selected:', selected_metrics)

import plotly.graph_objects as go

if selected_metrics == 'Accidents by Year and Location':
    fig=px.scatter_mapbox(df, lat="Y", lon="X", zoom=10,mapbox_style="carto-positron",
                      hover_name="County",color="AmbulanceR",animation_frame="CrashYear")
    fig.update_layout(title_text='Accidents by Year and Location')
    fig.show()
if selected_metrics == 'Accidents GroupedBy Biker Race and Gender':
 
    fig=px.histogram(df, x='BikeRace', color="BikeSex", barmode='group')
    fig.update_layout(title_text='Accidents GroupedBy Biker Race and Gender')
    fig.show()
if selected_metrics == 'Accidents by Bikers Age Group':
   fig=px.histogram(df, x='BikeAgeGrp' )
   fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
   fig.update_layout(title_text='Accidents by Bikers Age Group')
   fig.show() 
if selected_metrics == 'Accidents by month':
   fig=px.histogram(df, x='CrashMonth' ,animation_frame="CrashYear")
   fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
   fig.update_layout(title_text='Accidents by month')
   fig.show()      
st.plotly_chart(fig, use_container_width=True)

st.sidebar.title("Year Wise Data ")













