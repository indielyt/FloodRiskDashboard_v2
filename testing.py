# test of methods to access geospatial data
# 1. using .shp file and geopandas
# 2. using .json and python parsing
# 3. using .json in a postgres database and sqlalchemy

'''
~~~~~~~~~~~~~~~~
~~ IMPORTS ~~
~~~~~~~~~~~~~~~~
'''
import geopandas as gpd
import time
import json
from osgeo import ogr




'''
~~~~~~~~~~~~~~~~
~~ DATA ~~
~~~~~~~~~~~~~~~~
'''

shpfile = r'shp/S_Structure.shp'
# jsonfile = 'jsons\S_Structure.json'



'''
~~~~~~~~~~~~~~~~
~~ GDAL ~~
~~~~~~~~~~~~~~~~
'''
# https://stackoverflow.com/questions/51009185/convert-a-shapefile-of-polygons-to-numpy-array
# http://www2.geog.ucl.ac.uk/~plewis/geogg122_current/_build/html/ChapterX_GDAL/OGR_Python.html

if False:
    dataSource = ogr.Open(shpfile)
    daLayer = dataSource.GetLayer(0)
    layerDefinition = daLayer.GetLayerDefn()

    for i in range(layerDefinition.GetFieldCount()):
        print (layerDefinition.GetFieldDefn(i).GetName())

    t_a = time.time()
    import gdal
    t_b = time.time()

    t0 = time.time()

    source_ds = ogr.Open(shpfile)
    source_layer = source_ds.GetLayer()
    pixelWidth = pixelHeight = 0.001 
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    cols = int((x_max - x_min) / pixelHeight)
    rows = int((y_max - y_min) / pixelWidth)
    target_ds = gdal.GetDriverByName('GTiff').Create('temp.tif', cols, rows, 1, gdal.GDT_Byte) 
    target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_min, 0, pixelHeight))
    band = target_ds.GetRasterBand(1)
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], source_layer, options = ["ATTRIBUTE=R_SCORE"])
    target_ds = None #this is the line that makes the difference
    np_array = gdal.Open('temp.tif').ReadAsArray()

    t1 = time.time()

    print('Import Time: {:.2f} seconds'.format(round(t_b - t_a, 2)))
    print('GDAL Time: {:.2f} seconds'.format(round(t1 - t0, 2)))

    print(type(np_array))
    print(len(np_array))
    print(np_array)





'''
~~~~~~~~~~~~~~~~
~~ Geopandas 1 ~~
~~~~~~~~~~~~~~~~
'''


def generate_from_shp(shpfile):
    """
    function to time shp to geopandas dataframe to json workflow
    """

    print('starting')

    t_a = time.time()
    import geopandas as gpd
    import pandas as pd 
    t_b = time.time()

    t0 = time.time()
    shp_df = gpd.read_file(shpfile)
    t1 = time.time()

    t_c = time.time()
    shp_dff = shp_df.copy(deep=True)
    t_d = time.time()
    
    t2 = time.time()
    dataset_10 = shp_df[shp_df['R_SCORE'].between(10,20,inclusive=False)]
    dataset_20 = shp_df[shp_df['R_SCORE'].between(20,30,inclusive=False)]
    dataset_30 = shp_df[shp_df['R_SCORE'].between(30,40,inclusive=False)]
    dataset_40 = shp_df[shp_df['R_SCORE'].between(40,30,inclusive=False)]
    dataset_50 = shp_df[shp_df['R_SCORE'].between(40,50,inclusive=False)]
    dataset_60 = shp_df[shp_df['R_SCORE'].between(50,60,inclusive=False)]
    dataset_70 = shp_df[shp_df['R_SCORE'].between(60,70,inclusive=False)]
    dataset_80 = shp_df[shp_df['R_SCORE'].between(80,90,inclusive=False)]
    dataset_90 = shp_df[shp_df['R_SCORE'].between(80,90,inclusive=False)]
    t3 = time.time()

    t4 = time.time()
    shp_to_json_10 = json.loads(dataset_10.to_json())
    shp_to_json_20 = json.loads(dataset_20.to_json())
    shp_to_json_30 = json.loads(dataset_30.to_json())
    shp_to_json_40 = json.loads(dataset_40.to_json())
    shp_to_json_50 = json.loads(dataset_50.to_json())
    shp_to_json_60 = json.loads(dataset_60.to_json())
    shp_to_json_70 = json.loads(dataset_70.to_json())
    shp_to_json_80 = json.loads(dataset_80.to_json())
    shp_to_json_90 = json.loads(dataset_90.to_json())
    t5 = time.time()

    t6 = time.time()
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_10,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_20,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_30,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_40,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_50,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_60,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_70,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_80,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_90,type ='fill',color = 'black',opacity = 0.95)
    t7 = time.time()

    print('geopandas import Time: {:.2f} seconds'.format(round(t_b - t_a, 2)))
    print('read shp to geodataframe Time: {:.2f} seconds'.format(round(t1 - t0, 2)))
    print('copy geodataframe Time: {:.2f} seconds'.format(round(t_d - t_c, 2)))
    print('query geodataframe Time: {:.2f} seconds'.format(round(t3 - t2, 2)))
    print('convert to json Time: {:.2f} seconds'.format(round(t5- t4, 2)))
    print('define mapbox layers Time: {:.2f} seconds'.format(round(t7 - t6, 2)))

if False:

    generate_from_shp(shpfile)






'''
~~~~~~~~~~~~~~~~
~~ Geopandas 2 ~~
~~~~~~~~~~~~~~~~
'''



def generate_from_shp_2(shpfile):
    """
    function to time shp to geopandas dataframe to json workflow
    """

    print('starting')

    t_a = time.time()
    import geopandas as gpd
    import pandas as pd 
    import numpy as np
    t_b = time.time()

    t0 = time.time()
    shp_df = gpd.read_file(shpfile)
    shp_np = shp_df.values
    print(shp_np.shape)
    print(type(shp_np))

    t1 = time.time()

    t_c = time.time()
    shp_dff = shp_df.copy(deep=True)
    t_d = time.time()
    
    t2 = time.time()
    dataset_10 = shp_df[shp_df['R_SCORE'].between(10,20,inclusive=False)]
    dataset_20 = shp_df[shp_df['R_SCORE'].between(20,30,inclusive=False)]
    dataset_30 = shp_df[shp_df['R_SCORE'].between(30,40,inclusive=False)]
    dataset_40 = shp_df[shp_df['R_SCORE'].between(40,30,inclusive=False)]
    dataset_50 = shp_df[shp_df['R_SCORE'].between(40,50,inclusive=False)]
    dataset_60 = shp_df[shp_df['R_SCORE'].between(50,60,inclusive=False)]
    dataset_70 = shp_df[shp_df['R_SCORE'].between(60,70,inclusive=False)]
    dataset_80 = shp_df[shp_df['R_SCORE'].between(80,90,inclusive=False)]
    dataset_90 = shp_df[shp_df['R_SCORE'].between(80,90,inclusive=False)]
    t3 = time.time()

    t4 = time.time()
    shp_to_json_10 = json.loads(dataset_10.to_json())
    shp_to_json_20 = json.loads(dataset_20.to_json())
    shp_to_json_30 = json.loads(dataset_30.to_json())
    shp_to_json_40 = json.loads(dataset_40.to_json())
    shp_to_json_50 = json.loads(dataset_50.to_json())
    shp_to_json_60 = json.loads(dataset_60.to_json())
    shp_to_json_70 = json.loads(dataset_70.to_json())
    shp_to_json_80 = json.loads(dataset_80.to_json())
    shp_to_json_90 = json.loads(dataset_90.to_json())
    t5 = time.time()

    t6 = time.time()
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_10,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_20,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_30,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_40,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_50,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_60,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_70,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_80,type ='fill',color = 'black',opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_90,type ='fill',color = 'black',opacity = 0.95)
    t7 = time.time()

    # print('geopandas import Time: {:.2f} seconds'.format(round(t_b - t_a, 2)))
    # print('read shp to geodataframe Time: {:.2f} seconds'.format(round(t1 - t0, 2)))
    # print('copy geodataframe Time: {:.2f} seconds'.format(round(t_d - t_c, 2)))
    # print('query geodataframe Time: {:.2f} seconds'.format(round(t3 - t2, 2)))
    # print('convert to json Time: {:.2f} seconds'.format(round(t5- t4, 2)))
    # print('define mapbox layers Time: {:.2f} seconds'.format(round(t7 - t6, 2)))

if False:
    generate_from_shp_2(shpfile)















        # datalist= [dataset_10,
    #     dataset_20,
    #     dataset_30,
    #     dataset_40,
    #     dataset_50,
    #     dataset_60,
    #     dataset_70,
    #     dataset_80,
    #     dataset_90]
    # print(dataset_10)
    # print(shp_to_json)
    # print('finished')
    # for i in datalist:
    #     shp_to_json = json.loads(i.to_json)
    #     # print(shp_to_json)
    #     print(i)

# .shp file and geopandas test
# datalist= ['dataset_10',
#     'dataset_20',
#     'dataset_30',
#     'dataset_40',
#     'dataset_50',
#     'dataset_60',
#     'dataset_70',
#     'dataset_80',
#     'dataset_90'
# ]

# def generate_from_json(jsonfile):
#     json_df = gpd.read_file(jsonfile)
#     dataset_10 = json_df[json_df['R_SCORE']>10]
#     dataset_20 = json_df[json_df['R_SCORE']>20]
#     dataset_30 = json_df[json_df['R_SCORE']>30]
#     dataset_40 = json_df[json_df['R_SCORE']>40]
#     dataset_50 = json_df[json_df['R_SCORE']>50]
#     dataset_60 = json_df[json_df['R_SCORE']>60]
#     dataset_70 = json_df[json_df['R_SCORE']>70]
#     dataset_80 = json_df[json_df['R_SCORE']>80]
#     dataset_90 = json_df[json_df['R_SCORE']>90]
#     print (dataset_90.head())

# generate_from_json(jsonfile)

# jsondata = json.loads(jsonfile)
# # dataset_10 = jsonfile[0]
# print(jsondata)


