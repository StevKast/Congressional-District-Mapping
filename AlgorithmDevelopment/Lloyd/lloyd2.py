import csv, os, json, numpy, random
from pprint import pprint

#Globals
filename = "tract_data.csv"
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

#Print out pop of each districts and total pop
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
                if loc.getCoords()[0] == float(d[3]) and loc.getCoords()[1] == float(d[4]):
                    currentKey = distListKeys[key]
                    distList[currentKey].append(d)
                    data.pop(data.index(d))
                    break

def reachCap(tractList):
    pop = 0
    if not tractList:
        return false
    else:
        for tract in tractList:
            pop += tract.getPop()
    return pop > 800000

#LLoyd's
#----------------------------\/
#input x - current data point
#input
def bestKey(input, mu, clusters):
    x = input.getCoords()
    min = min([(i[0], numpy.linalg.norm(x-mu[i[0]])) for i in enumerate(mu)])[0]
    bestkey = min([(i[0], numpy.linalg.norm(x-mu[i[0]])) for i in enumerate(tempmu)], key=lambda t:t[1])[0]
    print(min)
    return bestkey


#input: data - list of all points
#input: mu - list of current centers
#output: dictionnary of clusters
def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = bestKey(x, mu, clusters)
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]


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
        newmu.append(numpy.mean(clusterCoords, axis = 0))
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
#output: dictionarry of all clusters
#oldmu is a list of the old find_centers
#mu is a list of the current centers
def find_centers(X, K):
    # Initialize to K random centers
    oldmuTracts = random.sample(X, K)
    muTracts = random.sample(X, K)
    mu = []
    oldmu = []

    for i in range(K):
        mu.append(muTracts[i].getCoords())
        oldmu.append(oldmuTracts[i].getCoords())

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
    output = list()
    for d in data:
        temp = tract(int(d[0]), int(d[1]), float(d[3]), float(d[4]))
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
    # with open('result.json', 'w') as p:
    #     json.dump(distList, p)
