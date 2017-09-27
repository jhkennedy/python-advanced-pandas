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
        dataset = nc.Dataset(filename)
        ff = dataset.variables['FF'][:,:,:]
        area = dataset.variables['AREA'][:,:]
                
        # Keep these as instance attributes
        self.latitude = dataset.variables['Latitude'][:]
        self.longitude = dataset.variables['Longitude'][:]
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
               
    def get_total_monthly_emissions_grid(self, start_month, end_month=None):
        ''' Find the total monthly emissions for all latitudes and longitudes on a grid
            Parameters:
               start_month - First month to include in the results in the format 'YYYY-MM'
               end_month - Optional final month to include in the results in the format 'YYYY-MM'
            Returns:
                total monthly emissions for all latitudes and longitudes on a grid in gC/m2/s
        '''
        if end_month is None:
            return self.emissions.loc[start_month, :]['Total Per Month']
           
        return self.emissions.loc[(slice(start_month, end_month), slice(None), slice(None)), :]['Total Per Month']
        
if __name__ == '__main__':
    df = HistoricalCO2Emissions('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')
    print(df.get_total_monthly_emissions_grid('2001-06', '2002-06')) # One year's data
    print(df.get_total_monthly_emissions_grid('1999-04')) # One month's data