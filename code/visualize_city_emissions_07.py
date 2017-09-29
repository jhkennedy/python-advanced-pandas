import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from historical_co2_emissions import HistoricalCO2Emissions

year = '2005' # hard code this for now

if __name__ == '__main__':
    # Setup the plot
    city_map = Basemap(projection='robin', lon_0=0)
    city_map.drawcoastlines()
    city_map.fillcontinents(color='0.75', lake_color='1')
    city_map.drawparallels(np.arange(-80.,81.,20.))
    city_map.drawmeridians(np.arange(-180.,181.,20.))
    city_map.drawmapboundary(fill_color='white')

    # Load city emissions data
    city_data = pd.read_csv('CityCO2Emissions.csv')
    
    # Load global emissions data
    emissions = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
	
    # Find the global emissions for the given year
    global_emissions = emissions.get_total_emissions_grid(year).sum(level=[1,2])
    
    # convert to MtC02e
    global_emissions *= 1.0e-12
    
    # convert to 2-D array of values
    global_emissions_values = global_emissions.unstack(level=1).values 

    # Plot contours
    lat_grid, lon_grid = np.meshgrid(emissions.latitude, emissions.longitude, indexing='ij')
    x_grid, y_grid = city_map(lon_grid, lat_grid)

    clevs = [0.1] + np.linspace(0.0,85,18)
    cont = city_map.contourf(x_grid, y_grid, global_emissions_values, clevs, cmap='Reds', zorder=100)
    
    # Plot cities
    x, y = city_map(np.array(city_data['Longitude'].tolist()), 
                    np.array(city_data['Latitude'].tolist()))
    
    city_map.scatter(x, y, 30, marker='o', edgecolors='m', facecolors='none', zorder=200)

    # Finish plot
    plt.title('The top 49 $CO_2$ emitting cities in 2005 [Hoornweg, 2010], \n ' +
            'located within the globally gridded $CO_2$ emissions (Mt;  '+
            '>1e-4) during ' + year)
    
    cbar = city_map.colorbar(cont, location='bottom', pad='5%')
    cbar.set_label('Mt $CO_2$')
    plt.show()