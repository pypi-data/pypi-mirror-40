import click, shapefile, json, sqlite3, csv, pygeoj
from osgeo import gdal
import pandas as pd
import numpy as np
import xarray as xr
import os

import getTimeextend

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print(__location__+'/testdata/')

def test_timeShape():
    assert getTimeextend.getShapefiletime(__location__+'/testdata/Abgrabungen_Kreis_Kleve_shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'time') == None

def test_timeCSV():    
    assert getTimeextend.getCSVtime(__location__+'/testdata/Behindertenparkplaetze_Duesseldorf.csv', 'time') == None

def test_timeGeoPackage():    
    assert getTimeextend.getGeopackagetime(__location__+'/testdata/Geopackage_Queensland_geopackage/census2016_cca_qld_short.gpkg', 'time') == None

def test_timeGeoJson():    
    assert getTimeextend.getGeoJsontime(__location__+'/testdata/muenster_ring_zeit.geojson', 'time') == "2018-11-14"

def test_timeGeoTiff():    
    assert getTimeextend.getGeoTifftime(__location__+'/testdata/MittlWindgeschw-100m_GeoTIFF/wf_100m_klas.tif', 'time') == None

def test_timeIso():    
     assert getTimeextend.getIsoTime(__location__+'/testdata/clc_1000_PT.gml', 'time') == "2012-09-09"

def test_timeNetCDF():    
    assert getTimeextend.getNetCDFtime(__location__+'/testdata/ECMWF_ERA-40_subset.nc', 'time') == "2002-07-01T12:00:00.000000000" "2002-07-31T18:00:00.000000000"
