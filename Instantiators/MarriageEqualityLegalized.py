'''
Created on 21 jul. 2019

@author: ingov
'''
"""
Data source: Wikipedia
"""
#We get MapGenerator so we can use the function build_map and putGenericMarkers to build our map
from API import MapGenerator as mg
#We get MarriageEqualityChartGeneratorWrapper so we can get the function gettingHTML
#so we can pass it as a parameter for function putGenericMarkers
from Wrappers import MarriageEqualityChartGeneratorWrapper as mecg
#We import pandas so we can build a dataframe and manage the data of our initial file
import pandas as pd
#We import os to get our current path so we can get the initial file with the initial data
import os
#We import folium so we can build the base map that we will use to build our map with all the
#information about marriage equality
import folium
"""
We are generating a world map, where we will paint green the countries where marriage equality
is legal and marker that will display a simple or double donut chart with information
about how the voting on the legalization of marriage equality went (if data about it
is available)
"""

#In this case, we set the following colours
colours = {"Legal":"#006600","Illegal":"#ff0000"}
#We are talking our same sex marriage approval rate, countries where the approval rate is as low as
#between 0 and 25 should be painted red as it is a very low approval rate, orange for approval rates
#as low as between 25 and 50, yellow between 50 and 75, green for values between
#75 and 100 as this is a good indicator of lgtbi tolerance and dark green for 100 for
#coherence between colours
#we use getcmd to get the absolute route of our json file
geo_world = os.getcwd()+"\..\data\world-countries.json"
#We get our excel file to a dataframe object
df_mel = pd.read_csv(os.getcwd()+"\..\data\MarriageEqualityLegalized.csv",sep="\t")
#df_ssa = pd.read_excel(os.getcwd()+"\..\data\SSM.xlsx")
#We create a folium map object
mel_world = folium.Map(titles='Mapbox Bright',start_zoom = 3)
#We turn our dataframe to a dictionary with the information we are interested in
#country and same sex marriage approval rate expressed in a scale from 0 to 100
dict_mel = df_mel.set_index('Country')['Status'].to_dict()
#We define the path were our html file will be saved
pathHTML = os.getcwd()+"\..\\marriage_equality_legal_worldwide.html"
#we define the caption for our legend in the map
vCap = "Same-Sex Approval Rate"
vCap2 = "Status"
#we use the function we defined previously to generate the map
vMap = mg.buildMap(mel_world, geo_world,dict_mel, colours, vCap,vCap2,'name')
#we read the csv with the data of countries where same-sex marriage is legal to a dataframe
#df_ssm = pd.read_csv(os.getcwd()+"\..\data\SSM.csv",sep="\t")
#We use the function putMarkers to put markers in the capital cities of countries where
#same-sex marriage is legal
vMap = mg.putGenericMarkers(vMap, df_mel, mecg.gettingHTML,'Lat', 'Lon', 'blue')
#We save the map to a map
mel_world.save(pathHTML)