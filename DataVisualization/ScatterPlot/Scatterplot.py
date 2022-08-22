
# coding: utf-8

# # Assignment 3: Dino Fun World Analysis
# 
# ### Assignment Description
# 
# The administrators of Dino Fun World, a local amusement park, have asked you, one of their data analysts, to perform three data analysis tasks for their park. These tasks will involve understanding, analyzing, and graphing attendance data for three days of the park's operations that the park has provided for you to use. They have provided the data in the form of a database.
# 
# Part 1: The park's administrators would like your help understanding the different paths visitors take through the park and different rides they visit. In this mission, they have selected five (5) visitors at random whose check-in sequences they would like you to analyze. For now, they would like you to construct a distance matrix for these five visitors. The five visitors have the IDs: 165316, 1835254, 296394, 404385, and 448990.
# 
# Part 2: The park's administrators would like to understand the attendance dynamics at each ride (note that not all attractions are rides). They would like to see the minimum (non-zero) attendance at each ride, the average attendance over the whole day, and the maximum attendance for each ride in a parallel coordinate plot.
# 
# Part 3: In addition to a parallel coordinate plot, the administrators would like to see a scatterplot matrix depicting the minimum, average, and maximum attendance for each ride as above.
# 
# ### Directions
# 
# The database provided by the park administration is formatted to be readable by any SQL database library. The course staff recommends the sqlite3 library. The database contains three tables, named 'checkin', 'attractions', and 'sequences'. The database file is named 'dinofunworld.db' and is available in the read only directory of the Jupyter Notebook environment (i.e., readonly/dinofunworld.db). It can also be accessed by selecting File > Open > dinofunworld.db.
# 
# The information contained in each of these tables is listed below:
# 
# `checkin`:
#     - The check-in data for all visitors for the day in the park. The data includes two types of check-ins: inferred and actual checkins.
#     - Fields: visitorID, timestamp, attraction, duration, type
# `attraction`:
#     - The attractions in the park by their corresponding AttractionID, Name, Region, Category, and type. Regions are from the VAST Challenge map such as Coaster Alley, Tundra Land, etc. Categories include Thrill rides, Kiddie Rides, etc. Type is broken into Outdoor Coaster, Other Ride, Carussel, etc.
#     - Fields: AttractionID, Name, Region, Category, type
# `sequences`:
#     - The check-in sequences of visitors. These sequences list the position of each visitor to the park every five minutes. If the visitor has not entered the part yet, the sequence has a value of 0 for that time interval. If the visitor is in the park, the sequence lists the attraction they have most recently checked in to until they check in to a new one or leave the park.
#     - Fields: visitorID, sequence
#     
# Using the data provided, perform the required analyses and create the distance matrix, parallel coordinate plot, and scatterplot matrix.
# 
# 
# ### Submission Directions for Assignment Deliverables
# 
# This assignment will be auto-graded. We recommend that you use Jupyter Notebook in your browser to complete and submit this assignment. In order for your answers to be correctly registered in the system, you must place the code for your answers in the cell indicated for each question. In addition, you should submit the assignment with the output of the code in the cell's display area. The display area should contain only your answer to the question with no extraneous information or else the answer may not be picked up correctly.
# 
# Each cell that is going to be graded has a set of comment lines at the beginning of the cell. These lines are extremely important and must not be modified or removed. (Graded Cell and PartID comments must be in the same line for proper execution of code.)
# 
# Please execute each cell in Jupyter Notebook before submitting.
# 
# If you choose to download the file and work on your assignment locally, you can also upload your file to each part in the programming assignment submission space. The file you submit should be named "Assignment_3.ipynb".
# 
# ### Evaluation
# 
# There are three parts in the grading, and each part has one test case where the total number of points for all parts is 3. If some part of your data is incorrect, you will get a partial score of 0.50. If the submission fails, we will return the corresponding error messages. If the submission is correct, you will see "Correct" with 1.0 point for each part.

# In[63]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
con = sqlite3.connect('readonly/dinofunworld.db')
cur = con.cursor()


# In[64]:


# Graded Cell, PartID: IiXwN
# Create a distance matrix suitable for use in hierarchical clustering of the
# checkin sequences of the 5 specified visitors. Your distance function should
# count the number of dissimilarities in the sequences without considering any
# other factors. The distance matrix should be reported as a dictionary of
# dictionaries (eg. {1: {2:0, 3:0, 4:0}, 2: {1:0, 3:0, ...}, ...}).


cur.execute("SELECT visitorID, sequence FROM sequences where visitorID IN (165316, 1835254, 296394, 404385, 448990);")
sequences = cur.fetchall()
chkinSeq = pd.DataFrame.from_records(sequences, columns=['visitor', 'sequence'])
chkinSeq['sequence_list'] = chkinSeq['sequence'].apply(lambda s: s.split("-"))
distanceMatrix = {}
for i in range(5):
    for j in range(i+1, 5):
        distance = sum(int(x) != int(y) for x, y in zip(chkinSeq['sequence_list'][i], chkinSeq['sequence_list'][j]))
        p = chkinSeq['visitor'][i]
        q = chkinSeq['visitor'][j]
        index_i = distanceMatrix.get(p, {})
        index_i[q] = distance
        distanceMatrix[p] = index_i
        index_j = distanceMatrix.get(q, {})
        index_j[p] = distance
        distanceMatrix[q] = index_j
print(distanceMatrix)


# In[94]:


# Graded Cell, PartID: 8S2jm
# Create and display a Parallel Coordinate Plot displaying the minimum, average, 
# and maximum attendance for each ride in the park (note that not all attractions
# are rides).


cur.execute("SELECT AttractionID, Name FROM attraction where LOWER(Category) LIKE '%ride%';")
attractionList = cur.fetchall()
#print(attractionList)
attractions = pd.DataFrame.from_records(attractionList, columns=['AttractionID', 'AttractionName'])
#print(attractions)

cur.execute("SELECT visitorID, sequence FROM sequences;")
sequenceOfVisitor = cur.fetchall()
sequenceDetails = pd.DataFrame.from_records(sequenceOfVisitor, columns=['visitorID', 'sequence'])
#print(sequenceDetails)

sequenceDetails['index'] = sequenceDetails['sequence'].apply(lambda s: s.split("-"))
#print(sequenceDetails['index'])
#print(len(attractionList))
addNewCol = "sequenceAttendance"
allRideMinAvgMax = {}

for i in range(len(attractionList)):
    sequenceDetails[addNewCol] = sequenceDetails['index'].apply(lambda s: [1 if int(x) == int(attractionList[i][0]) else 0 for x in s])
    rideAttendance = np.sum(sequenceDetails[addNewCol].values.tolist(), axis=0)
    rideAttendance = rideAttendance[np.nonzero(rideAttendance)]
    minAttendance = np.min(rideAttendance)
    avgAttendance = np.mean(rideAttendance)
    maxAttendance = np.max(rideAttendance)
    rideDetails = {"min": minAttendance, "avg": avgAttendance, "max": maxAttendance}
    allRideMinAvgMax[attractionList[i][1]] = rideDetails
#print("allRideMinAvgMax....",allRideMinAvgMax)

allRideDetails = pd.DataFrame.from_dict(allRideMinAvgMax, orient='index')
allRideDetails = allRideDetails.reset_index()
allRideDetails.columns = ['ride' if x=='index' else x for x in allRideDetails.columns]

pd.plotting.parallel_coordinates(allRideDetails, 'ride')

plt.legend(bbox_to_anchor=(1.04,1), borderaxespad=0, labelspacing=1, ncol=3, prop={'size': 8.5})
plt.title('Ride Attedance Parallel Coordinate Plot', color='black')
plt.show()

print(allRideDetails)


# In[105]:


# Graded Cell, PartID: KHoww
# Create and display a Scatterplot Matrix displaying the minimum, average, and 
# maximum attendance for each ride in the park.
# Note: This is a different view into the same data as the previous part. While
# you work on these plots, consider the different things that each chart says
# about the data.

pd.plotting.scatter_matrix(allRideDetails, color='#095D26', hist_kwds={'color':'#095D26'})
plt.suptitle("Scatterplot Matrix for Ride Attendance")
plt.show()
#print(allRideDetails)

