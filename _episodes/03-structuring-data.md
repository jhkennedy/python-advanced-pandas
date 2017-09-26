---
title: Structuring the Data
teaching: 20
exercises: 30
questions:
    - " How can I improve how the data is structured?"
    - " How do I access hierarchical data?"
    - " How can I combine Series and DataFrames?"
objectives:
    - "See how Time Series can be used in MultiIndexes."
    - "See how to access hierarchical data using a MultiIndex."
    - "See how to create new columns from Series."
---

We now have a Python program to load the NetCDF file and create a `Series` containing the emissions data. An example of what this
script might look like is available [here](../code/historical_co2_emissions_02.py). 

In order for the data to be useful, we must now consider how we intend to use it. Recall that our goal is to calculate the 
reduction in overall emissions if the top 50 cities are removed. We will do this by locating the cities in the CMIP5 dataset
by their latitude and longitude, removing the emissions from the surrounding N nearest-neighbor grid points considered to be
part of the city, then calculate the total remaining emissions.

Since we are interested in total emissions, it would make sense to pre-caculate these values. The fossil fuel (FF) variable
provided in the data set are in units of gC/m2/s (grams of carbon per meter squared per second) for each month in a particular
latitude/longitude grid. To convert these to the total emissions for the month across the grid, we need to multiply the FF
value by the area of each grid element (provided by the AREA variable) and by the number of seconds in the month.

### Working with Time Series

First, using the time series function `date_range` it is possible to
create a fixed frequency `DateTimeIndex` with a period of months, a start data of 1751 and an end date of 2007. We can then
obtain the number of days in each month using the `days_in_month` method and convert these to seconds, as follows:

```python
months = pd.date_range('1751-01', '2008-01', freq='M')
seconds_in_month = months.days_in_month * 24 * 60 * 60
```

Now we can calculate the total emissions for each month using the `ff` and `area` arrays:

```python
total_emissions_per_month = ff * area * seconds_in_month[:, None, None].values
```

Notice that we needed to specify `None` for the last two indices of `seconds_in_month`. This is because the
multiplication is done element-wise, so the arrays need to be compatible for *broadcasting*. Also, we need
to access the NumnPy array using the `.values` attribute (otherwise the result will be an `Int64Index`.

### Combining DataFrames and Series

Now that we have the data ready, we can construct a `DataFrame` containing the total emissions data.
One change that might make the `DataFrame` more useful is if the index used actual dates 
rather than the `time_counter` values from the dataset. This can be accomplished by creating a hierarchical index
using the `DateTimeIndex` we created for `months` instead of the `time_counter` values we used before.

The code should look something like this:

```python
emissions_index = pd.MultiIndex.from_product([months, latitude, longitude], names=['Month','Latitude','Longitude'])
emissions = pd.DataFrame(total_emissions_per_month.reshape(-1), 
                   index=emissions_index, columns=['Total Emissions Per Month'])
```

Finally, we can insert the `Series` we created previously as a column (we need to create a new `Series` so that it has
the same index as the `DataFrame`):    
                   
```python
emissions['FF'] = pd.Series(ff.reshape(-1), index=emissions_index)
print(emissions)
```
The resulting `DataFrame` looks like this:

```
                               Total Emissions Per Month   FF
Month      Latitude Longitude                                
1751-01-31 -89.5    -179.5                           0.0  0.0
                    -178.5                           0.0  0.0
                    -177.5                           0.0  0.0
                    -176.5                           0.0  0.0
                    -175.5                           0.0  0.0
                    -174.5                           0.0  0.0
                    -173.5                           0.0  0.0
                    -172.5                           0.0  0.0
                    -171.5                           0.0  0.0
                    -170.5                           0.0  0.0
                    -169.5                           0.0  0.0
                    -168.5                           0.0  0.0
                    -167.5                           0.0  0.0
                    -166.5                           0.0  0.0
                    -165.5                           0.0  0.0
                    -164.5                           0.0  0.0
                    -163.5                           0.0  0.0
                    -162.5                           0.0  0.0
                    -161.5                           0.0  0.0
                    -160.5                           0.0  0.0
                    -159.5                           0.0  0.0
                    -158.5                           0.0  0.0
                    -157.5                           0.0  0.0
                    -156.5                           0.0  0.0
                    -155.5                           0.0  0.0
                    -154.5                           0.0  0.0
                    -153.5                           0.0  0.0
                    -152.5                           0.0  0.0
                    -151.5                           0.0  0.0
                    -150.5                           0.0  0.0
...                                                  ...  ...
2007-12-31  89.5     150.5                           0.0  0.0
                     151.5                           0.0  0.0
                     152.5                           0.0  0.0
                     153.5                           0.0  0.0
                     154.5                           0.0  0.0
                     155.5                           0.0  0.0
                     156.5                           0.0  0.0
                     157.5                           0.0  0.0
                     158.5                           0.0  0.0
                     159.5                           0.0  0.0
                     160.5                           0.0  0.0
                     161.5                           0.0  0.0
                     162.5                           0.0  0.0
                     163.5                           0.0  0.0
                     164.5                           0.0  0.0
                     165.5                           0.0  0.0
                     166.5                           0.0  0.0
                     167.5                           0.0  0.0
                     168.5                           0.0  0.0
                     169.5                           0.0  0.0
                     170.5                           0.0  0.0
                     171.5                           0.0  0.0
                     172.5                           0.0  0.0
                     173.5                           0.0  0.0
                     174.5                           0.0  0.0
                     175.5                           0.0  0.0
                     176.5                           0.0  0.0
                     177.5                           0.0  0.0
                     178.5                           0.0  0.0
                     179.5                           0.0  0.0

[199843200 rows x 2 columns]
```

> ## Challenge
>
> Add the code necessary to create the `emissions` `DataFrame` to your program. Run the program
> and verify that it produces the output you expected.
{: .challenge}

### Accessing Hierarchical Data

How do we go about accessing the data? If you recall from the [Introduction to Pandas](https://ornl-training.github.io/python-pandas) lesson, values in a Pandas `DataFrame`
are indexed using `.loc[row_indexer, column_indexer]`, `.loc[row_indexer, :]`, or just `.loc[row_indexer]` for just accessing by row index (this can
sometimes lead to ambiguities with `MultiIndex`). This is straightforward for a single level index, but becomes a little more tricky for hierarchical indexes. 

The simplest case is just to pass a value for each level of the index. For example `emissions.loc['2007-12-31']` would return emissions for all 
latitude and longitudes for the last month in 2007, or `emissions.loc['2007-12-31', 89.5, 179.5]` would return the emissions at the North Pole for that 
month (zero hopefully!) An alternative to the latter would be `emissions.loc[('2007-12-31', 89.5, 179.5), :]` where we use a tuple for the index levels.

It's also possible to use slicing with a range of values, such as `emissions.loc['2007-10-31':'2007-12-31']` or 
`emissions.loc[('2007-10-31', 89.5, 179.5):('2007-12-31', 89.5, 179.5), :]`.

> ## Challenge
> Try adding the following to you program and run it:
>
> ```python
> emissions.loc[('2007-10-31', 89.5, 179.5):('2007-12-31', 89.5, 179.5), :]
> ```
>
> What values are printed? Is this what you expected? 
>
> Remove the code when you have finished the challenge.
{: .challenge}

It get's a little more complicated if you want to slice *within* one of the index levels. Suppose we want to see the monthly emissions for the North Pole for the last year. 

We do this using *slices*. A `slice` is a Python builtin data type that represents a set of indices. The full syntax is `slice(start, stop, step)` and the arguments have the
same meaning as the `range()`. One difference from `range()` is that `slice(None)` can be used to specify "all the contents." Slices can be used for any level of the index.

So, to find the emissions from just the North Pole for the last year of the dataset, we would use:

```python
emissions.loc[(slice('2007-01-31', '2007-12-31'), 89.5, 179.5), :]
```

> ## Challenge
> Add a line to your program that will print the emissions from the rectangular region between the closest grid points to New York City (latitude 40.7, longitude -74.0)
> and Chicago (latitude 41.9, longitude -87.6) for the last month in the dataset.
> 
> Remove the code when you've finished the challenge.
>
> > ## Solution
> > ```python
> > print(emissions.loc[('2007-12-31', slice(40.5, 42.5), slice(-87.0, -73.5)), :])
> > ```
> > 
> > The output should be:
> > 
> > ```
> >                                Total Emissions Per Month        FF
> > Month      Latitude Longitude                                     
> > 2007-12-31 40.5     -86.5                   2.705674e+11  0.000011
> >                     -85.5                   2.705674e+11  0.000011
> >                     -84.5                   1.314247e+11  0.000005
> >                     -83.5                   1.314247e+11  0.000005
> >                     -82.5                   1.314247e+11  0.000005
> >                     -81.5                   3.726125e+11  0.000015
> >                     -80.5                   1.314247e+11  0.000005
> >                     -79.5                   1.658883e+12  0.000066
> >                     -78.5                   2.226637e+11  0.000009
> >                     -77.5                   2.226637e+11  0.000009
> >                     -76.5                   5.604422e+11  0.000022
> >                     -75.5                   3.653162e+12  0.000145
> >                     -74.5                   3.411376e+12  0.000136
> >                     -73.5                   1.704235e+12  0.000068
> >            41.5     -86.5                   2.664934e+11  0.000011
> >                     -85.5                   2.664934e+11  0.000011
> >                     -84.5                   1.294457e+11  0.000005
> >                     -83.5                   4.933789e+11  0.000020
> >                     -82.5                   0.000000e+00  0.000000
> >                     -81.5                   1.806908e+12  0.000073
> >                     -80.5                   4.419064e+11  0.000018
> >                     -79.5                   2.193108e+11  0.000009
> >                     -78.5                   2.193108e+11  0.000009
> >                     -77.5                   2.193108e+11  0.000009
> >                     -76.5                   2.193108e+11  0.000009
> >                     -75.5                   2.193108e+11  0.000009
> >                     -74.5                   5.104873e+12  0.000206
> >                     -73.5                   5.160241e+11  0.000021
> >            42.5     -86.5                   0.000000e+00  0.000000
> >                     -85.5                   5.217427e+11  0.000021
> >                     -84.5                   1.560775e+11  0.000006
> >                     -83.5                   2.912191e+12  0.000119
> >                     -82.5                   1.550174e+11  0.000006
> >                     -81.5                   1.806039e+11  0.000007
> >                     -80.5                   0.000000e+00  0.000000
> >                     -79.5                   1.409411e+11  0.000006
> >                     -78.5                   8.748447e+11  0.000036
> >                     -77.5                   1.409411e+11  0.000006
> >                     -76.5                   1.409411e+11  0.000006
> >                     -75.5                   1.409411e+11  0.000006
> >                     -74.5                   1.409411e+11  0.000006
> >                     -73.5                   6.440737e+11  0.000026
> > ```
> {: .solution}
{: .challenge}
