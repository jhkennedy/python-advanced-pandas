---
title: Structuring the Data
teaching: 30
exercises: 30
questions:
    - " How can I use NetCDF in Pandas?"
    - " How should I structure my DataFrame?"
objectives:
---

We now have a Python program to load the NetCDF file and create a `Series` containing the emissions data. An example of what this
script might look like is available [here](../code/load_data_02.py). 

In order for the data to be useful, we must now consider how we intend to use it. Recall that our goal is to calculate the 
reduction in overall emissions if the top 50 cities are removed. We will do this by locating the cities in the CMIP5 dataset
by their latitude and longitude, removing the emissions from the surrounding N nearest-neighbor grid points considered to be
part of the city, then calculate the total remaining emissions.

Since we are interested in total emissions, it would make sense to pre-caculate these values. The fossil fuel (FF) variable
provided in the data set are in units of gC/m2/s (grams of carbon per meter squared per second) for each month in a particular
latitude/longitude grid. To convert these to the total emissions for the month across the grid, we need to multiple the FF
value by the area of each grid element (provided by the AREA variable) and by the number of seconds in the month.

First, using the time series function `date_range` it is possible to
create a fixed frequency `DateTimeIndex` with a period of months, a start data of 1751 and an end date of 2007. We can then
obtain the number of days in each month and convert these to seconds, as follows:

```python
months = pd.date_range('1751-01', '2008-01', freq='M')
seconds_in_month = months.days_in_month[:] * 24 * 60 * 60
```

Now we can calculate the total emissions for each month using the `ff` and `area` variables:

```python
total_emissions_per_month = ff[:,:,:] * area[:,:] * seconds_in_month[:, None, None]
```

Notice that we needed to specify `None` for the last two indices of `seconds_in_month`. This is because the
multiplication is done element-wise, so the arrays need to be compatible for *broadcasting*.

Now that we have the data ready, we can construct a `DataFrame` containing the total emissions data and insert the `Series`
we created previously as a column:

```python
emissions = pd.DataFrame(total_emissions_per_month.values.reshape(-1), index=emissions_index, columns=['Total Emissions Per Month'])
emissions['FF'] = ff_pd
print(emissions)
```
The resulting `DataFrame` looks like this:

```
                           Total Emissions Per Month   FF
Month  Latitude Longitude                                
1.0    -89.5    -179.5                           0.0  0.0
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
...                                              ...  ...
3084.0  89.5     150.5                           0.0  0.0
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


