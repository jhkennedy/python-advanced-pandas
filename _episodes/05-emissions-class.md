---
title: An Emissions Class
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
       
    def total_monthly_emissions_grid(from_month, to_month):
        ''' Find the total monthly emissions for all latitudes and longitudes on a grid
            Parameters:
               from_month - Start month in the format 'YYYY-MM'
               to_month - End month in format 'YYYY-MM'
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
from our other methods. We'll also add the following code to the `__init__` method:

```python
        #
        # Create a multiindex for the emissions data 
        #
        emissions_index = pd.MultiIndex.from_product([tc, lat, lon], names=['Month', 'Latitude', 'Longitude'])

        #
        # Create a series representing the emissions data
        #
        ff_pd = pd.Series(ff, index=emissions_index)

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
        total_emissions_per_month = ff * area * seconds_in_month[:, None, None]

        #
        # Create a dataframe with the fossil fuel and total emissions data 
        #
        self.emissions = pd.DataFrame(total_emissions_per_month.values.reshape(-1), 
                                index=emissions_index, columns=['Total Emissions Per Month'])
        self.emissions['FF'] = ff_pd
```

## Defining Methods


      