---
title: Creating an Emissions Class
teaching: 30
exercises: 30
questions:
    - " How can I use classes to make code reusable?"
objectives:
---

At the end of the last lesson we our program was able to load the NetCDF file and create a 
`DataFrame` containing the emissions and total emissions data. An example of what this
program might look like is available [here](../code/load_data_03.py). 

Let's look at how we can turn what we've done so far into a reusable Python program. We
ultimately want to be able to manipulate the emissions data in order to examine the impact that
large city emissions have on it. One approach might be to provide a class that loads the data and
then performs some operations on it to make it more usable. This data can be kept in attributes
until it is needed, such as when we want to retrieve information about the emissions. We could
provide some helpful methods that enable the emissions information to be easily accessed. 

Let's break this down into a number of steps.

> ## What's in a name?
>
> To follow clean code naming principles, classes and objects should have noun or noun phrase names like 
> "Customer", "WikiPage", "Account", and "AddressParser". Avoid generic words like "Manager", "Processor",
> "Data", or "Info" in the name of a class. A class name should not be a verb.
> 
> Methods should have verb or verb phrase names like "post_payment", "delete_page", or "save".
{: .callout}

## Defining the Class

Let's choose name for the class that reflects what it is. Feel free to choose something different if you think it
better reflects the purpose of the class. We're going to avoid putting things like "Gridded" and "Monthly" in the
name, since these might prevent the class from being extended in the future. We'll also follow the Python approach of capitalizing
the first letter of each word.

We'll also define some methods we think we might need for our later work. The methods will just return `None` for now, until
we're ready to write them.

```python
class HistoricalCO2Emissions():
    ''' Class that represents historical C02 emissions. The constructor expects a file name or
        path the points to a dataset in NetCDF4 format.
    '''
    
    def __init__(self, filename):
       return None
       
    def get_total_monthly_emissions_grid(self, from_month, to_month=None):
        ''' Find the total monthly emissions for all latitudes and longitudes on a grid
            Parameters:
               from_month - First month to include in the results in the format 'YYYY-MM'
               to_month - Optional final month to include in the results in the format 'YYYY-MM'
            Returns:
                total monthly emissions for all latitudes and logitudes on a grid
        '''
        return None
```

## Loading the Data

We've already seen how to load the dataset, and it's probably worth keeping instance attributes for each of
the NetCDF variables in the dataset. This code can be transferred directly to the constructor of our class.
The new version of the `__init__` method no longer needs a `return None` statement, since this is what
is returned implicitly anyway.

The new code looks like this:

```python
    def __init__(self, filename):
        #
        # Load dataset and create variable references
        #
        self.dataset = nc.Dataset(filename)
        self.lat = self.dataset.variables['Latitude'][:]
        self.lon = self.dataset.variables['Longitude'][:]
        self.tc = self.dataset.variables['time_counter'][:]  
        self.ff = self.dataset.variables['FF'][:,:,:]
        self.area = self.dataset.variables['AREA'][:,:]
```

Our constructor should also create the `DataFrame` since this is ultimately what we'll be referring to
from our other methods. 

One change that might make the `DataFrame` more useful is if the index used actual dates rather than the
`time_counter` values from the dataset. This can be accomplised by simply re-arranging when we create
the `MultiIndex` and using the `DateTimeIndex` we created for `months` instead of the `time_counter` values.

Here is the extra code we'll add to the `__init__` method. Notice that we've had `self.` to some variables
as these are now instance attributes:

```python
        #
        # Create a DateTimeIndex representing the months between Jan 1751 and  Dec 2007
        #
        months = pd.date_range('1751-01', '2008-01', freq='M') 

        # 
        # Calculate the number of seconds in each month
        #
        seconds_in_month = months.days_in_month[:] * 24 * 60 * 60

        # 
        # Compute the total emissions for each grid element
        #
        total_emissions_per_month = self.ff * self.area * seconds_in_month[:, None, None]

        #
        # Create a MultiIndex for the emissions data using the DateTimeIndex and lat/lon values
        #
        emissions_index = pd.MultiIndex.from_product([months, self.lat, self.lon], names=['Month', 'Latitude', 'Longitude'])

        #
        # Create a DataFrame for the fossil fuel and total emissions data 
        #
        self.emissions = pd.DataFrame(total_emissions_per_month.values.reshape(-1), 
                                index=emissions_index, columns=['Total Per Month'])

        #
        # Add the fossil fuel data to the DataFrame
        #
        self.emissions['Fossil Fuel'] = pd.Series(self.ff.reshape(-1), index=emissions_index)
```

## Defining Methods

We decided that a `get_total_monthly_emissions_grid` method would be useful, so let's see how we go about implementing it. It turns out
that we've already done most of the hard work. All we really need to do is use the `from_month` and `to_month` parameters to slice
the `DataFrame`, then return the `Total Per Month` values. Remember to check if `to_month` is `None` and return a specific month's worth
of data. We can replace the `return None` line with the following:

```python
        if to_month is None:
            return self.emissions.loc[from_month, :]['Total Per Month']
           
        return self.emissions.loc[(slice(from_month, to_month), slice(None), slice(None)), :]['Total Per Month']
```

> ## Why so complicated?
>
> Why can't we just use the following?
>
> ```python
> return self.emissions.loc[to_month:from_month,:]['Total Per Month']
> ```
>
> It turns out that if we were using a single level index rather than a hierarchical index, we would be
> able to. Unfortunately for hierarchical indexes we must use the full slice notation for it to
> work properly. Hopefully this will be resolved in a future version of Pandas.

> ## Challenge
> 
> So far we've described all the pieces of the class that required. Your job is now to put all this
> into the `load_data.py` program and make sure that it works.
>
> Once you have the class defined correctly, you can test out the program by adding the following
> code to the end. Run it and check that you're getting the expected results.
>
> ```python
> df = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
> print(df.get_total_monthly_emissions_grid('2001-06', '2002-06')) # One year's data
> print(df.get_total_monthly_emissions_grid('1999-04')) # One month's data
{: .challenge}

      