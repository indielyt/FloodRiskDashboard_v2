# test of methods to access geospatial data
# 1. using .shp file and geopandas
# 2. using .json and python parsing
# 3. using .json in a postgres database and sqlalchemy

#  imports
import geopandas as gpd
import time
import json

# try:
#   from osgeo import ogr
#   print ('Import of ogr from osgeo worked.  Hurray!\n')
# except:
#   print ('Import of ogr from osgeo failed\n\n')

# import fiona
# print(fiona.supported_drivers)

# data
shpfile = r'Users/daniel/Documents/GitHub/FloodRiskDashboard_v2/shp/S_Structure.shp'
# jsonfile = r'jsons\S_Structure.json'


def generate_from_shp(shpfile):
    """
    function to time shp to geopandas dataframe to json workflow
    """

    print('starting')

    t_a = time.time()
    import geopandas as gpd
    t_b = time.time()

    t0 = time.time()
    shp_df = gpd.read_file(shpfile)
    t1 = time.time()
    
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
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_10,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_20,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_30,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_40,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_50,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_60,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_70,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_80,type ='fill',color = cm[bin],opacity = 0.95)
    geo_layer = dict(sourcetype = 'geojson',source = shp_to_json_90,type ='fill',color = cm[bin],opacity = 0.95)
    t7 = time.time()

    print('geopandas import Time: {:.2f} seconds'.format(round(t_b - t_a, 2)))
    print('read shp to geodataframe Time: {:.2f} seconds'.format(round(t1 - t0, 2)))
    print('query geodataframe Time: {:.2f} seconds'.format(round(t3 - t2, 2)))
    print('convert to json Time: {:.2f} seconds'.format(round(t5- t4, 2)))
    print('define mapbox layers Time: {:.2f} seconds'.format(round(t7 - t6, 2)))

if False:

    generate_from_shp(shpfile)


    # t2 = time.time()
    # generate_from_json(jsonfile)
    # t3 = time.time()

    # print('shp Solve Time: {:.2f} seconds'.format(round(t1 - t0, 2)))
    # print('json Solve Time: {:.2f} seconds'.format(round(t3 - t2, 2)))




























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


