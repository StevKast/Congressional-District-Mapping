import pandas as pd
import json
import math

dictionary = {}
districtNumber = 1

data = pd.read_csv('tract_data.csv', delimiter=',')
data = data.values.tolist()
populations = [item[1] for item in data]

sumPop = 0
i = 0
for p in populations:
    sumPop += p

# Iterate through a list of tracts and split into two lists of even population.
# Based on population goal given
def getSplit(cdata, goal):
    endpop = 0
    current = 0
    pops = [item[1] for item in cdata]
    for p in pops:
        if current < goal:
            current += p
            endpop += 1
    return endpop

# order list of tracts based on distance from top rightmost tract
def topRight(cdata, popGoal):
    topRightC = []
    tr_data = []
    for x in cdata:
        if len(topRightC) == 0 or (x[3] > topRightC[3] and x[4] > topRightC[4]):
            topRightC = x

    for x in cdata:
        d = math.sqrt((x[3] - topRightC[3]) ** 2) + ((x[4] - topRightC[4]) ** 2)
        if len(x) == 5:
            x.append(d)
        else:
            x.pop(5)
            x.append(d)
        tr_data.append(x)

    tr_data = sorted(tr_data, key=lambda x: x[5])
    print(tr_data)
    split = getSplit(tr_data, popGoal)
    tr_data = tr_data[0:split]
    topLeftC = []
    bottomRightC = []
    for x in cdata:
        if len(topLeftC) == 0 or (x[3] > topLeftC[3] and x[4] < topLeftC[4]):
            topLeftC = x
        elif len(bottomRightC) == 0 or (x[3] < bottomRightC[3] and x[4] > bottomRightC[4]):
            bottomRightC = x

    distance = math.sqrt((topLeftC[3] - bottomRightC[3]) ** 2 + (topLeftC[4] - bottomRightC[4]) ** 2)
    return distance, tr_data

# order list of tracts based on distance from top leftmost tract
def topLeft(cdata, popGoal):
    topLeftC = []
    tl_data = []
    for x in cdata:
        if len(topLeftC) == 0 or (x[3] > topLeftC[3] and x[4] < topLeftC[4]):
            topLeftC = x

    for x in cdata:
        d = math.sqrt((x[3] - topLeftC[3]) ** 2) + ((x[4] - topLeftC[4]) ** 2)
        if len(x) == 5:
            x.append(d)
        else:
            x.pop(5)
            x.append(d)
        tl_data.append(x)

    tl_data = sorted(tl_data, key=lambda x: x[5])
    print(tl_data)
    split = getSplit(tl_data, popGoal)
    tl_data = tl_data[0:split]
    topRightC = []
    bottomLeftC = []
    for x in cdata:
        if len(topRightC) == 0 or (x[3] > topRightC[3] and x[4] > topRightC[4]):
            topRightC = x
        elif len(bottomLeftC) == 0 or (x[3] < bottomLeftC[3] and x[4] < bottomLeftC[4]):
            bottomLeftC = x

    distance = math.sqrt((topLeftC[3] - bottomLeftC[3]) ** 2 + (topLeftC[4] - bottomLeftC[4]) ** 2)
    return distance, tl_data

# order list of tracts based on distance from bottom leftmost tract
def bottomLeft(cdata, popGoal):
    bottomLeftC = []
    bl_data = []
    for x in cdata:
        if len(bottomLeftC) == 0 or (x[3] < bottomLeftC[3] and x[4] < bottomLeftC[4]):
            bottomLeftC = x

    for x in cdata:
        d = math.sqrt((x[3] - bottomLeftC[3]) ** 2) + ((x[4] - bottomLeftC[4]) ** 2)
        if len(x) == 5:
            x.append(d)
        else:
            x.pop(5)
            x.append(d)
        bl_data.append(x)

    bl_data = sorted(bl_data, key=lambda x: x[5])
    print(bl_data)
    split = getSplit(bl_data, popGoal)
    bl_data = bl_data[0:split]
    topLeftC = []
    bottomRightC = []
    for x in cdata:
        if len(topLeftC) == 0 or (x[3] > topLeftC[3] and x[4] < topLeftC[4]):
            topLeftC = x
        elif len(bottomRightC) == 0 or (x[3] < bottomRightC[3] and x[4] > bottomRightC[4]):
            bottomRightC = x

    distance = math.sqrt((topLeftC[3] - bottomRightC[3]) ** 2 + (topLeftC[4] - bottomRightC[4]) ** 2)
    return distance, bl_data

# order list of tracts based on distance from bottom rightmost tract
def bottomRight(cdata, popGoal):
    bottomRightC = []
    br_data = []
    for x in cdata:
        if len(bottomRightC) == 0 or (x[3] < bottomRightC[3] and x[4] > bottomRightC[4]):
            bottomRightC = x

    for x in cdata:
        d = math.sqrt((x[3] - bottomRightC[3]) ** 2) + ((x[4] - bottomRightC[4]) ** 2)
        if len(x) == 5:
            x.append(d)
        else:
            x.pop(5)
            x.append(d)
        br_data.append(x)

    br_data = sorted(br_data, key=lambda x: x[5])
    print(br_data)
    split = getSplit(br_data, popGoal)
    br_data = br_data[0:split]
    topRightC = []
    bottomLeftC = []
    for x in cdata:
        if len(topRightC) == 0 or (x[3] > topRightC[3] and x[4] > topRightC[4]):
            topRightC = x
        elif len(bottomLeftC) == 0 or (x[3] < bottomLeftC[3] and x[4] < bottomLeftC[4]):
            bottomLeftC = x

    distance = math.sqrt((topRightC[3] - bottomLeftC[3]) ** 2 + (topRightC[4] - bottomLeftC[4]) ** 2)
    return distance, br_data

# Compare Splitline distance from all splits possible, choose shortest splitline
def shortest(cdata, currentPopGoal):
    choices = []
    choices.append(topRight(cdata, currentPopGoal))
    choices.append(topLeft(cdata, currentPopGoal))
    choices.append(bottomLeft(cdata, currentPopGoal))
    choices.append(bottomRight(cdata, currentPopGoal))

    shortestSplit = []
    for c in choices:
        if len(shortestSplit) == 0 or c[0] < shortestSplit[0]:
            shortestSplit = c
    return shortestSplit[1]


def splitLine(cdata, currentPopGoal, overallPop):
    global districtNumber

    if currentPopGoal == overallPop / 16:
        geo = [item[0] for item in cdata]
        for g in geo:
            dictionary[g] = districtNumber
        districtNumber += 1
        return

    currentPopGoal = currentPopGoal / 2

    split = shortest(cdata, currentPopGoal)
    SplitA = split
    SplitB = []
    for x in cdata:
        if x not in SplitA:
            SplitB.append(x)
    splitLine(SplitA, currentPopGoal, overallPop)
    splitLine(SplitB, currentPopGoal, overallPop)
    return


splitLine(data, sumPop, sumPop)
print(dictionary)
dict_j = json.dumps(dictionary)
f = open("SplitlineDictionary.json", "w+")
f.write(dict_j)
f.close()
