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

    # Calculate percent contribution
    total_city_emissions = city_data['Total GHG (MtCO2e)'].sum()
    total_calc_emissions = city_emissions.sum()
    city_contribution = total_city_emissions - total_calc_emissions
    percent_contribution = city_contribution / global_emissions_values.sum() * 100.

    print('% global emissions cities account for:', percent_contribution)
