"""
Code purpose: Hydro-condition a given Prairie watershed using custom pwa-tools module.
Author: Idil Yaktubay, iyaktubay@iisd-ela.org (IISD-ELA)
Last Updated: July 2025
"""
# Import custom pwa-tools module (must be installed following instructions in README.md)
import pwa_tools as pwa


# Organize data folders and files and store relevant directory information in a dictionary
# (user will be prompted to enter the watershed name to name the working directory after)
DIRECTORY_DICT = pwa.set_directory_structure()


# Name of watershed shapefile from CLRH hydrofabrics zip file (.shp)
CLRH_FILENAME = pwa.hydrocon_usr_input().file("hydrofabric shapefile", 
                                              "finalcat_info_v1-0") # This is the default for Manning Canal


# Name of LiDAR DEM raster from LiDAR DEM zip file (.tif)
# This can be multiple files, separated by commas (e.g., Boyne river requires multiple rasters))
# Multiple rasters will be merged into one in latter steps
LIDAR_FILENAME = pwa.hydrocon_usr_input().file("LiDAR DEM raster", 
                                               "sr_dem_cgvd28") # This is the default for Manning Canal


# Name of streams shapefile from NHN streams zip file (.shp)
NHN_FILENAME = pwa.hydrocon_usr_input().file("NHN streams shapefile", 
                                             "NHN_05OE000_5_0_HD_SLWATER_1") # This is the default for Manning Canal


# Boolean object to indicate if there are multiple LiDAR DEM rasters
MULTIPLE_LIDAR_RASTERS = True if (isinstance(LIDAR_FILENAME, list) and len(LIDAR_FILENAME)) > 1 else False


# Load CLRH subbasins shapefile as geodataframe
clrh_gdf = pwa.read_shapefile(filename=CLRH_FILENAME,
                              directory=DIRECTORY_DICT["HYDROCON_RAW_PATH"])


# Merge rasters if multiple LiDAR DEM rasters are provided
if MULTIPLE_LIDAR_RASTERS:
    LIDAR_FILENAME = pwa.merge_rasters(lidar_files=LIDAR_FILENAME,
                                       gdf=clrh_gdf,
                                       dict=DIRECTORY_DICT)


# Directory for the LiDAR DEM raster (merged or single)
LIDAR_ROOT = DIRECTORY_DICT["HYDROCON_INTERIM_PATH"] if MULTIPLE_LIDAR_RASTERS else DIRECTORY_DICT["HYDROCON_RAW_PATH"]


# Project subbasins shapefile to match LiDAR DEM raster CRS
clrh_gdf_projected_lidar, input_lidar_crs, \
input_lidar_crs_alnum,  CLRH_PROJ_LIDAR_FILE = pwa.project_subbasins_to_lidar(gdf=clrh_gdf,
                                   gdf_filename=CLRH_FILENAME,
                                   lidar_filename=LIDAR_FILENAME, 
                                   lidar_directory=LIDAR_ROOT,
                                   dict=DIRECTORY_DICT)


# Clip LiDAR DEM raster to the projected subbasins shapefile
# # This may take longer than other tasks
if not MULTIPLE_LIDAR_RASTERS:
    LIDAR_CLIPPED_FILE = pwa.clip_lidar_to_shapefile(projected_gdf=clrh_gdf_projected_lidar,
                                                    lidar_filename=LIDAR_FILENAME,
                                                    lidar_directory=LIDAR_ROOT,
                                                    dict=DIRECTORY_DICT)
else:
    # if multiple rasters were provided, they were already clipped in pwa.merge_rasters
     LIDAR_CLIPPED_FILE = LIDAR_ROOT + LIDAR_FILENAME


# Resample the clipped LiDAR DEM raster to 5m resolution
LIDAR_CLIPPED_RESAMPLED_FILE = pwa.resample_lidar_raster(lidar_file=LIDAR_CLIPPED_FILE, 
                                                        resolution_m=5)


# Load NHN streams shapefile as geodataframe
nhn_gdf = pwa.read_shapefile(filename=NHN_FILENAME,
                              directory=DIRECTORY_DICT["HYDROCON_RAW_PATH"])


# Project subbasins shapefile to align with NHN streams shapefile
clrh_gdf_projected_to_nhn, CLRH_PROJ_NHN_FILE = pwa.project_crs_subbasins_to_nhn(nhn_gdf=nhn_gdf,
                                                         subbasins_gdf=clrh_gdf,
                                                         subbasins_filename=CLRH_FILENAME,
                                                         dict=DIRECTORY_DICT)


# Clip NHN streams shapefile to watershed
NHN_CLIPPED_PROJECTED_LIDAR_FILE = pwa.clip_nhn_to_watershed(nhn_filename=NHN_FILENAME, 
                                                        clrh_proj_nhn_file=CLRH_PROJ_NHN_FILE,
                                                        input_DEM_crs=input_lidar_crs,
                                                        input_DEM_crs_alnum=input_lidar_crs_alnum,
                                                        dict=DIRECTORY_DICT)


# Generate depression depths raster
DEPRESSIONS_RASTER_FILE = pwa.gen_depressions_raster(lidar_filename=LIDAR_FILENAME,
                            lidar_clipped_resampled_file=LIDAR_CLIPPED_RESAMPLED_FILE,
                           nhn_clipped_projected_lidar_file=NHN_CLIPPED_PROJECTED_LIDAR_FILE,
                           resolution_m=5,
                           dict=DIRECTORY_DICT)


# Generate wetland polygons shapefile with stats (this is NOT required for RAVEN, user will skip if not needed)
# Ask user if they want to generate a wetlands shapefile with stats
WANT_WETLANDS_SHAPEFILE = pwa.hydrocon_usr_input().string("\"Yes\" if you would like to also generate a wetlands shapefile with stats (NOT required for RAVEN)", 
                                                          "No")
if WANT_WETLANDS_SHAPEFILE.lower() == "yes":
    WETLAND_POLYGONS_FILE = pwa.gen_wetland_polygons(depressions_raster_file=DEPRESSIONS_RASTER_FILE,
                                                     dict=DIRECTORY_DICT)


# Calculate depression depths
DEPRESSION_DEPTHS_FILE = pwa.calc_depression_depths(clrh_proj_lidar_file=CLRH_PROJ_LIDAR_FILE,
                           watershed_name=DIRECTORY_DICT["WATERSHED_NAME"],
                           depressions_raster_file=DEPRESSIONS_RASTER_FILE,
                           clrh_gdf_projected_lidar=clrh_gdf_projected_lidar,
                           dict=DIRECTORY_DICT)