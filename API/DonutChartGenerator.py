'''
Created on 17 jul. 2019

@author: ingov
'''
#matplotlib.pyplot for plotting graphs
import matplotlib.pyplot as plt
#matplotlib.patches will be used for the annotations of our graph
import matplotlib.patches as mpatches
#This will be used to manage data when displaying annotations
import numpy as np
#Random is a library to generate random numbers
import random
#We will use matplotlib to call colors.to_hex to turn str values into int hexadecmial values
import matplotlib

size = 0.3

def get_random_colours(df):
    """
    @param df: A dataframe with the data
    @return: An array of random colors we can use to color the outer region of a double donut chart
    """
    #We get the number of rows
    rows = df.shape[0]
    hex_colours = []
    outer_colors = []
    #We initialize an array called hex_colours with a random color per row 
    for _ in range(0,rows):
        hex_colours.append(random.randint(0, 0xFFFFFF))
    #We now get how many columns/fields each row has
    times = int(df.shape[1]/rows)
    #We iterate through hex_colours the following way
    #For each column
    for time in range(0,times):
        #We go through every row and add the corresponding similar color:
        #We get the previous color for that row and make it lighter
        for i in range(0+(rows*time),rows*(time+1)):
            hex_colours.append((hex_colours[i] & 0xffffff) >> 1)
    #Now we turn all these int values into string values with the format for hexadecimal colors
    for i in range(0,len(hex_colours)):
        outer_colors.append("#{:06x}".format(hex_colours[i]))
    #The way colors are returned in this array are:
    #color for: [colorrow0column0,colorrow1column0,...,colorrowncolumn0,lighter(colorrow0column0),lighter(colorrow1column0),...]
    return outer_colors

def from_str_to_hex(strHex):
    """
    @param strHex: String that contains a hexadecimal number that represents a color
    @return: Hexadecimal int value of that color
    """
    return int(matplotlib.colors.to_hex(strHex)[1:],16) 

def get_outer_colours(df,inner_colours):
    """
    @param df: A dataframe with the data
    @param inner_colours: An array with the colors used to pain the inner region of a donut chart
    @return: An array of colors 
    
    """
    initial_colours = []
    #We translate the  inner colors from str to int hexadecimal values so we can operate with them
    for colour in inner_colours:
        initial_colours.append(from_str_to_hex(colour))
    hex_colours = []
    outer_colors = []   
    #For each column
    for i in range(0,df.shape[1]-1):
        #For each row
        for j in range(0,df.shape[0]):
            if(j==0):
                #In the row is 0, we are in the initial row so we just add the initial colors
                hex_colours.append(initial_colours[i])
            else:
                #We add to this array a lighter color (+0x000015) than the previous
                #color for that column
                hex_colours.append(hex_colours[((i*df.shape[0])+j)-1]+0x000015)
    #We now turn back those int colors to hexadecimal str
    for i in range(0,len(hex_colours)):
        outer_colors.append("#{:06x}".format(hex_colours[i]))
    #We return the array ready to be used for the outer colors of a double donut chart
    #with the following structure:
    #[initialColor0,Lighter(initialColor0), lighter(lighter(initialColor)0,...., initialColor1,
    #lighter(initialColor1),lighter(lighter(initialColor1),....]
    return outer_colors

def percentage(pct):
    """
    @param pct: Float number to round
    @return: String that contains the float number pct rounded to two decimals
    
    """
    n = pct.round(2)
    if(n > 0):
        return "{0}".format(pct.round(2))
    else:
        return ""


def make_legend(legendDict):
    """
    @param legendDict: Dictionary that contains the colors and values we are going to use
    to paint our map
    @return: A list of the colors we are using in this donut chart with the label for their value 
    to be used as legend
    """
    legendList = []
    for key in legendDict.keys():
        legendList.append(mpatches.Patch(color=key, label=legendDict[key]))
    return legendList

def graph_generator(df,func_outer,func_inner,get_outer_annotations,double,titleText,legendDict):
    """
    @param df: data frame we will use to build the double donut chart
    @param func_outer: Function we will use to get the data from our data frame for the outer 
    region of the double donut chart, if None, we will build a regular donut chart
    @param func_inner: Function we will use to get the data from our data frame for the inner 
    region of the double donut chart, if None, we will build a regular donut chart
    @param get_outer:annotations: Function we will use to display the annotations for the outer
    region of our double donut chart
    @param double: If True, we will generate a double donut chart, if False we will generate 
    a simple donut chart
    @param TitleText: Title that will be displayed in our chart
    @param legentDict: Dictionary with the values and colors used in the donut chart in
    the inner region   
    @return: An pair of objects figure and axis where our donut chart is displayed    
    """
    #We initialize a pair of object fig and ax, using plt.subplots
    fig, ax = plt.subplots()
    #We define the size of our figure (basically of our graph) in inches
    fig.set_size_inches(9.5, 5.5)
    #If double is True, we build the outer region
    if(double):
        #We get the dataseries to use for the outer region using the function func_outer over
        #our dataframe
        ds = func_outer(df)
        #We use the function get_outer_colours defined previously to get the colours for the
        #outer region, in this case, variations of the colors used in the inner region
        # that are saved in the keys of the dictionary legendDict
        outer_colors = get_outer_colours(df,legendDict.keys())
        #We build the outer region of our donut chart
        wedges,texts = ax.pie(ds, radius=1, colors=outer_colors,
                              wedgeprops=dict(width=size, edgecolor='w'))
        #We set the parameters for the annotations
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        legd = get_outer_annotations(df)
        #We display the annotations
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            if(ds.loc[i]>5):
                ax.annotate(legd[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                            horizontalalignment=horizontalalignment, **kw)
        #We build the inner donut chart
        ax.pie(func_inner(df), autopct=lambda pct: percentage(pct), radius=1-size, colors=legendDict.keys(),
           wedgeprops=dict(width=0.2, edgecolor='w'))
    else:
        #If not double, we builder only the inner donut chart, with a larger size
        ax.pie(func_inner(df), autopct=lambda pct: percentage(pct), radius=1-size, colors=legendDict.keys(),
           wedgeprops=dict(width=size, edgecolor='w'))
    #We set the title for our graph
    ax.set(aspect="equal", title=titleText)
    #We build and display the legend for it
    legendList = make_legend(legendDict)
    plt.legend(handles=legendList, loc="best")
    #We return the figure and the axis with our simple or double donut chart  
    return fig,ax