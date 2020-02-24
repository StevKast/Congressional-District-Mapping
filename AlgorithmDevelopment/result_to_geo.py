# Author: 	Tim Romer
# Date: 	2-24-2020
# Description: 	Converts the results of the algorithm into the geojson file for the
#		front-end use. This file will loop through all of the districts and
#		add the district to the geojson by district id.

import json

dist = []
tiger = []
results_geoid = {}

with open('Lloyd/result.json', 'r') as f:
	dist = json.load(f)

with open('../DataAnalysis/TigerData/tl_2017_39_tract.json', 'r') as f:
	tiger = json.load(f)
	
# Gets the geoid for each tract in each district adds it to a dictionary.
for district in dist:
	for i in range(len(dist[district])):
		results_geoid[dist[district][i][0]] = district

# Add the district information to the json
for tract in range(len(tiger['features'])):
	geoid = tiger["features"][tract]['properties']['GEOID']
	tiger["features"][tract]['properties']['district'] = results_geoid[geoid]

with open('Lloyd_Result.json', 'w') as wr:
	json.dump(tiger, wr)