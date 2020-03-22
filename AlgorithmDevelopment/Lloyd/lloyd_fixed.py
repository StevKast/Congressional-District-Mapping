# File : Lloyd's Algorithm (lloyd_tim2.py) 4th iteration
# Author : Tim Romer
# Date : 3-10-2020

import csv, os, json, numpy, random, math
from pprint import pprint

#Globals
filename = "ordered_tracts.csv"
data = []
distListKeys = ['d1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','d12','d13','d14','d15','d16']
distList = {'d1':[],
            'd2':[],
            'd3':[],
            'd4':[],
            'd5':[],
            'd6':[],
            'd7':[],
            'd8':[],
            'd9':[],
            'd9':[],
            'd10':[],
            'd11':[],
            'd12':[],
            'd13':[],
            'd14':[],
            'd15':[],
            'd16':[]}

# Target population size and allowable deviation from that mean
TARGET_DISTRICT_MEAN = 710767
TARGET_DISTRICT_SD   = TARGET_DISTRICT_MEAN + (TARGET_DISTRICT_MEAN * 0.005)

#class
class tract:
    def __init__(self, id, pop, x, y):
        self.id = id
        self.pop = pop
        self.coords = numpy.array([x, y])

    def getCoords(self):
        return self.coords

    def getPop(self):
        return self.pop

    def getId(self):
        return self.id

    def __str__(self):
        return "id: {} - pop: {} - coords: {}".format(self.id, self.pop, self.coords)
    def __repr__(self):
        return "{}, {}, {}".format(self.id, self.pop, self.coords)

def transferData(results, data):
    for key in results.keys(): #key -> int
        for loc in results[key]: #loc -> numpy array
            for d in data: #d -> list
                if loc.getCoords()[0] == float(d[4]) and loc.getCoords()[1] == float(d[5]):
                    currentKey = distListKeys[key]
                    distList[currentKey].append(d)
                    data.pop(data.index(d))
                    break

#Find current total pop of specified district
def totalPop(key):
    data = distList[key]
    totalPop = 0
    if len(data) == 0:
        return totalPop
    else:
        for row in data:
            if int(row[2]) is not None:
                totalPop = totalPop + int(row[2])
    return totalPop


#Print out pop of each districts and total pop
def printPop():
    ohioPop = 0
    for key in distList.keys():
        ohioPop += totalPop(key)
        print(key +" - "+ str(totalPop(key)))

    print('ohio pop = ', ohioPop)

# ----------------------Algorithm----------------------------------------

# Calculate the distance from the tract to the center
def getDist(tract_coords, center_coords):
	return math.sqrt(((tract_coords[0] - center_coords[0])**2) + ((tract_coords[1] - center_coords[1])**2))

# Will find the closest tract to the center provided
def find_closest_tract(X, center):
	min_dist  = 100000000000000 # Some arbitrary value that is larger than any possible distance
	min_tract = X[0]
	# Loop through all of the tracts to get find the closest tract to the center
	for x in X:
		distance = getDist(x.getCoords(), center)
		if distance < min_dist:
			min_dist = distance
			min_tract = x
	return min_tract


def find_min_pop_cluster(clusters):
    min_cluster_index = -1
    min_pop = 100000000000000
    for c in clusters:
        cluster_pop = 0
        for tract in clusters[c]:
            cluster_pop += tract.getPop()
        if cluster_pop < min_pop:
            min_pop = cluster_pop
            min_cluster_index = c
    return min_cluster_index
# This function will assign all of the tracts to a district round robin style
# until all tracts are assigned
def cluster_points(X, mu):
    center_count = 0
    clusters = {} # The object being returned
    taken_tracts = [] # Tracking the tracts that have been added

    while len(X) != 0:
        if len(clusters) == 16:
            min_cluster = find_min_pop_cluster(clusters) # Will return the index of the minimum cluster
            closest = find_closest_tract(X, mu[min_cluster]) # Will find the closest tract to that center
            taken_tracts.append(closest)
            X.remove(closest)
            clusters[min_cluster].append(closest)
        else:
            for center in mu:
                if (len(X) == 0): 
                    break
                closest = find_closest_tract(X, center) # Will find the closest tract to that center
                taken_tracts.append(closest)
                X.remove(closest)
                clusters[center_count] = [closest]
                center_count += 1
    return clusters

#Creates new centers
#input: mu - list of current centers
#input: cluster - list of current clusters
#output: newmu list of new centers
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())

    for k in keys:
        clusterCoords = []
        for i in clusters[k]:
            clusterCoords.append(i.getCoords())
        # TIM: Does this find a new center of the district??
        newmu.append(numpy.mean(clusterCoords, axis = 0))
    return newmu

#Tuple is a collection with UNCHANGEABLE order
#This checks if the current mu's are the same
#input: mu - current centers
#input: oldmu - old centers
#output: true if tuples are same, false otherwise
def has_converged(mu, oldmu):
    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])

# This is a helper method to help print the cluster populations
def print_cluster_pops(clusters):
    total_tracts = 0
    for c in clusters:
        cluster_pop = 0
        for index in clusters[c]:
            cluster_pop += index.pop
        total_tracts += len(clusters[c])
        print(c, cluster_pop, len(clusters[c]))
    print(total_tracts)
    exit()    

#Call this function for Lloyds
#X is a list of all points, K is the number of clusters you want
#output: dictionarry of all clusters
#oldmu is a list of the old find_centers
#mu is a list of the current centers
def find_centers(X, K):
    # Initialize to K random centers
    oldmuTracts = random.sample(X, K)
    muTracts = random.sample(X, K)
    mu = []
    oldmu = []
    count = 0
    clusters = {}
    ogX = X.copy()

    # TIM: get the coordinates for each tract sample and append to mu/oldmu
    for i in range(K):
        mu.append(muTracts[i].getCoords())
        oldmu.append(oldmuTracts[i].getCoords())

    # TIM: Why are we checking for convergence?
    while not has_converged(mu, oldmu):
        count += 1
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        X = ogX.copy()
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
        # print_cluster_pops(clusters)
        if count >= 100:
            break
        # Sanity tracker for tracking algorithm
        if count % 5 == 0:
            print('Iteration of Convergence: ', count)
        # print_cluster_pops(clusters)
    print('Converged on iteration: ', count)
    return(clusters)

#creates list of data points based on the census tracts
#x and y values are the coordinates
def init_data(data):
    output = list()
    for d in data:
        temp = tract(int(d[1]), int(d[2]), float(d[4]), float(d[5]))
        output.append(temp)
    return output

#Main
with open(filename) as csv_file:
    #read csv file
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
    data.pop(0)

    #call lloyds
    X = list(init_data(data))
    results = find_centers(X, 16)
    transferData(results, data)

    #print pop for testing
    #print to json
    printPop()
    with open('result.json', 'w') as p:
        json.dump(distList, p)