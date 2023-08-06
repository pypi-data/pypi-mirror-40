import click, shapefile, json, sqlite3, csv, pygeoj, pytest, math, os
from osgeo import gdal
import pandas as pd
import numpy as np
import xarray as xr
import os

import extractTool
import getShapefileInfo, getGeoTiffInfo, getCSVInfo, getGeoJsonInfo, getNetCDFInfo, getGeoPackageInfo, getIsoInfo, openFolder

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print(__location__+'/testdata/')

print("Ausgabe Shapefile: ")
a = getShapefileInfo.getShapefilebbx(__location__+'/testdata/Abgrabungen_Kreis_Kleve_shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'bbox', 'single')
"""erwartetes Ergebnis: [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]"""

#print("Ausgabe CSV: ")
#b = getCSVInfo.getCSVbbx(__location__+'/testdata/Behindertenparkplaetze_Duesseldorf.csv', 'bbox', 'single')
#"""erwartetes Ergebnis: No fitting header for latitudes or longitudes"""

# print("Ausgabe GeoPackage: ")
# c = getGeoPackageInfo.getGeopackagebbx(__location__+'/testdata/Geopackage_Queensland_geopackage/census2016_cca_qld_short.gpkg', 'bbox', 'single')
# """erwartetes Ergebnis: [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]"""

#print("Ausgabe GeoJson: ")
#d = getGeoJsonInfo.getGeoJsonbbx(__location__+'/testdata/schutzhuetten_aachen.json', 'bbox', 'single')
#"""erwartetes Ergebnis: [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667]"""

print("Ausgabe GeoTiff: ")
e = getGeoTiffInfo.getGeoTiffbbx(__location__+'/testdata/MittlWindgeschw-100m_GeoTIFF/wf_100m_klas.tif', 'bbox', 'single')
"""erwartetes Ergebnis: [5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733]"""

# print("Ausgabe Iso: ")
# f = getIsoInfo.getIsobbx(__location__+'/testdata/', 'bbx', 'single')
# """erwartetes Ergebnis: No fitting header for latitudes or longitudes"""

# print("Ausgabe NetCDF: ")
# g = getNetCDFInfo.getNetCDFbbx(__location__+'/testdata/tos_01_2001-2002.nc', 'bbox', 'single')
# """erwartetes Ergebnis: [-79.5, 1.0, 89.5, 359.0]"""

def test_answerA():
    assert getShapefileInfo.getShapefilebbx(__location__+'/testdata/Abgrabungen_Kreis_Kleve_shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'bbox', 'single') == a

def test_answerB():    
    assert getCSVInfo.getCSVbbx(__location__+'/testdata/Behindertenparkplaetze_Duesseldorf.csv', 'bbox', 'single') == b

# def test_answerC():    
#     assert getGeoPackageInfo.getGeopackagebbx(__location__+'/testdata/Geopackage_Queensland_geopackage/census2016_cca_qld_short.gpkg', 'bbox', 'single') == c

def test_answerD():    
    assert getGeoJsonInfo.getGeoJsonbbx(__location__+'/testdata/schutzhuetten_aachen.json', 'bbox', 'single') == d

def test_answerE():    
    assert getGeoTiffInfo.getGeoTiffbbx(__location__+'/testdata/MittlWindgeschw-100m_GeoTIFF/wf_100m_klas.tif', 'bbox', 'single') == e

# def test_answerF():    
#     assert getIsoInfo.getIsobbx(__location__+'/testdata/', 'bbx', 'single') == f

# def test_answerG():    
#     assert getNetCDFInfo.getNetCDFbbx(__location__+'/testdata/tos_01_2001-2002.nc', 'bbox', 'single') == g