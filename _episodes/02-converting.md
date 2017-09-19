---
title: Converting to Pandas
teaching: 30
exercises: 30
questions:
    - " How can I use NetCDF in Pandas?"
    - " How should I structure my DataFrame?"
objectives:
---

# Using NetCDF with Pandas

In the last module, we wrote a simple Python program to load the NetCDF data and print some useful information about it. An example script is
available [here](../code/load_data_01.py). We also saw that the data is accessible as NumPy arrays. However, it would be much more useful
if we could store the data as Pandas DataFrames so that we get the benefit of Pandas features for manipulating the data.

One problem we have with the emissions data is that it is stored as a 3-dimensional array, a "time" dimension containing the month since
1751, and latitude and logitude dimensions. How do we represent this as a DataFrame, which are inherently 2-dimensional structures?

## MultiIndex

In the [Introduction to Pandas](https://ornl-training.github.io/python-advanced-pandas) lessons, we saw how to index rows and columns of a Pandas `Series` or `DataFrame`
using labels and integers. Pandas uses an `Index` for this purpose, which is essentially a set of labels that represent the elements of a `Series` or one of the axes 
of the `DataFrame`. An `Index` is inherently one-dimensional, so can only represent one set of labels.

Pandas also provides the ability to index data hierarchically using a `MultiIndex`, which makes it possible to store and manipulate data with an arbitrary number of 
dimensions. You can think of a `MulitIndex` as an array of tuples, where each tuple is unique. A `Series` or `DataFrame` with a hierarchical index can then be 
manipulated as if it was a multi-dimensional array.

As an example, suppose we have an array that represents the amount of money we earned at the end of each week for the first quarter of 2017:

```python
earnings = np.array([370.72, 613.96, 98.17, 616.04, 575.00, 266.93, 243.11, 
                     467.21, 349.54, 698.09, 842.06, 988.02, 465.03])
```

With the data stored this way, it is not easy to answer a question like "what are the mean weekly earnings each month?".

Let's instead create a list ofn pairs of month labels and the dates of all the Friday's of the first quarter as follows:

```python
month_labels = ['Jan'] * 4, ['Feb'] * 4, ['Mar'] * 5
date_labels = [6, 13, 20, 27, 3, 10, 17, 24, 3, 10, 17, 24, 31]
month_date_pairs = list(zip(month_labels, date_labels))
print(month_date_pairs)
```

This generates the list:

```
[('Jan', 6), ('Jan', 13), ('Jan', 20), ('Jan', 27), ('Feb', 3), ('Feb', 10), ('Feb', 17), ('Feb', 24), ('Mar', 3), ('Mar', 10), ('Mar', 17), ('Mar', 24), ('Mar', 31)]
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
       31      465.03
dtype: float64
```

Notice that Pandas only displays the index labels if they are not repeated. Also, we gave each level of the index a name ("Month" and "Date). Although
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
Earnings in Mar were 668.548
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

