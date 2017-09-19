---
title: Data Formats
teaching: 30
exercises: 30
questions:
    - " How can I import data using Pandas?"
    - " What is NetCDF?"
    - " What tools are available to work with NetCDF?"
objectives:
    - "Describe the data formats supported by Pandas."
    - "Show examples of reading/writing data formats."
    - "Describe other data formats used for GIS data."
---

# Working With Data Formats in Python and Pandas

## Pandas Built-in Formats

Pandas provides a variety of tools for reading and writing textual and binary file formats. For textual formats, the most common of these are:

<table border="1">
<tbody>
<tr>
<td>Format</td>
<td>Example</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Comma-separated_values">CSV</a></td>
<td><pre>
import pandas as pd
df = pd.read_csv(filename, delimiter, header, ...)
</pre></td>
</tr>
<tr>
<td><a href="http://www.json.org/">JSON</a></td>
<td><pre>
import pandas as pd
df = pd.read_json('https://api.github.com/repos/pydata/pandas/issues?per_page=5')
</pre></td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/HTML">HTML</a></td>
<td><pre>
import pandas as pd
df = pd.read_html('http://www.fdic.gov/bank/individual/failed/banklist.html')
</pre></td>
</tr>
</tbody>
</table>

Pandas also supports reading and writing a variety of binary data formats, including:

<table border="1">
<tbody>
<tr>
<td>Format</td>
<td>Example</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Microsoft_Excel">Excel</a></td>
<td>
<pre>import pandas as pd
df = pd.DataFrame({'a':[1,2,3,4], 'b':[5,6,7,8]}, index=pd.MultiIndex.from_product([['a','b'],['c','d']]))
df.to_excel('df.excel.xlsx')
xlsx = pd.ExcelFile('df.xlsx')
pd.read_excel(xlsx, 'Sheet1')
</pre>
</td>
</tr>
<tr>
<td><a href="https://support.hdfgroup.org/HDF5/whatishdf5.html">HDF5</a></td>
<td>
<pre>
import pandas as pd
df = pd.DataFrame(dict(A=list(range(5)), B=list(range(5))))
df.to_hdf('df.h5','table',append=True)
pd.read_hdf('df.h5', 'table', where = ['index>2'])
</pre>
</td>
</tr>
<tr>
<td><a href="https://github.com/wesm/feather">Feather</a></td>
<td>
<pre>
import pandas as pd
df = pd.DataFrame(dict(A=list(range(5)), B=list(range(5))))
df.to_feather('df.feather')
pd.read_feather('df.feather')
</pre>
</td>
</tr>
<tr>
<td><a href="http://msgpack.org/index.html">Msgpack</a></td>
<td>
<pre>
import pandas as pd
df = pd.DataFrame(np.random.rand(5,2),columns=list('AB'))
df.to_msgpack('df.msg')
pd.read_msgpack('df.msg')
</pre>
</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Stata">Stata</a></td>
<td>
<pre>
import pandas as pd
df = pd.DataFrame(np.random.randn(10, 2), columns=list('AB'))
df.to_stata('df.dta')
pd.read_stata('df.dta')
</pre>
</td>
</tr>
<tr>
<td><a href="https://docs.python.org/3/library/pickle.html">Pickle</a></td>
<td>
<pre>
import pandas as pd
df = pd.DataFrame(np.random.rand(5,2),columns=list('AB'))
df.to_pickle("df.pkl.gz", compression="gzip")
pd.read_pickle("df.pkl.gz", compression="gzip")
</pre>
</td>
</tr>
</tbody>
</table>

Pandas also provides tools for managing SAS, SQL, and Google BigQuery formats. Please refer to the Pandas documentation for more information.

## [NetCDF](https://www.unidata.ucar.edu/software/netcdf/)

The Network Common Data Form (NetCDF) is a set of libraries and self-describing machine-independent data formats that support the creation, access, 
and sharing of array-oriented scientific data. NetCDF was developed and is maintained at Unidata, part of the University Corporation for Atmospheric 
Research (UCAR) Office of Programs (UOP). Unidata is funded primarily by the National Science Foundation.

Pandas does not have native support for reading/writing NetCDF, however there are a number of additional packages that provide this capability:

- netcdf4-python: a Python interface to the netCDF library
- PyNIO: a Python package that allows read and/or write access to a variety of data formats using an interface modeled on netCDF
- xarray: provides N-dimensional variants of the core pandas data structures

### NetCDF Data Model

The "classic" NetCDF data model consists of the following components:

- Variables: N-dimensional arrays of data. Variables in netCDF files can be one of six types (char, byte, short, int, float, double).
- Dimensions: These describe the axes of the data arrays. A dimension has a name and a length. An unlimited dimension has a length that can be expanded at any time, as more data are written to it. NetCDF files can contain at most one unlimited dimension.
- Attributes: These annotate variables or files with small notes or supplementary metadata. Attributes are always scalar values or 1D arrays, which can be associated with either a variable or the file as a whole. Although there is no enforced limit, the user is expected to keep attributes small.

In addition, the "common data model" introduced in NetCDF-4 includes the following:

- Groups: These provide a way of hierarchically organizing data, similar to directories in a Unix file system.
- User-defined types: These allow the definition of compound types (like C structures), enumeration types, variable length arrays, and opaque types.

### Meteorological Example

NetCDF can be used to store many kinds of data, but it was originally developed for the Earth science community.

NetCDF views the world of scientific data in the same way that an atmospheric scientist might: as sets of related arrays. There are various physical quantities (such as pressure and temperature) located at points at a particular latitude, longitude, vertical level, and time. A scientist might also like to store supporting information, such as the units, or some information about how the data were produced.

The axis information (latitude, longitude, level, and time) would be stored as netCDF dimensions. Dimensions have a length and a name.

The physical quantities (pressure, temperature) would be stored as netCDF variables. Variables are N-dimensional arrays of data, with a name and an associated set of netCDF dimensions.

It is also customary to add one variable for each dimension, to hold the values along that axis. These variables are call “coordinate variables.” The latitude coordinate variable would be a one-dimensional variable (with latitude as its dimension), and it would hold the latitude values at each point along the axis.

The additional bits of metadata would be stored as netCDF attributes. Attributes are always single values or one-dimensional arrays. (This works out well for a string, which is a one-dimensional array of ASCII characters.)

![Dataset Diagram](../fig/01_dataset_diagram.png)

### netCDF4

Although there are a number of packages for reading NetCDF files, we will just be working with `netcdf4-python` for this tutorial.

#### Opening a file

To open a netCDF file from python, you simply call the Dataset() constructor as follows:

```python
from netCDF4 import Dataset 
dataset = Dataset('data.nc')
print(dataset.file_format)
```

#### Working with "Classic" NetCDF

The netCDF4 module can read in any netCDF format. This tutorial will focus exclusively on the NetCDF-
"classic" data model using: NETCDF4_CLASSIC

The "classic" data model is made up of dimensions, variables and attributes only.

#### Interrogating Dimensions

You can interrogate dimensions using simple dictionary calls:

```python
print(dataset.dimensions.keys())
print(dataset.dimensions['time'])
```

This would result in the output:

```
['time', 'latitude', 'bound', 'longitude'])
<type 'netCDF4.Dimension'> (unlimited):
    name = 'time', size = 1
```

#### Interrogating Variables

You can interrogate variables using simple dictionary calls:

```python
for key in dataset.variables.keys():
  var = dataset.variables[key]
  print("name =", key)
```

This would result in the output:

```
name = tcc
name = time
name = latitude
name = longitude
```

Notice that you can access a variable by its key:

```python
var = dataset.variables['tcc']
print(" dims =", var.dimensions)
print(" shape =", var.shape)
print(" size =", var.size)
print(" ndim =", var.ndim)
print(" datatype =", var.datatype){: .python}
```

Which would result in:

```
dims = ('time', 'latitude', 'longitude')
shape = (1, 181, 360)
size = 65160
ndim = 3
datatype = float32
```

#### Global Attributes

Global attributes are available as attributes of the python dataset instance:

```python
# Find all NetCDF global attributes
print(dataset.ncattrs())
for attr in dataset.ncattrs():
    print(attr, '=', getattr(dataset, attr))
```

Results in:

```
['Conventions', 'history']
Conventions = CF-1.0
history = Written in a hurry on a Tuesday!
```

#### Variable Attributes

Variable attributes are available as attributes of the python variable instance:

```python
var = dataset.variables['windspeed']
# Get units attribute
print(var.units)
# Find all variable attributes
for attr in var.ncattrs():
    print(attr, '=', getattr(var, attr))
```

Results in:

```
m/s
long_name = Wind speed
Units = m/s
```

> ## Challenge
> Write a Python script to open the CIMP5 global emissions dataset. Call the script `load_data.py`. Use your knowledge of netCDF4 to answer
> the following questions:
> 
> 1. How many dimensions does the dataset contain? What are the sizes of the dimensions?
> 2. How many variables does the dataset contain, and what are their names and dimensions?
> 3. What do you think the purpose of the 'FF' variable is?
{: .challenge}
