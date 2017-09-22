---
title: Using NetCDF with Pandas
teaching: 30
exercises: 30
questions:
    - " How can I use NetCDF in Pandas?"
    - " How should I structure my DataFrame?"
objectives:
---

In the last module, we wrote a simple Python program to load the NetCDF data and print some useful information about it. An example of what this
script might look like is available [here](../code/load_data_01.py). We also saw that the data is accessible as NumPy arrays. However, it would be much more useful
if we could store the data as Pandas DataFrames so that we get the benefit of Pandas features for manipulating the data.

One problem we have with the emissions data is that it is stored as a 3-dimensional array, a "time" dimension containing the month since
1751, and latitude and logitude dimensions. How do we represent this as a DataFrame, which are inherently 2-dimensional structures?

## Multi-dimensional Data

In the [Introduction to Pandas](https://ornl-training.github.io/python-advanced-pandas) lessons, we saw how to index rows and columns of a Pandas `Series` or `DataFrame`
using labels and integers. Pandas uses an `Index` for this purpose, which is essentially a set of labels that represent the elements of a `Series` or one of the axes 
of the `DataFrame`. An `Index` is inherently one-dimensional, so can only represent one set of labels.

Pandas also provides the ability to index data hierarchically using a `MultiIndex`, which makes it possible to store and manipulate data with an arbitrary number of 
dimensions. You can think of a `MulitIndex` as an array of tuples, where each tuple is unique. A `Series` or `DataFrame` with a hierarchical index can then be 
manipulated as if it was a multi-dimensional array.

As an example, suppose we have an array that represents the amount of money we earned at the end of each week for the first quarter of 2017:

```python
earnings = np.array([370.72, 613.96, 98.17, 616.04, 575.00, 266.93, 243.11, 
                     467.21, 349.54, 698.09, 842.06, 988.02])
```

With the data stored this way, it is not easy to answer a question like "what are the mean weekly earnings each month?".

Let's instead create a list of pairs of month labels and the dates of all the Friday's of the first quarter as follows:

```python
month_labels = ['Jan'] * 4 + ['Feb'] * 4 + ['Mar'] * 4
date_labels = [6, 13, 20, 27, 3, 10, 17, 24, 3, 10, 17, 24]
month_date_pairs = list(zip(month_labels, date_labels))
print(month_date_pairs)
```

This generates the list:

```
[('Jan', 6), ('Jan', 13), ('Jan', 20), ('Jan', 27), ('Feb', 3), ('Feb', 10), ('Feb', 17), ('Feb', 24), ('Mar', 3), ('Mar', 10), ('Mar', 17), ('Mar', 24)]
```

We can now use this list to create a `MultiIndex` and add it to a `Series` representing the earnings data:

```python
import pandas as pd

fridays_index = pd.MultiIndex.from_tuples(month_date_pairs, names=['Month','Date'])
first_quarter_earnings = pd.Series(earnings, index=fridays_index)
print(first_quarter_earnings)
```

The output will be:

```
Month  Date
Jan    6       370.72
       13      613.96
       20       98.17
       27      616.04
Feb    3       575.00
       10      266.93
       17      243.11
       24      467.21
Mar    3       349.54
       10      698.09
       17      842.06
       24      988.02
dtype: float64
```

Notice that Pandas only displays the index labels if they are not repeated. Also, we gave each level of the index a name ("Month" and "Date"). Although
this is not necessary, it allows the index levels to be manipulated using the names.

Now we can easily answer the question "what are the mean weekly earnings each month?" as follows:

```python
for month in ['Jan', 'Feb', 'Mar']:
  print('Earnings in ' + month + ' were', first_quarter_earnings[month].mean())
```

Which results in:

```
Earnings in Jan were 424.7225
Earnings in Feb were 388.0625
Earnings in Mar were 719.4275
```

> ## Challenge
>
> Answer the following questions:
>
> 1. What are the total earnings for the first quarter?
> 2. What are the total earnings each month? 
> 3. Which month was most profitable?
> 4. Which month had the most variance in weekly earnings?
> 5. Generate a plot of the first quarter earnings using the plot method associated with `Series`.
{: .challenge}

## Generating a MultiIndex

We saw that it is possible to create a `MultiIndex` by providing a list of all the combinations of labels that we want to use. This can become
very tedious when there are large numbers of labels at each level, or multiple levels of hierarchy. One possible way to overcome this is to
use a package such as [`itertools`](https://docs.python.org/3/library/itertools.html), which provides methods for generating combinations of elements from lists.

Another approach is to use the `MultiIndex.from_product()` method which will generate an index by combining every element from a list of
two or more iterables. For example, suppose we wanted to create a two-level index where the first labels are taken from a NumPy array. 
We could do this in one statement as follows:

```python
latitude = np.array([-86.5, -85.5, -84.5, -83.5, -82.5, -81.5])
longitude = np.array([-105.5, -104.5, -103.5, -102.5, -101.5, -100.5])
multi_index = pd.MultiIndex.from_product([latitude, longitude], names=['Latitude', 'Longitude'])
print(multi_index)
```

This would generate the required `MultiIndex` and the output:

```
MultiIndex(levels=[[-86.5, -85.5, -84.5, -83.5, -82.5, -81.5], [-105.5, -104.5, -103.5, -102.5, -101.5, -100.5]],
           labels=[[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5], [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]],
           names=['Latitude', 'Longitude'])
```

> ## Challenge
>
> In the case of our CIMP5 global emissions data, we would like to create a `MultiIndex` that has three levels, one for each dimension of the array, namely
> "time_counter", "latitude", and "longitude". We can obtain the values for the labels from the corresponding variables in the dataset.
>
> Modify the `load_data.py` script as follows:
> 
> 1. Obtain NumPy arrays for the "Longitude", "Latitiude", "time_counter", "FF", and "AREA" netCDF variables and assign them to Python variables.
> 2. Generate a `MultiIndex` from the product of the "time_counter", "Latitude", and "Longitude" variables. Use 'Month', 'Latitude', and 'Longitude' as the level names.
{: .challenge}

## Wrapping the Data

Although a hierarchical index allows us to access data in a `Series` or `DataFrame` as if it was multi-dimensional, we still have to create them using 
data that is one-dimensional. Suppose that the quarterly earnings data was actually in a 2-dimensional array, rather than a one-dimensional array and we
try to create the `Series` the same way as before:

```python
earnings = np.array([[370.72, 613.96, 98.17, 616.04], [575.00, 266.93, 243.11, 
                     467.21], [349.54, 698.09, 842.06, 988.02]])
fridays_index = pd.MultiIndex.from_tuples(month_date_pairs, names=['Month','Date'])
first_quarter_earnings = pd.Series(earnings, index=fridays_index)
print(first_quarter_earnings)
```

If we run this, we get the result:

```
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
<ipython-input-81-916f673e41ea> in <module>()
      1 fridays_index = pd.MultiIndex.from_tuples(month_date_pairs, names=['Month','Date'])
----> 2 first_quarter_earnings = pd.Series(earnings, index=fridays_index)

anaconda3/lib/python3.6/site-packages/pandas/core/series.py in __init__(self, data, index, dtype, name, copy, fastpath)
    246             else:
    247                 data = _sanitize_array(data, index, dtype, copy,
--> 248                                        raise_cast_failure=True)
    249 
    250                 data = SingleBlockManager(data, index, fastpath=True)

anaconda3/lib/python3.6/site-packages/pandas/core/series.py in _sanitize_array(data, index, dtype, copy, raise_cast_failure)
   3025     elif subarr.ndim > 1:
   3026         if isinstance(data, np.ndarray):
-> 3027             raise Exception('Data must be 1-dimensional')
   3028         else:
   3029             subarr = _asarray_tuplesafe(data, dtype=dtype)

Exception: Data must be 1-dimensional
```

This is Pandas telling us that the data must be 1-dimensional in order to create the `Series`. So 
we need to "flatten" the data before it could be wrapped with a `Series`. Remember, we want to use a `MultiIndex` to access
the data as if it was multi-dimensional, not the indexes of a multi-dimensional array.

Fortunately, NumPy provides a variety of methods for reshaping arrays. One of these is the 
[`reshape()`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html) method, 
which takes the new shape as an argument and returns an array with the new shape. As long as
the new shape has the same total number of elements, the result will just be a new "view" of
the original array, not a copy. The examples below show how the array shape can be modified:

```python
print(earnings.reshape((2, 2, 3))) # reshaped to 3-dimensional
print(earnings.reshape((4, 3))) # same shape as the original
print(earnings.reshape((12,))) # reshape to 1-dimensional
print(earnings.reshape(-1)) # one dimension can be -1 to specify "whatever is left"
```

The output generated would be:

```
[[[ 370.72  613.96   98.17]
  [ 616.04  575.    266.93]]
 [[ 243.11  467.21  349.54]
  [ 698.09  842.06  988.02]]]
  
[[ 370.72  613.96   98.17]
 [ 616.04  575.    266.93]
 [ 243.11  467.21  349.54]
 [ 698.09  842.06  988.02]]
 
[ 370.72  613.96   98.17  616.04  575.    266.93  243.11  467.21  349.54
  698.09  842.06  988.02]
  
[ 370.72  613.96   98.17  616.04  575.    266.93  243.11  467.21  349.54
  698.09  842.06  988.02]
```

Notice that  the last two produce the same result, a one-dimensional array. The `reshape` method allows one of the
dimensions to be `-1`, which indicates that it should  be inferred from the length of the array and remaining
dimensions.

So now we are able to create the `Series` from the 2-dimensional array as follows:

```python
first_quarter_earnings = pd.Series(earnings.reshape(-1), index=fridays_index)
print(first_quarter_earnings)
```

> ## Challenge
>
> Returning to our CIMP5 global emissions data, it should now be possible to create a `Series` for the 'FF' variable. Modify the `load_data.py` 
> script so that it creates a `Series` called `ff_pd` using the `MultiIndex` you created previously.
{: .challenge} 
