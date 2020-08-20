# Development of segmented jsons based on scoring pillars and binning of the values

# Resources
# Activating arcgisPro conda environment  --  http://pro.arcgis.com/en/pro-app/arcpy/get-started/installing-python-for-arcgis-pro.htm#ESRI_SECTION2_03D9AE2696B241A2BDA803651E0F6892

import arcpy
import numpy as np
import os


# arcpy.env.workspace = r'C:\Users\Daniel.Aragon\Desktop\dashboarddata_12212018\V1_DashboardStagingData.gdb'
# json_folder = r'C:\Users\Daniel.Aragon\Downloads\new_data\R_SCORE'
# json_folder = r'C:\Users\Daniel.Aragon\Downloads\new_data\FR_TOT'
# json_folder = r'C:\Users\Daniel.Aragon\Downloads\new_data\AEP_TOT'
json_folder = r"C:\Users\Daniel.Aragon\Downloads\contours"


# dataset = R'C:\Users\Daniel.Aragon\Downloads\new_data\shp\S_Structure.shp'
dataset = r'W:\Risk MAP\2_0\Version2_RiskScoring_20190123\_data\RM_2_1_RiskAssessmentDB.gdb\CONF_CONTOURS_10'

# field = 'R_SCORE'
# field = 'FR_TOT'
# field = 'AEP_TOT'
# field = 'FDP_TOT'
field = 'Contour'


# develop intervals for binning
def percentiles_linear_spacing(start, stop, num_intervals):
	linspace = np.linspace(start, stop, num_intervals)
	return linspace.astype(int)


def output_binned_geojson(dataset, field, linspace_array): #, basename):
	# Make a layer from the feature class
	arcpy.MakeFeatureLayer_management(dataset, "lyr")

	for i in range(len(linspace_array)-1):
		json_name = str(linspace_array[i]) + "-" + str(linspace_array[i+1]) + ".geojson"
		# define sql where clause for select by attribute procoess
		whereclause = """{} < {} AND {} <= {}""".format(
			linspace_array[i], 
			arcpy.AddFieldDelimiters(dataset, field), # Correctly quotes/noquotes dataset depending on source location
			arcpy.AddFieldDelimiters(dataset, field), # Correctly quotes/noquotes dataset depending on source location
			linspace_array[i+1])
		arcpy.SelectLayerByAttribute_management("lyr", "CLEAR_SELECTION", whereclause) # Clear selection before select by attribute helped to make the script work
		arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", whereclause)
		arcpy.FeaturesToJSON_conversion("lyr", os.path.join(json_folder,json_name), "NOT_FORMATTED", "NO_Z_VALUES", "M_VALUES", "GEOJSON") # Convert the selected features to JSON

output_binned_geojson(dataset, field, percentiles_linear_spacing(0,100,11))