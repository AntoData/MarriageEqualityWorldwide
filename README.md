# MarriageEqualityWorldwide
In this project we generate two different html files that contain two maps:
- marriage_equality_approval_rate_worldwide.html: It's a map that represents the different rates of approval for marriage equality per country using different colors according to the approval rate. If marriage equality is already legal in that country, we display a marker. When the marker is opened, it displays the year in which marriage equality was legalized in that country
- marriage_equality_legal_worldwide.html: It's a map where we color the countries where marriage equality is legal in green and display a marker. When we open the marker, it will display a donut graph that represents how the voting to legalize marriage equality went in that country. If we have data available we will use a double donut, we the outer region will display the percentage of votes each political party gave for every option and in the inner one just totals for the different options (Yes, No, Abstained and Absent). If we only have totals, we will generate a simple donut chart and we won't. If we have no data we will display the year in which marriage equality was legalized. These graphs had been previously saved as png files in folder pngFiles

The project is organized in several folders
 
Folder API, contains two interesting modules:
- DonutChartGenerator whose function graph_generator allows you to generate simple or double donut charts very easily and very customized  - MapGenerator whose function build_map allows you to build a map coloring regions according to certain values defined by yourself and including a legend and putGenericMarkers that allows you to set markers in the map and the HTML code you want to be displayed when we open a marker

Folder Wrapper, contains Wrappers for the previously mentioned modules:
- MarriageEqualityChartGeneratorWrapper: Contains functions that will be used in the function marriage_equality_graph_generator that will call the function graph_generator customizing its parameters and its results so it fits our problem. In this case, generate a graph that
represents the voting in which marriage equality was legalized for each country.

Folder Instantiators, contains the modules we have to run to generate the maps that use the modules in API and also the modules in API:
- MarriageEqualityApprovalRate: When you run it, it will generate the file marriage_equality_approval_rate_worldwide.html
- MarriageEqualityLegalized: When you run it, it will generate the file marriage_equality_legal_worldwide.html

Folder Data:
Here we will include all the csvs, xlxs and so on files that we need to get the information for our maps and graphs

Folder pngFiles:
Here we will store the png files that where we save the different donut graphs we generate so we can display them when open a marker
