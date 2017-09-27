---
title: Visualizing the Data
teaching: 15
exercises: 30
questions:
    - " How can I use classes to make code reusable?"
objectives:
---

At the end of the last lesson we wrote a new program that calculated the 49 city's contribution
to the overall emissions. An example of what this program might look like is available 
[here](../code/city_emissions_contribution_06.py). 

Although we have completed the analysis that we set out to do, it would also be valuable to visualize the emissions
data with an overlay of the city locations. To do this, we're going to use the 
[Matplotlib basemap toolkit](https://matplotlib.org/basemap/users/intro.html).

The Matplotlib basemap toolkit is a library for plotting 2D data on maps in Python. It is similar in functionality to the 
MATLAB mapping toolbox, the IDL mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are other libraries 
that provide similar capabilities in Python.

Basemap does not do any plotting on it’s own, but provides the facilities to transform coordinates to one of 25 different 
map projections (using the PROJ.4 C library). Matplotlib is then used to plot contours, images, vectors, lines or points 
in the transformed coordinates.

Here is how to set up a basic plot. You can see there are various high-level methods available to configure how
the map is drawn, such as `drawcoastlines()`, `fillcontinents()`, etc. The `drawparallels()` and `drawmeridians()`
methods take an array specifying which parallels or meridians to draw (in degrees):

```python
from mpl_toolkits.basemap import Basemap

year = 2005

if __name__ == '__main__':
    # Setup the plot
    city_map = Basemap(projection='robin', lon_0=0)
    city_map.drawcoastlines()
    city_map.fillcontinents(color='0.75', lake_color='1')
    city_map.drawparallels(np.arange(-80.,81.,20.))
    city_map.drawmeridians(np.arange(-180.,181.,20.))
    city_map.drawmapboundary(fill_color='white')
```

Now we can load the emissions data for a particular year and calculate the global emissions in MtCO2e as we did before.

```python
    # Load global emissions data
    emissions = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')

    # Find the global emissions for the given year
    monthly_global_emissions = emissions.get_total_monthly_emissions_grid(year)
    
    # Sum and convert to MtC02
    global_emissions = monthly_global_emissions.sum(level=[1,2]) * 1.0e-12
    
    # Convert to 2-D NumPy array
    global_emissions_values = global_emissions.unstack(level=1).values 
```

Next we plot contours representing the emissions values. Calling a `Basemap` class instance with the arguments 
longitude and latitude will convert lon/lat (in degrees) to x/y map projection coordinates (in meters). These can
then be passed to the `contourf` method to plot the contours. The argument are the same as the Matplolib
`contourf` method.

```python
    lat_grid, lon_grid = np.meshgrid(emissions.latitude, emissions.longitude, indexing='ij')
    x_grid, y_grid = city_map(lon_grid, lat_grid)

    clevs = [0.1] + np.linspace(0.0,85,18)
    cont = city_map.contourf(x_grid, y_grid, global_emissions_values, clevs, cmap='Reds', zorder=100)
```

Once we have the emissions data, the next step is to load the city data and add it to the plot. This will simply
create a scatter plot of the city locations:

```python
    # Get city data 
    city_data = pd.read_csv('CityCO2Emissions.csv')

    x, y = city_map(np.array(city_data['Longitude'].tolist()), 
                    np.array(city_data['Latitude'].tolist()))
    
    city_map.scatter(x, y, 30, marker='o', edgecolors='m', facecolors='none', zorder=200)
```

Finally, add a title, color bar, and label, then plot it!

```python
    # Finish plot
     plt.title('The top 49 $CO_2$ emitting cities in 2005 [Hoornweg, 2010], \n ' +
            'located within the globally gridded $CO_2$ emissions (Mt;  '+
            '>1e-4) during ' + year)
    
    cbar = city_map.colorbar(cont, location='bottom', pad='5%')
    cbar.set_label('Mt $CO_2$')
    plt.show()
```

> ## Challenge
>
> Create a new Python program called `visualize_city_emissions.py` and add the above code to it. Test the
> program to make sure that it creates the plot as expected.
>
> > ## Solution
> >
> > You can download a version of this program [here](../code/visualize_city_emissions_07.py)
> {: .solution}
{: .challenge}

> ## Challenge
>
> Notice that we've used the same code to find the global emissions for a year in MtCO2 in two separate programs.
> It seems like this might be a good candidate for a new method in the `HistoricalCO2Emissions` class. Add a new
> method to this class called `get_total_emissions_Mt` that takes a string `year` as argument. It can return either
> a `DataFrame` or a NumPy array.
> 
> Once you have added this method, update the `city_emissions_contribution.py` and `visualize_city_emissions.py`
> programs to use the new method. Test both programs to make sure they still work correctly.
>
> > ## Solution
> >
> > You can download final versions of all three programs here:
> > - [`historical_co2_emissions.py`](../code/historical_co2_emissions.py)
> > - [`city_emissions_contribution.py`](../code/city_emissions_contribution.py)
> > - [`visualize_city_emissions.py`](../code/visualize_city_emissions.py)
> {: .solution}
{: .challenge}