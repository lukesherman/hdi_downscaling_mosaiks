import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import geopandas as gpd
import shapely
import fiona

from affine import Affine

import pandas as pd
import rasterio
import rasterio.mask
from rasterio import warp

import warnings


bins = np.hstack([0,np.linspace(0.0,63,20)]) # Bin creation for 20 feats, includes right edge


def apply_polygon_mask_and_return_flat_array(polygons, raster_file, plot=False, pad=False, return_2d_window = False):
    
    """
    
    Function to return a flat array of overlapping pixels between a shapefile geometry (shapely polygon) and a rasterio file. 
    
    Per documentation in rasterio.mask.mask raster pixels will be included when their center overlays the polygon.
    """
    arrays = []
    out_image, out_transform = rasterio.mask.mask(raster_file, [polygons], crop=True, nodata = np.nan, 
                                                  pad=pad, all_touched=False)
    if plot == True:
        fig, ax = plt.subplots(figsize=(10,8))
        f = plt.imshow(out_image[0])
        fig.colorbar(f)
    if return_2d_window:
        return out_image
    array = out_image[0].flatten()
    array = array[~np.isnan(array)]
    arrays.append(array)
    try:       
        return np.hstack(arrays)
    except:
        return np.array([0])
    
    

def correct_nl_df_creation(out, shp_file, raster_file, bins = bins):
    """
    Some of the ADM2 and other polygons are so small that we need to get the nearest NL pixel, 
    rather the consider the pixel to be contained by the polygon. This implements this correction AND adds 0 value for an
    data that are still missing
    
    """
    null_idxs = out[out.iloc[:,0].isnull()].index
    
    num_missing =  len(null_idxs)
    print("Num missing = ", num_missing)
    if num_missing == 0:
        return out
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") # suppress warnings for unprojected buffer
        #Create buffer the centroid of the adm polygon, equivelant to calculating centroid to centroid nearest
        buffers = shp_file.loc[null_idxs]["geometry"].centroid.buffer(0.00833333333333/2)
    
    
    for i, buffer in enumerate(buffers):
        
        a = apply_polygon_mask_and_return_flat_array(buffer, raster_file = raster_file)
        assert len(a) <= 1
        
        # if there is still no nl value being grabbed, it means we are off the raster. Assume 0 NL 
        if len(a) == 0:
            a = np.array([0])
            
        d =  np.histogram(a, bins=bins, density = False, weights=None)
        perc_in_each_bin = d[0]
        
        if i == 0:
            stacked = perc_in_each_bin
        else:
            stacked = np.vstack([stacked, perc_in_each_bin])
            
    fixed_out = pd.DataFrame(stacked, index = null_idxs)
    
    fixed_out.columns =  ["perc_pixels_in_bin_" + str(i) for i in range(out.shape[1])]
        
    out_dropped = out.drop(null_idxs)
        
    return pd.concat([fixed_out,out_dropped])




def create_nl_binned_dataframe(shp_file, raster_file,bins=bins, weight_raster = None):
    
    for i, polygon in enumerate(shp_file["geometry"]):
        a = apply_polygon_mask_and_return_flat_array(polygon, plot=False, raster_file=raster_file)
        
        w = None
        if weight_raster:
            w = apply_polygon_mask_and_return_flat_array(polygon, plot=False, raster_file=weight_raster)

            assert a.shape == w.shape

        d =  np.histogram(a, bins=bins, density = False, weights=w)
        
        if weight_raster:
            perc_in_each_bin = d[0]/w.sum()
        else:
            perc_in_each_bin = d[0]/len(a)

        if i == 0:
            stacked = perc_in_each_bin
        else:
            stacked = np.vstack([stacked, perc_in_each_bin])
    
#     assert all(stacked.sum(axis=1).round(5) == 1)
    
    out = pd.DataFrame(stacked, index = shp_file.index)
    out.columns =  ["perc_pixels_in_bin_" + str(i) for i in range(out.shape[1])]

    return out