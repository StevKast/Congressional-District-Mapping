import pandas as pd
import json

dictionary = {}
districtNumber = 1
tract_data = pd.read_csv("tract_data.csv")
populations = tract_data[' POP'].tolist()
geoID = tract_data['GEOID'].tolist()

sumPop = 0
for population in populations:
    sumPop += int(population)


def splitLine(tracts, geo, currentPopGoal, overallPop):
    global districtNumber

    if currentPopGoal == overallPop/16:
        print(geo)
        for g in geo:
            dictionary[g] = districtNumber
        districtNumber += 1
        return

    currentPopGoal = currentPopGoal / 2
    sum_p = 0
    tract_number = 0

    for population_x in tracts:
        sum_p += population_x
        if sum_p > currentPopGoal:
            SplitA_Pop = tracts[:tract_number]
            SplitA_ID = geo[:tract_number]
            SplitB_Pop = tracts[tract_number-1:]
            SplitB_ID = geo[tract_number-1:]
            splitLine(SplitA_Pop, SplitA_ID, currentPopGoal, overallPop)
            splitLine(SplitB_Pop, SplitB_ID, currentPopGoal, overallPop)
            return
        tract_number += 1

splitLine(populations, geoID, sumPop, sumPop)

print(dictionary)

dict_j = json.dumps(dictionary)

f = open("SplitlineDictionary_iteration1.json", "w+")
f.write(dict_j)
f.close()