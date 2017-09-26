---
layout: lesson
root: .

maintainers:
  - Greg Watson
---

**Lesson Maintainers:** {{ page.maintainers | join: ', ' }}

This is an advanced Pandas lesson designed for participants with basic Python programming experience and who have completed the Introduction to Pandas lesson. These 
lessons can be taught in a day (~ 6 hours). 

## Background

You are working on a project to determine if the Paris Accord greenhouse gas reduction targets could be met by just the world's largest cities, because these are the areas with
the tax-base and political will to be able to implement many of the carbon changes that would be necessary.

One possible way to do this would be to model the global contribution of expected emissions, and compare this to the emissions that would be produced if the largest 50 cities reduced their emissions by a specified amount, X. Creating a model like this is difficult, so a simpler approach might be to see if the data is already available, calculate 
the level of greenhouse gas reductions we could get from the cities, and then compare it naively to the IPCC AR5 warming/ppm data. Even if this approach is not completely 
accurate, it might provide a ball park figure that indicates if the approach would be worth continued exploration.

We'll start with the following two data sets:

- The CMIP5 global emissions dataset which provides gridded emissions for all latitute/logitudes from 1751 - 2007. This data set is from historical runs of the 
Coupled Model Intercomparison Project, Phase 5 (CMIP5) Earth Systems Models (ESMs). The historical fossil fuel CO2 emissions account for solid fuels, liquid fuels, gaseous fuels, gas flaring, and cement production. The data are monthly gridded emissions (gC/m-2/s).
- The latitude/logitude of the 50 largest cities and their associated greenhouse gas emissions. This data was compiled by Melissa Allen (thanks Melissa!)


> ## Getting Started
>
> Data Carpentry's teaching is hands-on, so participants are encouraged to use
> their own computers to insure the proper setup of tools for an efficient 
> workflow. <br>**These lessons assume no prior knowledge of the skills or tools.**
>
> To get started, follow the directions in the "[Setup](setup/)" tab to 
> download data to your computer and follow any installation instructions.
{: .prereq}

> ## Prerequisites
>
> This lesson assumes basic knowledge of Python and completion of the Introduction to Pandas lessons. The following are good measures of the prerequisite skills necessary for this lesson.:
> - Software Carpentry [Programming with Python](http://swcarpentry.github.io/python-novice-inflammation/) 
> - [Plotting and Programming in Python](https://ornl-training.github.io/python-novice-gapminder/)
> - [Introduction to Pandas](https://ornl-training.github.io/python-pandas)
{: .prereq}

> ## For Instructors
> If you are teaching this lesson in a workshop, please see the 
> [Instructor notes](guide/).
{: .prereq}
