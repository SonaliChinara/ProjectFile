from Precode2 import *
import numpy
from math import sqrt
data = np.load('AllSamples.npy')

k1,i_point1,k2,i_point2 = initial_S2('0000') # please replace 0111 with your last four digit of your ID

print(k1)
print(i_point1)
print(k2)
print(i_point2)

def edclidean_distance (point1 ,point2):
    edclidean = sqrt (((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))
    return edclidean

def findClosestCentorid(centroids,point):
        distance= []
        for centroid in centroids:
            distance.append (edclidean_distance(centroid,point))
        closet_centroids=np.argmin(distance)
        return closet_centroids
    
def findNewCentriods(clusters,centroids):
    newCentroids= []
    for i in range(len(clusters)) :
        if len(clusters[i]) != 0 :
            newCentroids.append(np.mean(clusters[i],axis=0))
        else: newCentroids.append(centroids[i])
    return np.array(newCentroids)

def calculateCost(centroids, cluster):
    sum = 0
    for i, val in enumerate(centroids):        
        sum+= np.sum(np.power(cluster[i]-val,2))      
    return sum

def calculateKmean(centroids,k,data):
    not_converg =True
    while not_converg :
        clusters=[]
        for i in range(len(centroids)):
            clusters.append([])
        for point in data:
            cluster_index=findClosestCentorid(centroids,point)
            clusters[cluster_index].append(point)
        newCentroids = findNewCentriods(clusters,centroids)
        if np.count_nonzero(centroids-newCentroids) == 0 :
            not_converg = False
        centroids= newCentroids
    for i in range(len(clusters)):
        clusters[i] = np.array(clusters[i])
    return newCentroids,clusters


def getAllIntialPoints(samples,first_intial,k):
    centroids=[first_intial]
    for i in range(k-1):
        distance=[]
        n = len(samples)
        for i in range(n):
            distance.append([])
        for j in range(n):            
            for centroid in centroids:
                distance[j].append(edclidean_distance(centroid,samples[j]))
        distance = np.array(distance)
        mean_distance=distance.mean(axis=1)
        far_point=np.argmax(mean_distance)
        centroids.append(samples[far_point])
    return (np.array(centroids))




intial_centroids_k4 = getAllIntialPoints(data,i_point1,k1)
centroids,clusters = calculateKmean(intial_centroids_k4,k1,data)
cost = calculateCost(centroids,clusters)
print ("::::Centroids for 4 cluster::::")
print(centroids)
print("cost::::::::",cost)


intial_centroids_k6 = getAllIntialPoints(data,i_point2,k2)
centroids,clusters = calculateKmean(intial_centroids_k6,k2,data)
cost = calculateCost(centroids,clusters)
print ("::::Centroids for 6 cluster::::")
print(centroids)
print("cost::::::::",cost)