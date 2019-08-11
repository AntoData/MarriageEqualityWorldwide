'''
Created on 21 jul. 2019

@author: ingov
'''
"""
Data source: Wikipedia
"""
from API import MapGenerator as mg
import pandas as pd
import os
import folium
"""
We are going to generate a world map where we will paint each country
in different colours that represent a certain approval rate where that data is available.
If there is not data on marriage equality approval available, we will just paint it black
If marriage equality is legal in that country, we will also display a marker. If we select
the marker the year in which marriage equality was legalized will be displayed 
"""
#In this case, we set the following colours
colours = {0:"red",25:"orange",50:"yellow",75:"green",100:"#003300"}
#Color code for the map:
#Countries where the approval rate is as low as between 0 and 25 per cent should be painted red 
#as it is a very low approval rate, orange for approval rates as low as between 25 and 50, 
#yellow between 50 and 75, green for values between 75 and 100 as this is a good indicator for 
#lgtbi tolerance and dark green for 100
#we use getcmd to get the absolute route of our json file
geo_world = os.getcwd()+"\..\data\world-countries.json"
#We get our excel file to a dataframe object
df_mear = pd.read_excel(os.getcwd()+"\..\data\MarriageEqualityApprovalRate.xlsx")
#We create a folium map object
mear_world = folium.Map(titles='Mapbox Bright',start_zoom = 3)
#We turn our dataframe to a dictionary with the information we are interested in:
#country and same sex marriage approval rate expressed in a scale from 0 to 100
dict_mear = df_mear.set_index('Country')['For-100'].to_dict()
#We define the path were our html file will be saved
pathHTML = os.getcwd()+"\..\marriage_equality_approval_rate_worldwide.html"
#we define the caption for our legend in the map
vCap = "Same-Sex Approval Rate"
#we use the function we defined previously to generate the map
vMap = mg.buildMap(mear_world, geo_world,dict_mear, colours, vCap,'name')
#we read the csv with the data of countries where same-sex marriage is legal to a dataframe
df_mel = pd.read_csv(os.getcwd()+"\..\data\MarriageEqualityLegalized.csv",sep="\t")
#We use the function putMarkers to put markers in the capital cities of countries where
#same-sex marriage is legal
vMap = mg.putMarkers(vMap, df_mel, 'Lat', 'Lon', 'Year', 'blue')
#We save the map to a map
mear_world.save(pathHTML)