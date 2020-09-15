'''
Creates tifs of TIN anomaly from average
Created by: Marketa Podebradska
Date: 9/15/2020
'''

import gdal, ogr, os, osr
import numpy as np

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

years = range(2000, 2002)

all_TIN = []

for year in years:
    TIN_raster = gdal.Open(f'../output/TIN_{year}.tif')
    TIN_array = TIN_raster.ReadAsArray()
    all_TIN.append(TIN_array)

numpy_all_TIN = np.array(all_TIN)

median_TIN = np.median(numpy_all_TIN, axis = 0)

for year in years:
    print(f'working on {year}')
    TIN_raster_year = gdal.Open(f'../output/TIN_{year}.tif')
    TIN_array_year = TIN_raster_year.ReadAsArray()
    anomaly_TIN = TIN_array_year-median_TIN
    newRasterfn = f'../output/TIN_anomaly_{year}.tif'
    transform = TIN_raster_year.GetGeoTransform()
    x = transform[0]
    y = transform[3]
    rasterOrigin = (x, y)
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,anomaly_TIN)
