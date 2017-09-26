---
title: Visualizing the Data
teaching: 30
exercises: 30
questions:
    - " How can I use classes to make code reusable?"
objectives:
---

At the end of the last lesson we wrote a new program that calculated the to 49 city's contribution
to the overall emissions. An example of what this program might look like is available 
[here](../code/city_emissions_contribution.py). 

Although we have completed the analysis that we set out to do, it would also be valuable to visualize the emissions
data with an overlay of the city locations. To do this, we're going to use the 
[Matplotlib basemap toolkit](https://matplotlib.org/basemap/users/intro.html).

The Matplotlib basemap toolkit is a library for plotting 2D data on maps in Python. It is similar in functionality to the 
MATLAB mapping toolbox, the IDL mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are other libraries 
that provide similar capabilities in Python.

Here is how to set up a basic plot:

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

Now we can load the emissions data for a particular year.

```python
    # Load global emissions data
    emissions = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')

    # Find the global emissions for the given year
    global_emissions = emissions.get_total_emissions_grid(year)

    # convert to MtC02e
    global_emissions *= 1.0e-12
```

Plot contours 

```python
    x_grid, y_grid = city_map(emis.lon_grid, emis.lat_grid)

    clevs = [0.1] + np.linspace(0.0,85,18)
    cont = city_map.contourf(x_grid, y_grid, emis_year_Mt.unstack(level=1).values, clevs, cmap='Reds', zorder=100)

    # Show the emissions grid
    city_map.scatter(x_grid, y_grid, 10, marker='+', color='b', zorder=150)
```

Load the city data and add to the plot:

```python
    # Get city data 
    city_data = pandas.read_csv(args.cities)

    x, y = city_map(np.array(city_data['Longitude'].tolist()), 
                    np.array(city_data['Latitude'].tolist()))
    
    city_map.scatter(x, y, 30, marker='o', edgecolors='m', facecolors='none', zorder=200)
```

Add title, color bar, and label, then plot it!

```python
    # Finish plot
     plt.title('The top 49 $CO_2$ emitting cities in 2005 [Hoornweg, 2010], \n '+
            'located within the globally gridded $CO_2$ emissions (Mt; '+
            '>1e-4) during '+str(args.year))
    
    cbar = city_map.colorbar(cont, location='bottom', pad='5%')
    cbar.set_label('Mt $CO_2$')
    plt.show()
```