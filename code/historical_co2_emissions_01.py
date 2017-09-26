#
# Program to load the CMIP5 emissions dataset
#
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
