#
# Program to manage the CMIP5 emissions dataset
#
import pandas as pd
import netCDF4 as nc

#
# Constants
#
MOLAR_MASS_AIR = 28.966 # g/Mol
MEAN_MASS_AIR = 5.1480e21 # g
MOLAR_MASS_C = 12.01 # g/Mol
PPM_C_1752 = 276.39 # Mol/(Mol/1e6)

class HistoricalCO2Emissions():
    ''' Class that represents historical C02 emissions. The constructor expects a file name or
        path the points to a dataset in NetCDF4 format.
    '''
    
    
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
               
    def get_total_monthly_emissions_grid(self, from_month, to_month=None):
        ''' Find the total monthly emissions for all latitudes and longitudes on a grid
            Parameters:
               from_month - First month to include in the results in the format 'YYYY-MM'
               to_month - Optional final month to include in the results in the format 'YYYY-MM'
            Returns:
                total monthly emissions for all latitudes and logitudes on a grid in gC/m2/s
        '''
        if to_month is None:
            return self.emissions.loc[from_month, :]['Total Per Month']
           
        return self.emissions.loc[(slice(from_month, to_month), slice(None), slice(None)), :]['Total Per Month']
        
    def get_total_emissions_grid_Mt(self, year):
        ''' Find the total emissions for a particular year for all latitudes and longitudes on a grid in Mt
            Parameters:
               year - Year to include in the results in the format 'YYYY'
            Returns:
                total emissions for all latitudes and logitudes on a grid in Mt
        '''
        total = self.get_total_monthly_emissions_grid(from_month, to_month)
        total_sum = total.sum(level=[1,2])
        return (total_sum / MOLAR_MASS_C) / (MEAN_MASS_AIR / MOLAR_MASS_AIR) * 1.e-6

if __name__ == '__main__':
    df = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
    print(df.get_total_monthly_emissions_grid('2001-06', '2002-06')) # One year's data
    print(df.get_total_monthly_emissions_grid('1999-04')) # One month's data