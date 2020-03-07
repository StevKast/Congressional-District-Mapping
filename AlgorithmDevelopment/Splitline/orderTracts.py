import pandas as pd
import math
from operator import itemgetter

tract_data = pd.read_csv("../Lloyd/tract_data.csv")

populations = tract_data[' POP'].tolist()
geoID = tract_data['GEOID'].tolist()
tractName = tract_data[' FULL_NAME'].tolist()
lats = tract_data[' LAT'].tolist()
lons = tract_data[' LON'].tolist()

data = []
topRight = []
for g, p, t, la, lo in zip(geoID, populations, tractName, lats, lons):
    if len(topRight) == 0 or (la > topRight[3] and lo > topRight[4]):
        topRight = [g, p, t, la, lo]


print(topRight)
distances = []
for g, p, t, la, lo in zip(geoID, populations, tractName, lats, lons):
    d = math.sqrt((la - topRight[3])**2) + ((lo - topRight[4])**2)
    distances.append(d)

for g, p, t, la, lo, d in zip(geoID, populations, tractName, lats, lons, distances):
    data.append([g, p, t, la, lo, d])

data = sorted(data, key=lambda x: x[5])

print(data)

df = pd.DataFrame(data, columns=['GEOID', 'POP', 'FULL_NAME', 'LAT', 'LON', 'DISTANCE_TO_TOP_RIGHT'])
df.to_csv("ordered_tracts.csv")