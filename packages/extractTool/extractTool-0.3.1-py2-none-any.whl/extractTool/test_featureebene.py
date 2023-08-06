import click, shapefile, json, sqlite3, csv, pygeoj
from osgeo import gdal
import pandas as pd
import numpy as np
import xarray as xr
import os

import extractTool
import getShapefileInfo, getGeoTiffInfo, getCSVInfo, getGeoJsonInfo, getNetCDFInfo, getGeoPackageInfo, getIsoInfo, openFolder

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print(__location__+'/testdata/')

def test_featureShape():
    assert getShapefileInfo.getShapefilebbx(__location__+'/testdata/Abgrabungen_Kreis_Kleve_shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'feature', 'single', False) == 0

def test_featureCSV():    
    assert getCSVInfo.getCSVbbx(__location__+'/testdata/Behindertenparkplaetze_Duesseldorf.csv', 'feature', 'single') == "nich fertig"

def test_featureGeoPackage():    
    assert getGeoPackageInfo.getGeopackagebbx(__location__+'/testdata/Geopackage_Queensland_geopackage/census2016_cca_qld_short.gpkg', 'feature', 'single') == [(96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169,-43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (112.921, -43.7405), (96.8169, -43.7405),(96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405), (96.8169, -43.7405)]

def test_featureGeoJson():    
    assert getGeoJsonInfo.getGeoJsonbbx(__location__+'/testdata/schutzhuetten_aachen.json', 'feature', 'single') == [[296952.85186914, 5624067.07285793], [295913.66024875, 5624880.6537705], [295319.12138993, 5623861.12308584], [301987.96613832, 5618723.70111273], [302067.71444814, 5619693.82603416], [295295.33077593, 5624535.3383897], [302039.51397745, 5626416.78906231], [302531.3161606, 5626839.79436834], [301151.43818774, 5631223.82854667], [300110.34453109, 5618144.09259115], [292537.45935834, 5623556.4350225], [293218.82603216, 5624555.09775785], [293940.83749215, 5624058.1092388], [292063.81225905, 5626164.30672035]]

def test_featureGeoTiff():    
    assert getGeoTiffInfo.getGeoTiffbbx(__location__+'/testdata/MittlWindgeschw-100m_GeoTIFF/wf_100m_klas.tif', 'feature', 'single') == None

def test_featureIso():    
     assert getIsoInfo.getIsobbx(__location__+'/testdata/3D_LoD1_33390_5664.gml', 'feature', 'single') == f

def test_featureNetCDF():    
    assert getNetCDFInfo.getNetCDFbbx(__location__+'/testdata/ECMWF_ERA-40_subset.nc', 'feature', 'single') == None

#--detail=bboxSingle no time value
def test_bboxSingleShapefile():
     assert getShapefileInfo.getShapefilebbx(__location__+'/testdata/Abgrabungen_Kreis_Kleve_shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'bbox', 'single', False)

def test_bboxSingleGeoJson():

def test_bboxSingleNetCDF():

def test_bboxSingleCSV():

def test_bboxSingle0Geopackage():

def test_bboxSingleGeoTiff():

def test_bboxSingleIso():


#--detail=bboxWhole

def test_bboxWholeShapefile():

def test_bboxWholeGeoJson():

def test_bboxWholeNetCDF():

def test_bboxWholeCSV():

def test_bboxWhole0Geopackage():

def test_bboxWholeGeoTiff():

def test_bboxWholeIso():