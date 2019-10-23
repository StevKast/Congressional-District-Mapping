#Code is from frankrowe github
#Frank Rowe: https://gist.github.com/frankrowe
#shp2gj.py: https://gist.github.com/frankrowe/6071443


import pyshp as shapefile
# read the shapefile
reader = shapefile.Reader("TigerData/tl_2017_39_tract.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
   atr = dict(zip(field_names, sr.record))
   geom = sr.shape.__geo_interface__
   buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 

# write the GeoJSON file
from json import dumps
geojson = open("TigerData/tl_2017_39_tract.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2) + "\n")
geojson.close()