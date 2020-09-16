#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Marketa Poderadska
Date: 9/16/2020

Creates a multi-dimensional array of annual max NDVI values.

"""

import gdal, ogr, os, osr
import numpy as np

years = range(2000, 2019)
weeks = range(1, 53)

yearly_max = []
for year in years:
    weekly_NDVI = []
    for week in weeks:
        week_str = '%02d' % int(week)
        NDVI_raster = gdal.Open(f'../input/eMODIS{year}{week_str}.tif')
        NDVI_array = NDVI_raster.ReadAsArray()
        weekly_NDVI.append(NDVI_array)
    annual_max = np.max(weekly_NDVI, axis = 0)
    yearly_max.append(annual_max)

print(yearly_max)

