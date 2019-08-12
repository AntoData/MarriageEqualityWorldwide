'''
Created on 21 jul. 2019

@author: ingov
'''
#We use folium to genetate the maps
import folium
#We use LinearColormap to create scales for pair of colours-values
from branca.colormap import LinearColormap
#We use branca to create the legend for our map
import branca

def color_scale(color1, color2, value,minValue,maxValue):
    """
    @param color1: This parameter is a string that contains a hexadecimal color (format #XXXXXX)
    or a valid color (for instance red, orange, yellow, blue) that establishes the first color
    in that range of values, the color that will be associated with minValue
    @param color2: This parameter is a string that contains a hexadecimal color (format #XXXXXX)
    or a valid color (for instance red, orange, yellow, blue) that establishes the second color
    in that range of values the color that will be associated with maxValue
    @param value: This parameter is a number, the value we have to paint with a color between
    color1 and color2 and that has to be between minValue and maxValue
    @param minValue: This parameter is a number, the lowest value possible within this range
    we are defining
    @param maxValue: This parameter is a number, the highest value possible within this range
    we are defining
    @return: LinearColorMap object
    
    Basically this builds an object where we build a color scale between two colors
    In minValue we indicate the value that represents color1 and in maxValue we indicate
    the value that represents color2 and we build a segment where the color of each
    value has a color according to that scale of value
    When we use it as a function using the parameter "value" we return the corresponding
    color for that value. We will use this function to color our map
    """
    return LinearColormap([color1,color2], vmin = minValue, vmax = maxValue)(value) 

#This function gets the object feature that represents the property feature in the json,
#a dictionary with the data (we use a dataframe and turn it into a dictionary),
#and a map with the ranges and colours where the key is the value and the value
#is the color associated to that value 
def get_color(feature,dataMap,colours,mapProperty):
    """
    @param feature: Presents the property feature in the json of our map
    @param dataMap: A dictionary with the data (we use a dataframe and turn it into a dictionary)
    @param colours: Dictionary with the ranges and colours where the key is the value and the value
    is the color associated to that value. It is important to notice that we can mix string values
    that will be static values (no range for them) and ranges. We will have to put all string/static
    values first in the map and them the number values that will be paired to make ranges.
    Also important to notice, the keys are the values and the values are the color a string
    with the hexadecimal color (#XXXXXX) or a valid color name
    @param mapProperty: Property in feature we will use to identify the zones defined in the
    json
    @return: the colour for the region we are iterating over, if it was a string/static value we will
    just return the colour in the map colours. But if it is a float we will evaluate inside which
    range it is and use the previously defined funcion color_scale to get the right color
    """
    #We get the keys of the dict colours which are the range of values to consider to 
    #colour this map, we will use it to compare the values in the dictionary with the values
    #for each row in the dictionary dataMap
    coloursKey = list(colours.keys())
    #We get the value of the associated to the region of our json that is going to be painted
    #in our data frame (well, the dictionary that we got from our dataframe), in this case
    #the property we use in the json (mapProperty) to get the value has to be a child of
    #properties. Also, our key values have to coincide with the property in the json that is
    #represented by mapProperty
    print(feature['properties'][mapProperty])
    value = dataMap.get(feature['properties'][mapProperty])
    try:
        number = int(value)
        value = number
    except Exception:
        try:
            number = float(value)
            value = number
        except Exception:
            pass
    #If value is not None, it means it is in our dataMap so we have to color that area    
    if(value is not None):
        #If value is not int or float, it means is a static value
        if not isinstance(value,(int,float)):
            i=0
            #We iterate through the different values that are associated with colors
            while(i<len(coloursKey) and value is not None):
                #If our value is equal to the value associated with a certain color, we return
                #that color
                if coloursKey[i] == value:
                    return colours.get(coloursKey[i])
                i = i + 1
        else:
            #We iterate through the values that define the ranges of colours that we got from
            #our dictionary of colors (key:value, value:colour)
            i = 1
            while(i<len(coloursKey) and value is not None):
                #if our current value is in that range, we use the function color_scale
                #that we defined previously to get the corresponding shade of the colour
                #for that value
                if isinstance(coloursKey[i-1],(int,float)) and isinstance(coloursKey[i],(int,float)):
                    lowerValue = float(coloursKey[i-1])
                    upperValue = float(coloursKey[i])
                    numValue = float(value)
                    if lowerValue <= numValue <= upperValue:
                        return color_scale(colours.get(lowerValue),colours.get(upperValue),numValue,lowerValue,upperValue)
                i=i+1
                


def buildMap(vMap,jsondata,dataMap,colours,vCaption,vCaption2,mapProperty):
    """
    @param vMap: Folium map object we will use as the base to build the regions and paint them
    @param jsondata: Route to the json we will use to divide our map into regions and to paint them
    @param dataMap: A dictionary with the data (we use a dataframe and turn it into a dictionary)
    @param colours: Dictionary with the ranges and colours where the key is the value and the value
    is the color associated to that value. It is important to notice that we can mix string values
    that will be static values (no range for them) and ranges. We will have to put all string/static
    values first in the map and them the number values that will be paired to make ranges.
    Also important to notice, the keys are the values and the values are the color a string
    with the hexadecimal color (#XXXXXX) or a valid color name
    @param VCaption: Text we will put in the legend for the linear colours in the map
    @param VCaption2: Text we will put in the legend for the static colours in the map
    @param mapProperty: Property in feature we will use to identify the zones defined in the
    json
    @return: the map divided in regions, with the regions painted and coloured according to the
    values we indicated in the dictionary dataMap
    """
    #We color the map in vMap using the feature GeoJson
    #and add it to the map
    folium.GeoJson(
    data = jsondata,
    style_function = lambda feature: {
        'fillColor': get_color(feature,dataMap,colours,mapProperty),
        'fillOpacity': 0.7,
        'color' : None,
        'weight' : 1,
    }    
    ).add_to(vMap)
    #We create a legend for the colours which we have painted our map with
    coloursKeys = list(colours.keys())
    #coloursValues = list(colours.values())
    linearLegendKeys = []
    linearLegendValues = []
    nonlinearLegendKeys = []
    nonlinearLegendValues = []
    numValue = True
    for vcolour in coloursKeys:
        if isinstance(vcolour, (int,float)):
            linearLegendValues.append(colours[vcolour])
            linearLegendKeys.append(vcolour)
        else:
            nonlinearLegendKeys.append(vcolour)
            nonlinearLegendValues.append(colours[vcolour])
            numValue = False
            
    #We create a colormap object to be used as legend
    if(len(linearLegendKeys)>1 and len(linearLegendValues)>1):
        colormap = branca.colormap.LinearColormap(linearLegendValues)
        colormap = colormap.to_step(index=linearLegendKeys)
        colormap.caption = vCaption
        #We add the colormap to our map
        colormap.add_to(vMap)
    #We this value corresponds to an static value, we will add it to the legend for static values
    if(not numValue):
        htmlLegend = """
        <div style='position: fixed;bottom:50px;left:50px;border:2px solid grey;z-index:9999; font-size:14px'>
        &nbsp; """+vCaption2
        for key in nonlinearLegendKeys:
            htmlLegend += '<br> &nbsp; '+key+' &nbsp;' 
            htmlLegend += '<svg width="40" height="11">'
            color = colours[key].replace(' ',"")
            rgbcolor = list(int(color[i:i+2], 16) for i in (1, 3, 5))
            htmlLegend += '    <rect width="40" height="11" style="fill:rgb({0},{1},{2});stroke-width:3;stroke:rgb(0,0,0)" />'.format(rgbcolor[0],rgbcolor[1],rgbcolor[2])
            htmlLegend += '</svg>'
        htmlLegend += """
        </div>
        """
        vMap.get_root().html.add_child(folium.Element(htmlLegend))
        
        
    return vMap

def putMarkers(vMap,vData,colLat,colLon,colPopup,markerColour):
    """
    @param vMap: Folium map object we will use as the base to build the regions and paint them
    @param vData: A dataframe with the data
    @param colLat: Name of the column in the dataframe where the latitude for the point where
    we want to display the marker is saved
    @param colLong: Name of the column in the dataframe where the longitude for the point where
    we want to display the marker is saved
    @param colPopup: Name of the column in the dataframe where the message for the popup for that
    marker is saved
    @param markerColour: Colour for the marker
    @return: Our map vMap with the markers added
    """
    #we go through the dataframe
    for i in range(0,vData.shape[0]):
        #And create and add a marker for every row
        folium.Marker(location=[vData.loc[i][colLat],vData.loc[i][colLon]], popup = "<b>{0}</b>".format(vData.loc[i][colPopup]), 
                      icon= folium.Icon(color=markerColour,size=1)).add_to(vMap)
    return vMap

def putGenericMarkers(vMap,vData,func_HTML,colLat,colLon,markerColour):
    """
    @param vMap: Folium map object we will use as the base to build the regions and paint them
    @param vData: A dataframe with the data
    @param func_HTML: This is a function that will provide the HTML code for the popup for 
    that every marker
    @param colLat: Name of the column in the dataframe where the latitude for the point where
    we want to display the marker is saved
    @param colLong: Name of the column in the dataframe where the longitude for the point where
    we want to display the marker is saved
    @param markerColour: Colour for the marker
    @return: Our map vMap with the markers added
    """
    #we go through the dataframe
    for i in range(0,vData.shape[0]):
        #And create and add a marker for every row
        folium.Marker(location=[vData.loc[i][colLat],vData.loc[i][colLon]], popup = func_HTML(vData.loc[i]), 
                      icon= folium.Icon(color=markerColour,size=1)).add_to(vMap)
    return vMap