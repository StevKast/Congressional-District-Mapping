import csv, os, json, numpy, random
from pprint import pprint

#Globals
filename = "tract_data.csv"
data = list()
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

#Methods
#Find current total pop of specified district
def totalPop(key):
    data = distList[key]
    totalPop = 0
    if len(data) == 0:
        return totalPop
    else:
        for row in data:
            if int(row[1]) is not None:
                totalPop = totalPop + int(row[1])
    return totalPop


#Find the lowest pop distrcit
def lowestPop():
    lowestPopDist = 'd1'
    for key in distList.keys():
        if totalPop(key) < totalPop(lowestPopDist):
            lowestPopDist = key
    return lowestPopDist

#Print out pop of each districts
def printPop():
    ohioPop = 0
    for key in distList.keys():
        ohioPop += totalPop(key)
        print(key +" - "+ str(totalPop(key)))

    print('ohio pop = ', ohioPop)

#Transfers data from the given dict to the distList dic
def transferData(results, data):
    for key in results.keys(): #key -> int
        for loc in results[key]: #loc -> numpy array
            for d in data: #d -> list
                x = float(d[3])
                y = float(d[4])
                if loc[0] == x and loc[1] == y:
                    currentKey = distListKeys[key]
                    distList[currentKey].append(d)
                    data.pop(data.index(d))
                    break

#check if every district pop is withing a num
def similarPop(range):
    for dist1 in distList:
        for dist2 in distList:
            if totalPop(dist1) - totalPop(dist2) > abs(range):
                return False
    return True

def reachCap(keyInput):
    return totalPop(keyInput) > 800000

#LLoyd's
#----------------------------\/
#input x - current data point
#input
def bestKey(x, mu):
    bestkey = min([(i[0], numpy.linalg.norm(x-mu[i[0]])) \
            for i in enumerate(mu)], key=lambda t:t[1])[0]
    return bestkey


#input: data - list of all points
#input: mu - list of current centers
#output: dictionnary of clusters
def cluster_points(dataInput, mu):
    clusters  = {}
    for x in dataInput:
        bestmukey = bestKey(x, mu)
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
        # transferData(clusters, data)
        # if reachCap(bestmukey):
        #     mu.pop(index(bestmukey))
    return clusters

#Creates new centers
#input: mu - list of current centers
#input: cluster - list of current clusters
#output: newmu list of new centers
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(numpy.mean(clusters[k], axis = 0))
    return newmu

#Tuple is a collection with UNCHANGEABLE order
#This checks if the current mu's are the same
#input: mu - current centers
#input: oldmu - old centers
#output: true if tuples are same, false otherwise
def has_converged(mu, oldmu):
    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])

#Call this function for Lloyds
#X is a list of all points, K is the number of clusters you want
#returns a tuple
#tuple[0] is a list of all the cluster find_centers
#tuple[1] is a dictionnary contain k keys, and the values are a list of each points
#oldmu is a list of the old find_centers
#mu is a list of the current centers
def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(clusters)


#creates list of data points based on the census tracts
#x and y values are the coordinates
def init_data(data):
    X = numpy.array([(float(data[i][3]), float(data[i][4])) for i in range(len(data))])
    return X

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
