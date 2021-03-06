---
title: Creating a Class
teaching: 20
exercises: 15
questions:
    - " How can I use a class to make code reusable?"
    - " What do I need to do to turn my code into a class?"
objectives:
    - "See how to restructured existing code into a class."
    - "See how to make use of object oriented programming principles."
    - "See how to improve code reuse."
---

At the end of the last lesson our program was able to load the NetCDF file and create a 
`DataFrame` containing the emissions and total emissions data. An example of what this
program might look like is available [here](../code/historical_co2_emissions_03.py). 

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
       
    def get_total_monthly_emissions_grid(self, start_month, end_month=None):
        ''' Find the total monthly emissions for all latitudes and longitudes on a grid
            Parameters:
               start_month - First month to include in the results in the format 'YYYY-MM'
               end_month - Optional final month to include in the results in the format 'YYYY-MM'
            Returns:
                total monthly emissions for all latitudes and logitudes on a grid in gC/m2/s
        '''
        return None
```

## Loading the Data

We've already seen how to load the data set, this code can be transferred directly to the constructor of our class.
We'll also keep instance attributes for the latitude and longitude values so we can use them later.
The new version of the `__init__` method no longer needs a `return None` statement, since this is what
is returned implicitly anyway.

The new code looks like this:

```python
    def __init__(self, filename):
        #
        # Load dataset and create variable references
        #
        dataset = nc.Dataset(filename)
        ff = dataset.variables['FF'][:,:,:]
        area = dataset.variables['AREA'][:,:]
        
        # Keep these as instance attributes
        self.latitude = dataset.variables['Latitude'][:]
        self.longitude = dataset.variables['Longitude'][:]
```

Our constructor should also create the `DataFrame` since this is ultimately what we'll be referring to
from our other methods. 

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
        total_emissions_per_month = ff * area * seconds_in_month[:, None, None].values

        #
        # Create a MultiIndex for the emissions data using the DateTimeIndex and lat/lon values
        #
        emissions_index = pd.MultiIndex.from_product([months, self.latitude, self.longitude], names=['Month', 'Latitude', 'Longitude'])

        #
        # Create a DataFrame for the fossil fuel and total emissions data 
        #
        self.emissions = pd.DataFrame(total_emissions_per_month.reshape(-1), 
                                index=emissions_index, columns=['Total Per Month'])

        #
        # Add the fossil fuel data to the DataFrame
        #
        self.emissions['Fossil Fuel'] = pd.Series(ff.reshape(-1), index=emissions_index)
```

## Defining Methods

We decided that a `get_total_monthly_emissions_grid` method would be useful, so let's see how we go about implementing it. It turns out
that we've already done most of the hard work. All we really need to do is use the `start_month` and `end_month` parameters to slice
the `DataFrame`, then return the `Total Per Month` values. Remember to check if `end_month` is `None` and return a specific month's worth
of data. We can replace the `return None` line with the following:

```python
        if end_month is None:
            return self.emissions.loc[start_month, :]['Total Per Month']
           
        return self.emissions.loc[(slice(start_month, end_month), slice(None), slice(None)), :]['Total Per Month']
```

> ## Why so complicated?
>
> Why can't we just use the following?
>
> ```python
>         return self.emissions.loc[start_month:end_month]['Total Per Month']
> ```
>
> It turns out that if we were using a single level index rather than a hierarchical index, we would be
> able to. Unfortunately for hierarchical indexes we must use the full slice notation for it to
> work properly. Hopefully this will be resolved in a future version of Pandas.

> ## Challenge
> 
> So far we've described all the pieces of the class that required. Your job is now to put all this
> into the `historical_co2_emissions.py` program and make sure that it works.
>
> Once you have the class defined correctly, you can test out the program by adding the following
> code to the end. Run it and check that you're getting the expected results.
>
> ```python
> if __name__ == '__main__':
>     df = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
>     print(df.get_total_monthly_emissions_grid('2001-06', '2002-06')) # One year's data
>     print(df.get_total_monthly_emissions_grid('1999-04')) # One month's data
> ```
{: .challenge}

      