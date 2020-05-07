# File : Lloyd's Algorithm (lloyd_fixed_split.py) 7th iteration
# Author : Tim Romer
# Date : 3-31-2020

import csv, os, json, numpy, random, math
import pandas as pd
from pprint import pprint

# Globals
filename = "ordered_tracts.csv" # File name on where to get initial district centers
data = [] # Storing tract and district data
# List of district names to write to the outputted json file
distListKeys = ['d1','d2','d3','d4',
                'd5','d6','d7','d8',
                'd9','d10','d11','d12',
                'd13','d14','d15','d16']
# List to store the tracts in certain districts
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

# -------------------------- Tract Class --------------------------------------

class tract:
    """
    A class used to represent a census tract

    ...
    Attributes
    ----------
    id : str
        a unique string that represents each tract
    pop : int
        the population of the census tract
    x : float
        the longitude of the geographic center of the tract
    y : float
        the latitude of the geographic center of the tract

    Methods
    -------
    getCoords()
        returns the latitude and longitude in a numpy array
    getPop()
        returns the population for the tract
    getId()
        returns the unique id for the tract
    """

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

# ----------------------- Helper Functions ------------------------------------

def transferData(results, data):
    """
    This function will transfer the results of the algorithm into a new form 
    to write to the json output.

    Parameters
    ----------
    results : Dictionary 
        results of the algorithm
    data : List
        object to write results of the algorithm to

    Returns
    -------
        Nothing as data is a global object
    """

    for key in results.keys(): #key -> int
        for loc in results[key]: #loc -> numpy array
            for d in data: #d -> list
                if loc.getCoords()[0] == float(d[4]) and loc.getCoords()[1] == float(d[5]):
                    currentKey = distListKeys[key]
                    distList[currentKey].append(d)
                    data.pop(data.index(d))
                    break

def totalPop(key):
    """
    Find current total pop of specified district
    
    Parameters
    ----------
    key : str
        a district name to get the population of

    Returns
    -------
    int
        the total population for a specified district
    """

    data = distList[key]
    totalPop = 0
    if len(data) == 0:
        return totalPop
    else:
        for row in data:
            if int(row[2]) is not None:
                totalPop = totalPop + int(row[2])
    return totalPop


def printPop():
    """
    Print out pop of each districts and total pop
    """

    ohioPop = 0
    for key in distList.keys():
        ohioPop += totalPop(key)
        print(key +" - "+ str(totalPop(key)))

    print('ohio pop = ', ohioPop)

def print_cluster_pops(clusters):
"""
This is a helper method to help print the cluster populations

Parameters
----------
Clusters : list
    a list of district centers
"""
total_tracts = 0
for c in clusters:
    cluster_pop = 0
    for index in clusters[c]:
        cluster_pop += index.pop
    total_tracts += len(clusters[c])
    print(c, cluster_pop, len(clusters[c]))
print(total_tracts)

def read_initial_centers(X):
"""
This will read the initial centers from a csv with chosen centers

Parameters
----------
X : List
    List of tracts

Returns
-------
list
    initial districts

"""
initial = pd.read_csv('optimized_initial_centers.csv')
ret = []
for index, row in initial.iterrows():
    for x in X:
        if row['geoid'] == x.getId():
            ret.append(x)
return ret

# ----------------------Algorithm----------------------------------------

def bestKey(input, mu, clusters):
    """
    Will find the closest availbale tract for a district

    Parameters
    ----------
    input : tract
        tract object to examine
    mu : list
        a list of the optimal geographic centers for districts
    clusters : dictionary
        dictionary of districts and the list of tracts that are in each district
    """

    x = input.getCoords()
    bestkey = min([(i[0], numpy.linalg.norm(x-mu[i[0]])) for i in enumerate(mu)], key=lambda t:t[1])[0]
    return bestkey

def getDist(tract_coords, center_coords):
    """
    Calculate the distance from the tract to the center

    Parameters
    ----------
    tract_coords : array
        the geographic center of a tract
    center_coords : array
        the geographic center of a district

    Returns
    -------
    float
        The distance between the tract centers and district centers
    """

	return math.sqrt(((tract_coords[0] - center_coords[0])**2) + ((tract_coords[1] - center_coords[1])**2))

def find_closest_tract(X, center):
    """
    Will find the closest tract to the center provided
    
    Parameters
    ----------
    X : list
        List of tracts to loop through
    center : center
        array of centers coordinates for the district 

    Returns
    -------
    tract
        closest tract to the center
    """

    # Some arbitrary value that is larger than any possible distance
	min_dist  = 100000000000000
	min_tract = X[0]

	# Loop through all of the tracts to get find the closest tract to the 
    # center
	for x in X:
		distance = getDist(x.getCoords(), center)
		if distance < min_dist:
			min_dist = distance
			min_tract = x
	return min_tract

def find_min_pop_cluster(clusters):
    """
    Will loop through the districts, calculate each population, then return the
    center with the minimum population.

    Parameters
    ----------
    clusters : list
        A list of districts 

    Returns
    -------
    int
        The index of the minimum district
    """

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


def cluster_points(X, mu):
    """
    This function will assign all of the tracts to a district round robin style
    until all tracts are assigned

    Parameters
    ----------
    X : list
        List of tracts
    mu : list
        List of district centers

    Returns
    -------
    dictionary
        dictionary of districts and the tracts inside each district
    """

    center_count = 0
    clusters = {} # The object being returned
    taken_tracts = [] # Tracking the tracts that have been added
    initial_tract_length = len(X)

    while len(X) != 0:
        if len(clusters) == 16:
            if len(taken_tracts) / initial_tract_length <= 0.80:
                min_cluster = find_min_pop_cluster(clusters) # Will return the index of the minimum cluster
                closest = find_closest_tract(X, mu[min_cluster]) # Will find the closest tract to that center
                taken_tracts.append(closest)
                X.remove(closest)
                clusters[min_cluster].append(closest)
                print(len(taken_tracts))
            else:
                print(X[0])
                bestmukey = bestKey(X[0], mu, clusters)
                clusters[bestmukey].append(X[0])
                taken_tracts.append(X[0])
                X.remove(X[0])
                print(len(taken_tracts))
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

def reevaluate_centers(mu, clusters):
    """
    Creates new centers based on the districts that have been created. Apart
    of the iterative process.

    Parameters
    ----------
    mu : list
        list of current centers
    cluster : dictionary
        list of current clusters

    Returns
    -------
    list
        A list of new/optimized centers
    """
    newmu = []
    keys = sorted(clusters.keys())

    for k in keys:
        clusterCoords = []
        for i in clusters[k]:
            clusterCoords.append(i.getCoords())
        # TIM: Does this find a new center of the district??
        newmu.append(numpy.mean(clusterCoords, axis = 0))
    return newmu


#input: mu - current centers
#input: oldmu - old centers
#output: true if tuples are same, false otherwise
def has_converged(mu, oldmu):
    """
    Tuple is a collection with UNCHANGEABLE order
    This checks if the current mu's are the same

    Parameters
    ----------
    mu : list
        List of the new optimized centers
    oldmu : list
        List of the previous centers

    Returns
    -------
    bool
        wether convergence has been reached. All oldmu is equal to mu
    """

    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])




def find_centers(X, K):
    """
    Call this function for Lloyds
    X is a list of all points, K is the number of clusters you want
    output: dictionarry of all clusters
    oldmu is a list of the old find_centers
    mu is a list of the current centers

    Driver function for lloyds. Will check convergence for district centers
    and will add all tracts to the districts. Right now, this method will
    only run once because the initial district centers were chosen and will
    not change.
    """

    # Initialize to K random centers
    oldmuTracts = random.sample(X, K)
    muTracts = read_initial_centers(X)
    mu = []
    oldmu = []
    count = 0
    clusters = {}
    ogX = X.copy()

    # get the coordinates for each tract sample and append to mu/oldmu
    for i in range(K):
        mu.append(muTracts[i].getCoords())
        oldmu.append(oldmuTracts[i].getCoords())

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
        # if count % 5 == 0:
        print('Iteration of Convergence: ', count)
        break
    print('Converged on iteration: ', count)
    return(clusters)


def init_data(data):
    """
    creates list of data points based on the census tracts
    x and y values are the coordinates
    """
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
    # print_cluster_pops(results)
    transferData(results, data)

    #print pop for testing
    #print to json
    printPop()
    with open('result.json', 'w') as p:
        json.dump(distList, p)