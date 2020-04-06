# Congressional-District-Mapping

## Data Analysis

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
The .shp file is now available in the TigerData Folder

There is a seperate github repository for the web application portion of the project.
Github link: https://www.github.com/StevKast/Congressional-District-Mapping-SPA
Website link: https://www.congressional-districting.herokuapp.com/index.html

## Algorithm Development

### Modified Lloyd's Algorithm
Folder: Lloyd.

There have been several iterations of this algorithm in attempts to make compact, 
contiguous congressional districts.

Author's: Tim Romer, Gauthier Knox Kelly

Iterations:
1. lloyd.py: A test script that worked to read in all tracts and add them to congressional districts.
2. lloyd2.py: Script that iteratively recentered districts to add the nearest tract to eventually reach a convergence.
3. lloyd_tim.py: Iteration that added a population constraint that attempted to limit the population allowed in each district. 
This lead to a large amount of contiguity issues among districts.
4. lloyd_tim2.py: Iteration that focused on balancing the amount of tracts to each district. Another attempt to balance the 
populations. This had mixed results because the population dispartiy among tracts, that were supposed to have even 
populations, was greater than expected.
5. lloyd_tim3.py: Iteration that only added tracts to districts, in an iterative manner, that had the lowest population. This 
proved to succeed in the goal of creating evenly populated districts but this still produced contiguity issues.
6. lloyd_fixed.py: This will likely feature fixed starting points across the state and prevent the optimization of centers 
in order to allow the districts to grow organically and not overlap like in the past.
7. lloyd_fixed_split.py: This iteration built on the previous with fixing the district centers but in order to help the contiguity issue, once the tracts added has reached a certain percentage, the tracts will only add to the closest district.

Issues:
- The main issue is that the districts that are being generated are not continous.
...There seems to be a correlation between the balance of populations and degree of a district being contiguous. The more balanced the populations are, the less contiguous a district is.

### Shortest Splitline Algorithm
Folder: Splitline.

Author: Brian Fotheringham
