PyPi Module

Anleitung wie man pypi module erstellt:
https://packaging.python.org/tutorials/packaging-projects/

# Use as CLI-Tool
   
## Install
   
`pip install extractTool`

In addition, the following commands must be executed (if necessary with sudo):   
`apt-get install python-gdal`     
`apt-get install gdal-bin`   

`pip install pytest`

## Usage

`python detailebenen.py --path="<filepath>"`

behind it can still be added specifications:

Options:   
`--bbox` &larr; for the bounding box of the file (is also set as default)      
`--feature` &larr; to get all the coordinates of the file      
`--single` &larr; to get only the coordinates of a file (also default)      
`--whole` &larr; in combination with --bbox or --feature to read the respective one from an entire directory   
`--time` &larr; to get the time of a file      
