'''
Created on 21 jul. 2019

@author: ingov
'''
#We use pandas to create and manage dataframes and dataseries with our data
import pandas as pd
#We use matplotlib.pyplot to build and plot graphs
import matplotlib.pyplot as plt
#We use os to get our current folder so we can manage files
import os
#We use DonutChartGenerator to generate a donut graph
from API import DonutChartGenerator as dcg

def get_votes_by_party(data):
    """
    @param data: Dataframe with our data
    @return: A series, where we transform our 2D data frame to a 1D series
    The format of that series is: [YesParty1, YesParty2, YesParty3,...,YesPartyN, NoParty1,...,
    NoPartyN,...] so the outer region of our chart matches with the inner region. This way the
    section with Yes votes for every party in the outer region of the chart, makes with the
    section of Yes in the inner region and so on
    """
    totals = []
    #For each column, in this case for each possible option in the voting
    for j in range(1,data.shape[1]):
        #We get the votes for every political party
        for i in range(0,data.shape[0]):
            #We add it to our array
            totals.append(data.loc[i][data.columns[j]])
    #We turn our array into a series
    ds = pd.Series(totals)
    return ds

def get_annotations_marriage_equality(data):
    """
    @param data: Dataframe with the data for our chart
    @return: The annotations in the correct format for the outer region of the chart 
    """
    legend = []
    #We just match key and value and give it the format: <Party> <Vote> and it to the array
    #legend that we will return
    for j in range(1,data.shape[1]):
        for i in range(0,data.shape[0]):
            item = "{0} {1}".format(data['Party'][i],data.columns[j])
            legend.append(item)
    return legend

def inner_donut_totals(df):
    """
    @param df: Dataframe with the information
    @return: A dataseries that contains the total of votes for every column/option.
    In other words, the number of votes for Yes, No,... that we will use for the inner region
    of our chart
    """
    return df.drop(['Party'],axis=1).sum()

def marriage_equality_graph_generator(country,func_outer=get_votes_by_party,func_inner=inner_donut_totals,get_outer_annotations=get_annotations_marriage_equality,double=True,titleText="Marriage Equality",legendDict = {'green':'Yes','red':'No','yellow':'Abstained','grey':'Absent'}):    
    """
    @param country: Country where marriage equality was legalized and we are going to generate
    a donut chart for the vote on marriage equality
    @param func_outer: Function we are going to use to get the data to generate the outer region
    of our doble donut chart. By default, get_votes_by_party defined previously
    @param func_inner: Function we are going to use to get the data to generate the inner region
    of our doble donut chart. By default, inner_donut_total defined previously
    @param get_outer_annotations: Function we will use to get the data for the annotations for the outer
    region of our donut chart. By default, get_annotations_marriage_equality defined previously
    @param double: If True, we will build a double donut chart. If false a simple one.
    By default True
    @param titleText: Text for the graph, by default Marriage Equality
    @param legendDict: Dictionary that contains the colors used for the inner region of this chart.
    By default: green for Yes, red for No, yellow for Abstained and grey for Absent
    @return A png file with our graph
    This is a wrapper for the function graph generator in modile DonutChartGenerator in folder API
    Basically just prepares the data and particular aspects of our problem which is building donut chart
    that represent the votings for marriage equality in different countries    
    """
    try:
        #We read the xlsx file that contais the information for the voting in that country
        #and build a dataframe with it (all files have the same format)
        df = pd.read_excel(os.getcwd()+"\..\data\{0}.xlsx".format(country))
        #We add the country to the title of the graph
        titleText = titleText + " " + country
        #We use our graph generator to buld the graph
        fig,ax = dcg.graph_generator(df, func_outer, func_inner, get_outer_annotations,double, titleText, legendDict)
        #We save our graph as a png file that will be used later in the markers in the map
        plt.savefig(os.getcwd()+"\..\pngFiles\{0}.png".format(country))
        #We close our figure (which is important as we can't keep creating and displaying
        #figures eternally)
        plt.close(fig)
    except FileNotFoundError:
        #If we don't find the file for it, it means we have no information about that country
        #and we just go on
        pass
    
def gettingHTML(series):
    """
    @param series: Dataseries that contains that information in the voting for same sex marriage
    for a particular country
    @returns: A string with HTML code that will display the graph we saved previously in
    a png code in the pop-up for the marker
    """
    doublePie = False
    noinfo = False
    if series['Voting'] == "Parliament":
        doublePie = True
    elif series['Voting'] == "-":
        noinfo = True
        
    if not noinfo:    
        marriage_equality_graph_generator(series['Country'], get_votes_by_party,inner_donut_totals,get_annotations_marriage_equality, doublePie, series['Date'], legendDict = {'green':'Yes','red':'No','yellow':'Abstained','grey':'Absent'})
        path = os.getcwd()+"\..\pngFiles\{0}.png".format(series['Country'])
        path = path.replace("\\","/")
        strHTML = "<img src='"+path+"' alt='"+series['Date']+"'>"
    else:
        strHTML = strHTML = "<b>{0}</b>\n".format(series['Year'])
    return strHTML