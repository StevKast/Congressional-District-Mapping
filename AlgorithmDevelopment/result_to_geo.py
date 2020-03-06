# Author: 	Tim Romer
# Date: 	2-24-2020
# Description: 	Converts the results of the algorithm into the geojson file for the
#		front-end use. This file will loop through all of the districts and
#		add the district to the geojson by district id.

import json

dist = [] # Stores the result of the algorithm
tiger = [] # Stores the geojson data
results_geoid = {} # Stores the cleaned result of algorithm if needed
files = ['Lloyd/result.json', 'SplitlineDictionary.json'] # Files to merge json

# Loop through the files
for file in files:
	# Open the file to be read
	with open(file, 'r') as f:
		dist = json.load(f)

	# Open the geojson file
	with open('../DataAnalysis/TigerData/tl_2017_39_tract.json', 'r') as f:
		tiger = json.load(f)
	
	# Gets the geoid for each tract in each district adds it to a dictionary.
	if file == 'Lloyd/result.json':
		for district in dist:
			for i in range(len(dist[district])):
				results_geoid[dist[district][i][0]] = district


	# Add the district information to the json
	for tract in range(len(tiger['features'])):
		geoid = tiger["features"][tract]['properties']['GEOID']
		if file == 'Lloyd/result.json':
			tiger["features"][tract]['properties']['district'] = results_geoid[geoid]
		else:
			tiger["features"][tract]['properties']['district'] = 'd' + str(dist[geoid])

	# Write the married json to a file to json file
	if file == 'Lloyd/result.json':
		with open('result_Lloyd.json', 'w') as wr:
			json.dump(tiger, wr)
	else:
		with open('result_' + file, 'w') as wr:
			json.dump(tiger, wr)
