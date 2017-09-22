---
title: Data Analysis with the Class
teaching: 30
exercises: 30
questions:
    - " How can I use classes to make code reusable?"
objectives:
---

At the end of the last lesson our program provided a class for managing the emissions data. 
An example of what this program might look like is available [here](../code/load_data_04.py). 

The purpose of creating the `HistoricalCO2Emissions` class was so that we could re-use it for
our analysis task. So let's see how to do that now.

## Some Things About Importing You Didn't Know

Previously, we've seen that to include new functionality in a Python program, you need to *import* it.
There are a couple of different import statements: `import ... as` and `from ... import` but they
essentially do the same thing. So what is importing actually? And while we're at it, what is the difference between 
a "package" and a "module" anyway?

### Modules

In Python, a *module* is the name given to a series of executable statements in a single file. Usually
this file ends with `.py`, but that is not always necessary. 

When you import a module, it's almost exactly the same as if you entered the statements manually, or ran
the script using `python module.py`. The important difference is that for a statement like `import module`
or `import module as foo` it's as if the module name (or `foo.`) is added as a prefix to all the variables, functions,
classes, etc. imported from the module. In other words, the module has a *namespace* which is either the name 
of the module, or what it is imported as. This allows modules to use name without worrying about them clashing with
names used in the importing module. The exception to this is when you use the `from ... import ...``` variant.
In this case the names from the module are imported directly into the module, so they don't have to be prefixed
with anything. Of course in this case, you may get clashes between the names used in the current module and
those from the imported module.

So if module `a.py` contained:

```python
var = 4
```

then it could be used from module `b.py` as:

```python
import a
print(a.var) # prints 4
```

Modules are also only ever imported *once*. So multiple statements importing the same module will not result
in the module be run multiple times, although you can provide multiple namespaces for the same names
this way.

> ## Challenge
>
> Suppose module `a.py` contained the following:
>
> ```python
> var = [1,2]
> ```
>
> What would be the output from the running
> this script:
>
> ```python
> import a
> import a as c
>
> print(a.var)
> print(c.var)
> c.var.append(3)
> print(a.var)
> ```
> 
> > ## Solution
> >
> > ```
> > [1,2]
> > [1,2]
> > [1,2,3]
> > ```
> {: .solution}
{: .challenge}

Another important distinction between importing a module and running it as a script (using the
`python module.py` command is the value
of the global variable `__name__`. When you import a module, this variable is set to the name
of the module, however, when you run the module as a script this variable is set to `__main__`.
This enables code to be placed in the module that will only be executed when it is run as
as script, and why you see the following statement so often.

```
if __name__ == '__main__':
    ...
```

Any code that is placed inside the body of the `if` statement will only be executed when the
module is run, *not* when it is imported. This allows modules to be used both as libraries and
as programs, and also provides a great way of including test code with the module.

### Packages

Where does a package come into all this then? A package is really just a way of grouping modules
together in a more logical way, like putting all the modules related to Pandas in one place, and
all the modules relating to NetCDF4 in another place. Packages do also introduce a hierarchy, so
module `C` that is inside a directory `B` that is inside package `A` can be imported using the
statement `import A.B.C`.

A *package* is a directory tree with some Python files (modules) in it. If you want to tell Python that a 
certain directory is a package then just create a file called `__init__.py` and put it in the directory.
A package can contain other packages but to be useful, it must contain modules somewhere in it's hierarchy.

### Module Search Path

One final thing, how does Python know where to find modules like `numpy` or `pandas`? If the name is not
a built-in module, then it will search for the module in a list of directories given by the variable `sys.path`.

This variable is initialized from these locations:

- the directory containing the input script (or the current directory).
- the PYTHONPATH environment variable
- an installation-dependent default.

Since this list contains the current directory, it is possible to import modules in the same directory
as the program being run without needing to specify anything additional.

See the Python [Modules](https://docs.python.org/3.6/tutorial/modules.html) documentation for more details
on modules, packages, and importing.

## Finding the Cities

The next step in our analysis task is to determine the CO2 emissions from the top emitting cities. Fortunately
we already have a dataset that lists these 
