---
layout: page
title: Setup 
permalink: /setup/
---

> ## Data
{: .prereq}

> ## Software
{: .prereq}
For this workshop we use Python version 3.x.

## Required Python Packages for this workshop

* [Pandas](http://pandas.pydata.org/)
* [Jupyter notebook](http://jupyter.org/)
* [Numpy](http://www.numpy.org/)
* [Matplotlib](http://matplotlib.org/)
* [ggplot](http://ggplot.yhathq.com/)

## Install the workshop packages

For installing these packages we will use Anaconda. 
Anaconda is a Python distribution aimed at data science.

### Anaconda installation

Download and install [Anaconda](https://www.continuum.io/downloads).
Remember to download and install the installer for <b>Python 3.x</b> for your
platform.

You can download either the graphical or command-line installer. If you
download the command line installer, you will need to run the installer
using the `sh` command. For example, if you downloaded 
`Anaconda3-4.4.0-MacOSX-x86_64.sh`, you would need to run the command:

```
sh Anaconda3-4.4.0-MacOSX-x86_64.sh
```

It is usually necessary to restart your shell once you've installed Anaconda.

### ggplot installation

Run the command:

```
conda install ggplot
```

In some cases, installing `ggplot` from conda may fail with an error like:

```
UnsatisfiableError:The following specifications were found to be in conflict:
      - ggplot -> python3.4*
      - python 3.6*
```

In that case, try installing `ggplot` with Anaconda `pip` by running this command in your terminal:

```
pip install -U ggplot
```

## Launch a Jupyter notebook

After installing either Anaconda or Miniconda and the workshop packages,
launch a Jupyter notebook by typing this command from the terminal:

```
jupyter notebook
```

The notebook should open automatically in your browser. If it does not or you
wish to use a different browser, open this link: <http://localhost:8888>.

---

## Overview of the Jupyter notebook (Optional)

![Example Jupyter Notebook](../fig/00_0_jupyter_notebook_example.jpg)  
*Screenshot of a [Jupyter Notebook on quantum mechanics](https://github.com/jrjohansson/qutip-lectures) by Robert Johansson*

### How the Jupyter notebook works

After typing the command `jupyter notebook`, the following happens:

* A Jupyter Notebook server is automatically created on your local machine.
* The Jupyter Notebook server runs locally on your machine only and does not
  use an internet connection.
* The Jupyter Notebook server opens the Jupyter notebook client, also known
  as the notebook user interface, in your default web browser.

  ![Jupyter notebook file browser](../fig/00_1_jupyter_file_browser.png)  
  *The Jupyter notebook file browser*

* To create a new Python notebook select the "New" dropdown on the upper
  right of the screen.

  ![Jupyter notebook file browser](../fig/00_2_jupyter_new_notebook.png)  
  *The Jupyter notebook file browser*

* When you can create a new notebook and type code into the browser, the web
  browser and the Jupyter notebook server communicate with each other.

  ![new Jupyter notebook](../fig/00_3_jupyter_blank_notebook.png)  
  *A new, blank Jupyter notebook*

* Under the "help" menu, take a quick interactive tour of how to
  use the notebook. Help on Jupyter and key workshop packages is
  available here too.

  ![Jupyter tour and help](../fig/00_4_jupyter_tour_help.png)  
  *User interface tour and Help*

* The Jupyter Notebook server does the work and calculations, and the web
  browser renders the notebook.
* The web browser then displays the updated notebook to you.

* For example, click in the first cell and type some Python code.

  ![Code cell](../fig/00_5_jupyter_code_before.png)  
  *A Code cell*

* This is a **Code** cell (see the cell type dropdown with the word **Code**).
  To run the cell, type Shift-Enter.

  ![Code cell and its output](../fig/00_6_jupyter_code_after.png)  
  *A Code cell and its output*

* Let's look at a **Markdown** cell. Markdown is a text manipulation
  language that is readable yet offers additional formatting. Don't forget
  to select **Markdown** from the cell type dropdown. Click in the cell and
  enter the markdown text.

  ![markdown input cell](../fig/00_7_jupyter_markdown_before.png)  
  *A markdown input cell*

* To run the cell, type Shift-Enter.

  ![rendered markdown cell](../fig/00_8_jupyter_markdown_after.png)  
  *A rendered markdown cell*


This workflow has several advantages:

- You can easily type, edit, and copy and paste blocks of code.
- Tab completion allows you to easily access the names of things you are using
  and learn more about them.
- It allows you to annotate your code with links, different sized text,
  bullets, etc. to make information more accessible to you and your
  collaborators.
- It allows you to display figures next to the code that produces them
  to tell a complete story of the analysis.

### How the notebook is stored

* The notebook file is stored in a format called JSON and has the suffix
  `.ipynb`.
* Just like HTML for a webpage, what's saved in a notebook file looks
  different from what you see in your browser.
* But this format allows Jupyter to mix software (in several languages) with
  documentation and graphics, all in one file.

### Notebook modes: Control and Edit

The notebook has two modes of operation: Control and Edit. Control mode lets
you edit notebook level features; while, Edit mode lets you change the
contents of a notebook cell. Remember a notebook is made up of a number of
cells which can contain code, markdown, html, visualizations, and more.

### Help and more information

Use the **Help** menu and its options when needed.
