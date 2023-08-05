## nonlineartemppy

[![Travis_CI_Badge](https://travis-ci.org/johnwoodill/nonlineartemppy.svg?branch=master)](https://travis-ci.org/johnwoodill/nonlineartemppy#)
![]()
![](https://img.shields.io/python/v3.6.png?color=blue)
![](https://img.shields.io/license/MIT.png?color=blue)


Overview
--------
`nonlineartemppy` calculates nonlinear temperature distributions using an integrated sine technique. Degree days define time above a specified temperature threshold (e.g. degree days above 30C) and time in each degree define time within a specified temperature threshold (e.g. time in 30C).

-   `degree_days()`: calculates degree days within a specified thresholds
-   `degree_time()`: calculates time in each degree at one degree intervals within a specified thresholds.

Installation
------------

``` python
# Install through pip
pip install nonlineartemppy
```

Usage
-----

``` python
import numpy as np
import pandas as pd
import nonlineartemppy.calculations as nltemp
import io
import pkgutil

# Import Napa data set
data = pkgutil.get_data('nonlineartemppy', 'data/napa.csv')
napa = pd.read_csv(io.BytesIO(data), encoding='utf8', sep=",", dtype={"switch": np.int8})
napa = pd.DataFrame(napa)

# Degree Days
dd_napa = nltemp.degree_days(napa, range(0,5))

dd_napa.head()

         date    year  month  day  fips       county state   lat   long  \
0  1899-12-15  1899.0     12   15  6055  Napa County    CA  38.5 -122.5   
1  1899-12-16  1899.0     12   16  6055  Napa County    CA  38.5 -122.5   
2  1899-12-17  1899.0     12   17  6055  Napa County    CA  38.5 -122.5   
3  1899-12-18  1899.0     12   18  6055  Napa County    CA  38.5 -122.5   
4  1899-12-19  1899.0     12   19  6055  Napa County    CA  38.5 -122.5   

      tmax    tmin     tavg   dday0C   dday1C   dday2C   dday3C   dday4C  
0  12.5000  4.1100  8.30500  8.30500  7.30500  6.30500  5.30500  4.30500  
1  12.5445  4.2894  8.41695  8.41695  7.41695  6.41695  5.41695  4.41695  
2  12.5878  4.4574  8.52260  8.52260  7.52260  6.52260  5.52260  4.52260  
3  12.6298  4.6144  8.62210  8.62210  7.62210  6.62210  5.62210  4.62210  
4  12.6706  4.7604  8.71550  8.71550  7.71550  6.71550  5.71550  4.71550  


# Time in each degree
td_napa = nltemp.degree_time(napa, range(0,5))
td_napa.head()

         date    year  month  day  fips       county state   lat   long  \
0  1899-12-15  1899.0     12   15  6055  Napa County    CA  38.5 -122.5   
1  1899-12-16  1899.0     12   16  6055  Napa County    CA  38.5 -122.5   
2  1899-12-17  1899.0     12   17  6055  Napa County    CA  38.5 -122.5   
3  1899-12-18  1899.0     12   18  6055  Napa County    CA  38.5 -122.5   
4  1899-12-19  1899.0     12   19  6055  Napa County    CA  38.5 -122.5   

      tmax    tmin  tdegree0C  tdegree1C  tdegree2C  tdegree3C  tdegree4C  
0  12.5000  4.1100        0.0        0.0        0.0        0.0    0.02960  
1  12.5445  4.2894        0.0        0.0        0.0        0.0    0.01624  
2  12.5878  4.4574        0.0        0.0        0.0        0.0    0.00334  
3  12.6298  4.6144        0.0        0.0        0.0        0.0    0.00000  
4  12.6706  4.7604        0.0        0.0        0.0        0.0    0.00000 

```