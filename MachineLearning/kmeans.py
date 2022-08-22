from Precode import *
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show, output_notebook

data = np.load('AllSamples.npy')
k1,i_point1,k2,i_point2 = initial_S1('0000') # please replace 0111 with your last four digit of your ID


centroids = i_point1
centroid_1 ={}
condition=1
cost = []
def find_clusters(k, centroids):
    #initialize array for clusters (k)
    clusters = {}
    for i in range(k):
        clusters[i] = []
    for subset in data:
        euc_dist = []
        for j in range(k):
            euc_dist.append(np.linalg.norm(subset - centroids[j]))
        clusters[euc_dist.index(min(euc_dist))].append(subset)

    return clusters
def find_centroid(k, clusters):
    centro = {}
    for i in range(k1):
        centro[i] = []
    for i in range(k):
        centro[i] = np.average(clusters[i], axis=0)
        
    return centro
    
def graph_plot(centroids):
    # Create a blank figure with labels
    p = figure(plot_width = 600, plot_height = 600, 
               title = 'Clustering',
               x_axis_label = 'X', y_axis_label = 'Y')

    # Add squares glyph
    for i in range(len(data)):
        p.square(data[i][0],data[i][1], size = 12, color = 'red')

    for i in range(len(i_point1)):
        p.square(i_point1[i][0],i_point1[i][1], size = 12, color = 'navy')

    #p.circle(circles_x, circles_y, size = 12, color = 'red')

    # Set to output the plot in the notebook
    output_notebook()
    # Show the plot
    show(p)
def check_condition(centroids, k):
    for i in range(k):
        
        if(centroids[i]== centroid_1[i]):
            condition = 0
def find_cost(k,cluster,centroids):
    val = 0
    for i in range(k):
        for sub in cluster[i]:
            val += np.linalg.norm(sub - centroids[i])**2
    cost.append([centroids, val])
    

    
#print(condition)

centroids = i_point1
#for j in range(100):

#replace k1 to k2 for question 3 &4
for i in range(50):
    centroid_1 = centroids
    cluster = find_clusters(k1, centroids)
    cent = find_centroid(k1, cluster)
    centroids = cent
    find_cost(k1,cluster,centroids)
    #check_condition(centroids,k1)   
print(centroids)
print(cost[-1])