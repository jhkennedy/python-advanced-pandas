---
title: Analyzing the Data
teaching: 30
exercises: 30
questions:
    - " How can I use classes to make code reusable?"
objectives:
---

At the end of the last lesson our program provided a class for managing the emissions data. 
An example of what this program might look like is available [here](../code/load_data_04.py). 

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
> Write a program called `global_emissions_cities.py` that loads the city emissions data
> from `CityCO2Emissions.csv` into a Pands `DataFrame` and prints it out.
>
> > ## Solution
> > 
> > ```python
> > import pandas as pd
> > 
> > if __name__ == "__main__":
> >     # Load city emissions data
> > 	    city_data = pd.read_csv('CityCO2Emissions.csv')
> > 	    print(city_data)
> > ```
> {: .solution}
{: .challenge}

## Finding the Cities

In order to determine the contribution that the city emissions make to the global emissions, we need to first remove
the emissions from the global emissions data set.

The simplest way to do this is to use interpolation to determine the emissions in the global data set at a given location. 
We can do this using the `RegularGridInterpolator` which is part of the SciPy Interpolation package (`scipy.interpolate`). 
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
    global_emissions = emissions.get_total_emissions_grid(year)
    
    # convert to MtC02e
    global_emissions *= 1.0e-12
    
    # convert to 2-D array of values
    global_emissions_values = global_emissions.unstack(level=1).values 

    # Interpolate the emissions for the city locations
    emission_interpolator = RegularGridInterpolator([emissions.latitude, emissions.longitude], global_emissions_values, method="nearest")
    city_emissions = emission_interpolator(city_data[['Latitude', 'Longitude']])
    print(result)
```

The final step in our analysis task is to calculate the total city emissions, the total global emissions, then an estimate of
how much the cites have contributed. 

The total emissions from the cities is calculated as follows:

```python
total_city_emissions = city_data['Total GHG (MtCO2e)'].sum()
```

The total emissions for the cities we calculated from the global data set is:

```python
total_calc_emissions = city_emissions.sum()
```

We can then estimate the city contribution and as a percentage of the global emissions as follows:

```python
city_contribution = total_city_emissions - total_calc_emissions
percent_contribution = city_contribution / global_emissions_values.sum() * 100.
```

> ## Challenge
>
> Add this code to your program and print out the final result, which is the percentage contribution of the cities.
>
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
