#
# Program to load the CMIP5 emissions dataset
#
import pandas as pd
import netCDF4 as nc

ds = nc.Dataset('CMIP5_gridcar_CO2_emissions_fossil_fuel_Andres_1751-2007_monthly_SC_mask11.nc')

#
# Display some information about the dataset
#
for dim in ds.dimensions:
  print(dim, '=', ds.dimensions[dim])
  
for key in ds.variables.keys():
  var = ds.variables[key]
  print("name =", key)
  print(" dims =", var.dimensions)
  print(" shape =", var.shape)
  print(" size =", var.size)
  print(" ndim =", var.ndim)
  print(" datatype =", var.datatype)

#
# Obtain ndarray's for each dataset variable
#
lat = ds.variables['Latitude'][:]
lon = ds.variables['Longitude'][:]
tc = ds.variables['time_counter'][:]
ff = ds.variables['FF'][:,:,:]

#
# Create a multiindex for the emissions data
#
emissions_index = pd.MultiIndex.from_product([tc, lat, lon], names=['Month', 'Latitude', 'Longitude'])

#
# Create a series representing the emissions data
#
ff_pd = pd.Series(ff, index=emissions_index)
print(ff_pd)

