##import

import arcpy
import numpy as np 
import pandas as pd
import os


##allow overwriting
arcpy.env.overwriteOutput = True

##set workspace

arcpy.env.workspace = r"Z:\Geog428\Lab2\Assignment_2\Assignmentresults\Assignmentresults.gdb"


##########################
##Question 1###


##Make map layers parks and crime
arcpy.MakeFeatureLayer_management("" + "Parks_maintained_by_the_City_of_Victoria","Parks")
arcpy.MakeFeatureLayer_management("" + "Victoria_Crime","Crime")

##intersect parks and crime
arcpy.analysis.Intersect("Crime #;Parks #", "" + "Park_Crime", 'ALL', None, 'INPUT')


#count crimes

print("Question 1")
print(arcpy.management.GetCount('Park_Crime'))


###################################
######Question 2##############


##make map layer neighbourhood

arcpy.MakeFeatureLayer_management("" + "Neighbourhood_Boundaries","Nhoods")



##Select neighbourhoods
OK =  "Oaklands"
FW = "Fernwood"
NJ = "North Jubilee"
SJ = "South Jubilee"

whereExpr =  "Neighbourh LIKE '%s'" % OK + "or Neighbourh LIKE '%s'" % FW + "or Neighbourh LIKE '%s'" % SJ + "or Neighbourh LIKE '%s'" % NJ
print(whereExpr)

arcpy.management.SelectLayerByAttribute('Nhoods', 'NEW_SELECTION', whereExpr)


##Select parks in the neighbourhoods

arcpy.management.SelectLayerByLocation('Parks', 'WITHIN', 'Nhoods')

##Buffer selected parks
arcpy.analysis.Buffer('Parks',"" + "ParkBuffer",'500 Meters', 'FULL', 'ROUND', 'ALL')

####select 2016 crimes

crimeYear = 2016
PCrime = "Property Crime"
whereExpr = "incident_d LIKE '%%%s%%'" %crimeYear + "And parent_inc LIKE '%s'" %PCrime
print(whereExpr)


arcpy.management.SelectLayerByAttribute("Crime", 'NEW_SELECTION', whereExpr)

##intersect crime and parks

arcpy.analysis.Intersect("Crime #;ParkBuffer #", "" + "Crime_Q2", 'ALL', None, 'INPUT')


##get count
print("Question 2")
print(arcpy.management.GetCount('Crime_Q2'))

########################
###Question 3########

##add layer
      
arcpy.MakeFeatureLayer_management("" + "Schools", "School" )

##Select neighbourhood except vic west

VicWest = "Victoria West"

whereExpr = "Neighbourh LIKE '%s'" %VicWest
print(whereExpr)

arcpy.management.SelectLayerByAttribute('Nhoods', 'NEW_SELECTION',whereExpr, 'INVERT')

##intersect schools
arcpy.analysis.Intersect("School #;Nhoods #","" + "schools_subset", 'ALL',None, 'INPUT')

###buffer school subset

arcpy.analysis.Buffer('schools_subset',"" + "school_buffer",'500 Meters', 'FULL', 'ROUND', 'ALL')

##Select crime types

##add types

crime1 = "Disorder"
crime2 = "Liquor"
crime3 = "Drugs"


whereExpr = "parent_inc LIKE '%s'" % crime1 + "or parent_inc LIKE '%s'" % crime2 + "or parent_inc LIKE '%s'" % crime3
print(whereExpr) 

arcpy.management.SelectLayerByAttribute('Crime', 'NEW_SELECTION', whereExpr)

## add year

crimeYear = 2017

whereExpr = "incident_d LIKE '%%%s%%'" %crimeYear
print(whereExpr)

arcpy.management.SelectLayerByAttribute('Crime', 'SUBSET_SELECTION',whereExpr)

##intersect crime and school buffer

arcpy.analysis.Intersect("Crime #;school_buffer #", "" + "Q3school_crime", 'ALL', None, 'INPUT')

##get count
print("Question 3")
print(arcpy.management.GetCount('Q3school_crime'))

##############################
###Question 4


##make map layer neighbourhood

arcpy.MakeFeatureLayer_management("" + "Neighbourhood_Boundaries","Nhoods")
arcpy.MakeFeatureLayer_management("" + "Parks_maintained_by_the_City_of_Victoria","Parks")
arcpy.MakeFeatureLayer_management("" + "Victoria_Crime","Crime")


##Select neighbourhoods
OK =  "Oaklands"
FW = "Fernwood"
NJ = "North Jubilee"
SJ = "South Jubilee"

whereExpr =  "Neighbourh LIKE '%s'" % OK + "or Neighbourh LIKE '%s'" % FW + "or Neighbourh LIKE '%s'" % SJ + "or Neighbourh LIKE '%s'" % NJ
whereExpr

arcpy.management.SelectLayerByAttribute('Nhoods', 'NEW_SELECTION', whereExpr)


##Select parks in the neighbourhoods

arcpy.management.SelectLayerByLocation('Parks', 'WITHIN', 'Nhoods')

##Buffer selected parks 100m
arcpy.analysis.Buffer('Parks',"" +"ParkBuffer100",'100 Meters', 'FULL', 'ROUND', 'ALL')

####select 2017 propery crimes

crimeYear = 2017
PCrime = "Property Crime"
whereExpr = "incident_d LIKE '%%%s%%'" %crimeYear + "And parent_inc LIKE '%s'" %PCrime

arcpy.management.SelectLayerByAttribute("Crime", 'NEW_SELECTION', whereExpr)

##intersect crime and parks

arcpy.analysis.Intersect("Crime #;ParkBuffer100 #", "" + "Crime_Q4", 'ALL', None, 'INPUT')


##get count
print("Question 4")
print(arcpy.management.GetCount('Crime_Q4'))

######################################
##Question 5


##add layers
arcpy.MakeFeatureLayer_management("" + "Schools","School")
arcpy.MakeFeatureLayer_management("" + "Neighbourhood_Boundaries","Nhoods")
arcpy.MakeFeatureLayer_management("" + "Victoria_Crime","Crime")

##Select neighbourhood except vic west

VicWest = "Victoria West"

whereExpr = "Neighbourh LIKE '%s'" %VicWest

arcpy.management.SelectLayerByAttribute('Nhoods', 'NEW_SELECTION',whereExpr, 'INVERT')

##intersect schools
arcpy.analysis.Intersect("School #;Nhoods #", "" + "schools_subset", 'ALL',None, 'INPUT')

###buffer school subset

arcpy.analysis.Buffer('schools_subset',"" + "school_buffer100",'100 Meters', 'FULL', 'ROUND', 'ALL')

##Select crime types

##add types

crime1 = "Disorder"
crime2 = "Liquor"
crime3 = "Drugs"


whereExpr = "parent_inc LIKE '%s'" % crime1 + "or parent_inc LIKE '%s'" % crime2 + "or parent_inc LIKE '%s'" % crime3
whereExpr 

arcpy.management.SelectLayerByAttribute('Crime', 'NEW_SELECTION', whereExpr)

## add year

crimeYear = 2015

whereExpr = "incident_d LIKE '%%%s%%'" %crimeYear
print(whereExpr)

arcpy.management.SelectLayerByAttribute('Crime', 'SUBSET_SELECTION',whereExpr)

##intersect crime and school buffer

arcpy.analysis.Intersect("Crime #; school_buffer100 #", "" + "Q5school_crime", 'ALL', None, 'INPUT')

##get count
print("Question 5")
print(arcpy.management.GetCount('Q5school_crime'))


###############################
##Question 6

#set variables
crimeTypes = ['Assault', 'Robbery','Property Crime','Theft','Theft from Vehicle'] #make array with crime types
days = ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']


dayCounter = [None] *7 #makes day counter array with nothing in it times 7
#none lets you put anything into it vs 0 will only allow numbers

maxDays = [[None] *3] * len(crimeTypes)



#for each crime type
for i in (np.arange(len(crimeTypes))):
    crime = crimeTypes [i]
    print('\n\nStarting' +crime +"crimes...")
    for j in (np.arange(len(days))):
            day = days[j]
            print('\nCounting' + day + ' ' + crime + "Crimes,,,")
            
##test SQL
i=0
j=0

whereExpr = "parent_inc = '%s'" %crimeTypes[i] + "And day_of_wee = '%s'" %days[j]

print(whereExpr)

##test two loop
crimeTypes = ['Assault', 'Robbery']
days = ['Friday', 'Saturday']
dayCounter = [None] *2
maxDays = [[None] *3] * len(crimeTypes)


#select crimes
crime = crimeTypes[i]
day = days[j]

#count crimes

for i in (np.arange(len(crimeTypes))):
    crime = crimeTypes [i]
    print('\n\nStarting' +crime +"crimes...")
    for j in (np.arange(len(days))):
            day = days[j]
            print('\nCounting' + day + ' ' + crime + "Crimes,,,")
            whereExpr = "parent_inc = '%s'" %crimeTypes[i] + "And day_of_wee = '%s'" %days[j]
            arcpy.management.SelectLayerByAttribute('Crime', 'NEW_SELECTION',whereExpr)
            ##set count from arcpy.managment.getcount(crimes)
            count = arcpy.management.GetCount('Crime')
            dayCounter[j]= int(count[0])
    #maxdays line up with crime loop
    maxElement = np.amax(dayCounter)#max value
    maxDay = days[np.where(dayCounter == np.amax(dayCounter))[0][0]]
    maxDays[i] = [crime, maxDay, maxElement]	


print("finished check two loop")

#set full loop to run

#reset variables
crimeTypes = ['Assault', 'Robbery','Property Crime','Theft','Theft from Vehicle'] #make array with crime types
days = ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

#set counter arrays
dayCounter = [None] *7 
maxDays = [[None] *3] * len(crimeTypes)

##Run loop
for i in (np.arange(len(crimeTypes))):
    crime = crimeTypes[i]
    print('\n\nStarting' +crime +"crimes...")
    whereClause = "parent_inc = '%s'" %crimeTypes[i] 
    arcpy.management.MakeFeatureLayer('Crime', "" + os.path.splitext(crime.replace(" ",""))[0], whereClause,None)
    for j in (np.arange(len(days))):
            day = days[j]
            print('\nCounting' + day + ' ' + crime + "Crimes,,,")
            whereExpr = "parent_inc = '%s'" %crimeTypes[i] + "And day_of_wee = '%s'" %days[j]
            arcpy.management.SelectLayerByAttribute('Crime', 'NEW_SELECTION',whereExpr)    
            count = arcpy.management.GetCount('Crime')
            dayCounter[j]= int(count[0])
    maxElement = np.amax(dayCounter)
    maxDay = days[np.where(dayCounter == np.amax(dayCounter))[0][0]]
    maxDays[i] = [crime, maxDay, maxElement]

print("Question 6")
print(maxDays)

##create dataframe and save to csv   

df = pd.DataFrame.from_records(maxDays)
df.to_csv("" + "MaxDayResults1.csv")



