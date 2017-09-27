---
title: Analyzing the Data
teaching: 30
exercises: 30
questions:
    - " How can I use a class to make code reusable?"
objectives:
---

At the end of the last lesson our program provided a class for managing the emissions data. 
An example of what this program might look like is available [here](../code/historical_co2_emissions_05.py). 

The purpose of creating the `HistoricalCO2Emissions` class was so that we could re-use it for
our analysis task. So let's see how to do that now. We're going to create a new program
called `global_emissions_cities.py` that will determine the contribution that the city emissions 
make to the global emissions.

## Loading the City Data

The city emissions data is located in a file called `CityCO2Emissions.csv`. This contains the coordinates of the city, along
with the total emissions (in MtC02e) as follows. Since the file is in CSV format, we can easily use the Pandas `read_csv`
method to load the data. Here is the first line of the file:

```
City,Country,Latitude,Longitude,Population (Millions),Total GHG (MtCO2e),Total GHG (tCO2e/cap)
```

> ## Challenge
>
> Write a program called `city_emissions_contribution.py` that loads the city emissions data
> from `CityCO2Emissions.csv` into a Pandas `DataFrame` and prints it out.
{: .challenge}

## Finding the Cities

In order to determine the contribution that the city emissions make to the global emissions, we need to first remove
the emissions from the global emissions data set.

The simplest way to do this is to use interpolation to determine the emissions in the global data set at a given location. 
We can do this using the [`RegularGridInterpolator`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RegularGridInterpolator.html#scipy.interpolate.RegularGridInterpolator) which is part of the 
SciPy Interpolation package ([`scipy.interpolate`](https://docs.scipy.org/doc/scipy/reference/interpolate.html#module-scipy.interpolate)). 
This class takes a set of points defining a regular grid (latitude/longitude in our case), and the data on the grid. The 
interplator can then be called with a specific coordinate and it will return an approximation at the point. By default, 
it will use "linear" interpolation, so we also need to specify that we want to use "nearest".

Assuming the latitude values are in a variable called `latitude`, longitude in `longitude` and the values in `global_emission_values`, 
we use the interpolator as follows:

```python
from scipy.interpolate import RegularGridInterpolator

emission_interpolator = RegularGridInterpolator([latitude, longitude], global_emission_values, method="nearest")
result = emission_interpolator(city_location)
```

Fortunately, our class provides the `latitude` and `longitude` data, and we can obtain the global emissions data using the 
`get_total_emissions_grid` method. The only tricky part is that we need to convert the emissions data into a 2-D array so
that it can be used by the interpolator. We also have to convert the values from gC/m2/s to MtCO2e. Fortunately
this just requires multiplying the values by `1.0e-12`.

Let's put this into the program and try it out:

```python
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from historical_co2_emissions import HistoricalCO2Emissions

year = '2005' # hard code this for now

if __name__ == "__main__":
    # Load city emissions data
    city_data = pd.read_csv('CityCO2Emissions.csv')
    
    # Load global emissions data
    emissions = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
	
    # Find the global emissions for the given year
    monthly_global_emissions = emissions.get_total_monthly_emissions_grid(year)
    
    # Sum and convert to MtC02e
    global_emissions = monthly_global_emissions.sum(level=[1,2]) * 1.0e-12
    
    # Convert to 2-D NumPy array
    global_emissions_values = global_emissions.unstack(level=1).values 

    # Interpolate the emissions for the city locations
    emission_interpolator = RegularGridInterpolator([emissions.latitude, emissions.longitude], global_emissions_values, method="nearest")
    city_emissions = emission_interpolator(city_data[['Latitude', 'Longitude']])
    print(result)
```

The final step in our analysis task is to calculate the total city emissions, the total global emissions, then an estimate of
how much the cites have contributed. 

We can calculate the total emissions from the cities by summing the data from the "Total GHG (MtCO2e)" column:

```python
total_city_emissions = city_data['Total GHG (MtCO2e)'].sum()
```

The emissions for the cities were calculated from the global data set and saved as `city_emissions`. We can just sum
this to find the total emissions:

```python
total_calc_emissions = city_emissions.sum()
```

Finally, we can obtain the total global emissions by summing the values in the `global_emissions_values` array, then
use this to estimate the city contribution and as a percentage of the global emissions as follows:

```python
city_contribution = total_city_emissions - total_calc_emissions
percent_contribution = city_contribution / global_emissions_values.sum() * 100.
```

> ## Challenge
>
> Add this code to your program and print out the final result, which is the percentage contribution of the cities.
> What value do you obtain?
>
> > ## Solution
> >
> > % of global emissions cities account for: 25.7745026041
> {: .solution}
{: .challenge}

## An Alternative

The `RegularGridInterpolator` we used is pretty simplistic. If we want to be able to specify the number of
nearest neighbors to use, for example, another approach would be to use a k-d tree
for nearest-neighbor lookup. The SciPy Spatial data structures and algorithms module 
([`scipi.spatial`](https://docs.scipy.org/doc/scipy/reference/spatial.html#module-scipy.spatial))
provides a [`cKDTree`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html#scipy.spatial.cKDTree)
class for this purpose. 

This class works differently from the interpolator in that it takes
N data points of dimension M. The nearest neighbor lookup is then performed by passing the coordinates to
the `query` method on the class, along with the number of neighbors. We can then sum up the values at each
of these points in the data set to obtain the desired value.

The first step is to construct the grid of points to use for the lookup. This needs to be an array of N
points, where each point is one of our grid elements. For example:

```python
[(-89.5, -179.5), (-89.5, -179.0), (-89.5, -178.5), ...]
```

Fortunately we already have the latitude and longitude values, so we can convert them into this format in 
two steps. The first step is to construct a mesh of all the possible values using the 
NumPy [`meshgrid`](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.meshgrid.html) function:

```python
import numpy as np
mx,my = np.meshgrid(emissions.latitude, emissions.longitude)
```

These meshes can then be used to construct the required array as follows:

```python
# construct array of pairs
lat_lon_values = np.array([mx,my])

# transpose rows and columns, then reshape
lat_lon_values = lat_lon_values.T.reshape(-1, 2)
```

We can do this all in one statement:

```python
lat_lon_values = np.array(np.meshgrid(emissions.latitude, emissions.longitude)).T.reshape(-1, 2)
```

It's now possible to use `cKDTree` to look up the nearest neighbors as follows:

```python
from scipy.spatial import cKDTree

kdtree = cKDTree(lat_lon_values)
query_dist, query_index = kdtree.query(city_data[['Latitude','Longitude'], k=neighbors)
```

The `query` method returns two arrays: the distance to the nearest neighbors
and the indices of the neighbors in the `lat_lon_values` array. We can use this index
array to find the sum of the elements we're interested in:

```python
emissions_index = lat_lon_values[query_index]
```

One issues is that to use this as an index into the `DataFrame`, it must be a tuple
containing a list of the latitude values and a list of the longitude values. Currently
it looks like this:

```python
[[[  40.5  -74.5]
  [  40.5  -73.5]
  [  41.5  -74.5]
  [  41.5  -73.5]]

...
```

Whereas it needs to be like this:

```python
([40.5, 40.5, 41.5, 41.5, ...], [-74.5, -73.5, -74.5, -73.5, ...])
```

We need to do some manipulation to get it into the right format. Here is the code
to do that and to calculate the sum:

```python
emissions_index = tuple(emissions_index.reshape(-1,2).T.tolist())
total_calc_emissions = global_emissions.to_frame().loc[emissions_index, :].sum())
```

> ## Challenge
> 
> Using the description above, modify the program so that it uses a k-d tree to determine
> the nearest neighbors. For bonus points, use a command-line argument to select between
> the two methods.
{: .challenge}

## Some Things You Didn't Know About Importing

Previously, we've seen that to include new functionality in a Python program, you need to *import* it.
There are a couple of different import statements: `import ... as` and `from ... import` but they
essentially do the same thing. So what is importing actually? And while we're at it, what is the difference between 
a "package" and a "module" anyway?

### Modules

In Python, a *module* is the name given to a series of executable statements in a single file. Usually
this file ends with `.py`, but that is not always necessary. 

When you import a module, it's almost exactly the same as if you entered the statements manually, or ran
the script using `python module.py`. The important difference is that for a statement like `import module`
or `import module as foo` it's as if the module name (or `foo.`) is added as a prefix to all the variables, functions,
classes, etc. imported from the module. In other words, the module has a *namespace* which is either the name 
of the module, or what it is imported as. This allows modules to use name without worrying about them clashing with
names used in the importing module. The exception to this is when you use the `from ... import ...``` variant.
In this case the names from the module are imported directly into the module, so they don't have to be prefixed
with anything. Of course in this case, you may get clashes between the names used in the current module and
those from the imported module.

So if module `a.py` contained:

```python
var = 4
```

then it could be used from module `b.py` as:

```python
import a
print(a.var) # prints 4
```

Modules are also only ever imported *once*. So multiple statements importing the same module will not result
in the module be run multiple times, although you can provide multiple namespaces for the same names
this way.

> ## Challenge
>
> Suppose module `a.py` contained the following:
>
> ```python
> var = [1,2]
> ```
>
> What would be the output from the running
> this script:
>
> ```python
> import a
> import a as c
>
> print(a.var)
> print(c.var)
> c.var.append(3)
> print(a.var)
> ```
> 
> > ## Solution
> >
> > ```
> > [1,2]
> > [1,2]
> > [1,2,3]
> > ```
> {: .solution}
{: .challenge}

Another important distinction between importing a module and running it as a script (using the
`python module.py` command is the value
of the global variable `__name__`. When you import a module, this variable is set to the name
of the module, however, when you run the module as a script this variable is set to `__main__`.
This enables code to be placed in the module that will only be executed when it is run as
as script, and why you see the following statement so often.

```
if __name__ == '__main__':
    ...
```

Any code that is placed inside the body of the `if` statement will only be executed when the
module is run, *not* when it is imported. This allows modules to be used both as libraries and
as programs, and also provides a great way of including test code with the module.

### Packages

Where does a package come into all this then? A package is really just a way of grouping modules
together in a more logical way, like putting all the modules related to Pandas in one place, and
all the modules relating to NetCDF4 in another place. Packages do also introduce a hierarchy, so
module `C` that is inside a directory `B` that is inside package `A` can be imported using the
statement `import A.B.C`.

A *package* is a directory tree with some Python files (modules) in it. If you want to tell Python that a 
certain directory is a package then just create a file called `__init__.py` and put it in the directory.
A package can contain other packages but to be useful, it must contain modules somewhere in it's hierarchy.

### Module Search Path

One final thing, how does Python know where to find modules like `numpy` or `pandas`? If the name is not
a built-in module, then it will search for the module in a list of directories given by the variable `sys.path`.

This variable is initialized from these locations:

- the directory containing the input script (or the current directory).
- the PYTHONPATH environment variable
- an installation-dependent default.

Since this list contains the current directory, it is possible to import modules in the same directory
as the program being run without needing to specify anything additional.

See the Python [Modules](https://docs.python.org/3.6/tutorial/modules.html) documentation for more details
on modules, packages, and importing.
