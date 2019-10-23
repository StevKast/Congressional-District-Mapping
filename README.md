# Congressional-District-Mapping

To run the Romer Initial Data Exploration notebook in the Data Analysis 
folder, you will need to install an external python library via pip in 
your anaconda environment via the conda prompt. The link for the repo 
with documentation is included in the notebook.

To run the python notebooks, there are a few python libraries that you need. 
They are as follows:
1. census
2. us
3. dbfread

Use your local package manager to install these libraries.

All of the datafiles you need are in the repository however the .shp file is
to large to upload to github so you will need to go get it yourself for your 
local machine. Below, are the instructions to get it:
1. Go to census.gov/cgi-bin/geo/shapefiles/index.php
2. Select 2017 for Select Year
3. Select Census Tracts for Select a layer type
4. Click Submit
5. Select Ohio for Select a State
6. Inside the zip file you just downloaded, it will be tlp_2017_39_tract.shp

**REVISION**
THe .shp file is now available in the TigerData Folder
