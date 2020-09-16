#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Marketa Poderadska
Date: 9/16/2020

Saves rasters of annual NDVI max.

"""

import gdal, ogr, os, osr
import numpy as np

years = range(2000, 2019)
weeks = range(1, 53)

def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):

    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

yearly_max = []
for year in years:
    weekly_NDVI = []
    for week in weeks:
        week_str = '%02d' % int(week)
        NDVI_raster = gdal.Open(f'../input/eMODIS{year}{week_str}.tif')
        NDVI_array = NDVI_raster.ReadAsArray()
        weekly_NDVI.append(NDVI_array)
    annual_max = np.max(weekly_NDVI, axis = 0)
    transform = NDVI_raster.GetGeoTransform()
    x = transform[0]
    y = transform[3]
    rasterOrigin = (x, y)
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    array2raster(f'..output/max_NDVI_{year}.tif', rasterOrigin, pixelWidth, pixelHeight, annual_max)

