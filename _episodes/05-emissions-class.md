---
title: An Emissions Class
teaching: 30
exercises: 30
questions:
    - " How can I use NetCDF in Pandas?"
    - " How should I structure my DataFrame?"
objectives:
---

At the end of the last lesson we our program was able to load the NetCDF file and create a 
`DataFrame` containing the emissions and total emissions data. An example of what this
program might look like is available [here](../code/load_data_03.py). 

Let's look 

The first function we will create will be called `load_data` and will take a single argument that is the filename of
the dataset we are loading. It will look like this:

```python
def load_data(filename):
   '''Load a NetCDF4 file containing the CMIP5 dataset.
   
      Parameters:
      	filename: path to the dataset
      	
    	  Return value:
    	    A pandas dataframe containing the fossil fuel emission and total emissions for each month
    	    on a lat/lon grid.
    	 '''
    	 
    	 ...
```

The second function
      