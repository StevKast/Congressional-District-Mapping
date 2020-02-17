import csv, os, json
from pprint import pprint

#Globals
filename = "tract_data.csv"
#Districts will be a list of districts where number one is districts[0]
distlist = {'d1': list(),
            'd2': list(),
            'd3': list(),
            'd4': list(),
            'd5': list(),
            'd6': list(),
            'd7': list(),
            'd8': list(),
            'd9': list(),
            'd10': list(),
            'd11': list(),
            'd12': list(),
            'd13': list(),
            'd14': list(),
            'd15': list(),
            'd16': list()}

#Methods
#Find current total pop of specified district
def totalPop(key):
    data = distlist[key]
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
    for key in distlist.keys():
        if totalPop(key) < totalPop(lowestPopDist):
            lowestPopDist = key
    return lowestPopDist

#LLoyd's Algorithm
def lloyd(data):
    minPopDist = data[0]
    for row in data:
        lowest = lowestPop()
        distlist[lowest].append(row)

#Main
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
    data.pop(0)
    lloyd(data)
    with open('result.json', 'w') as p:
        json.dump(distlist, p)
