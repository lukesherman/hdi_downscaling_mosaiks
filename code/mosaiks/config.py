"""This module is loaded to access all model settings.
The first group contains global settings, and then each
application area has its own settings. The variable name for
each application must be associated with a dictionary that
at the minimum has the following keys:


Keys:
-----
application : str
    Name of application area.
variable : str or list of str
    The name(s) of the variable(s) being predicted in this
    application area.
sampling : str
    The sampling scheme used for the preferred model for this
    application area (e.g. 'POP')
"""
######################
# PROJECT SETTINGS
######################

# Verbose
verbose = True

# GPU -- set to True to use torch.cuda.is_available to check for GPUs.
# If False, will never check for a GPU.
GPU = False

import os
from os.path import basename, dirname, join

import numpy as np

import seaborn as sns
import mosaiks 
import matplotlib.colors as mcolors

# # get home directory
# if "MOSAIKS_HOME" in os.environ:
#     root_dir = os.environ["MOSAIKS_HOME"]
# else:
#     c_dir = dirname(dirname(mosaiks.__file__))
#     # assume if we don't find site-packages at this layer, then this package was
#     # installed in place (i.e. with -e flag in pip install)
#     if basename(c_dir) == "site-packages":
#         root_dir = "/"
#     else:
#         root_dir = dirname(c_dir)
#     print(
#         "env variable MOSAIKS_HOME not defined;"
#         ' setting to: "{}"'.format(root_dir)
#         + '\nIf not desired, please reset os.environ["MOSAIKS_NAME"]'
#     )
#     os.environ["MOSAIKS_HOME"] = root_dir

# # code_dir is mosaiks/code/
# code_dir = os.environ.get("MOSAIKS_CODE", join(root_dir, "code"))
# # data_dir is mosaiks/data
# data_dir = os.environ.get("MOSAIKS_DATA", "/shares/maps100/data/")
# # grid_dir is mosaiks/data/grids
# grid_dir = join(data_dir, "int", "grids")
# # features is mosaiks/data/features
# features_dir = "/shares/maps100/data/features/"
# # output is mosaiks/data/output
# out_dir = join(data_dir, "output")
# # final results at mosaiks/results
# res_dir = os.environ.get("MOSAIKS_RESULTS", join(root_dir, "results"))
# os.makedirs(res_dir, exist_ok=True)
# # main prediction directory
# main_pred_dir = "/shares/maps100/results/predictions/main"
# # main plot directory
# main_plot_dir = "/shares/maps100/results/plots/main"
# # general logs directory
# main_log_dir = "/shares/maps100/results/logs/main"



# shapefile paths (for regional models)
# continent
shp_path_stem = "/shares/maps100/data/raw/region_shapefiles/"
continent_shp_path = (shp_path_stem +
                      "World_Continents_NoAntarctica/" +
                      "World_Continents_NoAntarctica.shp")

# figures directory for final paper
main_fig_dir = "/shares/maps100/results/figures"    

# country
country_shp_path = (shp_path_stem +
                    "gadm/gadm36_0.shp")

# path to sparse grid pop density file; for weighted feature aggregation 
sparse_grid_pop_density_path = ("/shares/maps100/data/int/applications/population"
                               "/outcomes_sampled_population_LandmassIntermediateResSparseGrid10.csv")

dense_grid_pop_density_path = ("/shares/maps100/data/int/applications/population"
                               "/population_density_global_dense_grid_2022_7.p")

pop_density_val_colname = "population"

# ML MODEL
ml_model = {
    "seed": 0,
    "test_set_frac": 0.2,
    "model_default": "ridge",
    "n_folds": 5,
    "global_lambdas": np.logspace(-4, 3, 9),
}


# colors
colorblind_friendly_teal = "#029e73"


# REGIONAL MODELS
continent_vm_dict = {
    'Africa': ['4', '5', '6', '7'],
    'Asia': ['1', '4', '5', '6', '7', '8', '9', '10'],
    'Australia': ['9', '10'],
    'North America': ['1', '2', '3'],
    'Oceania': ['1', '9', '10'],
    'South America': ['2', '3', '4'],
    'Europe': ['4', '5', '6']
}

shp_file_dict = {
    "continent": continent_shp_path,
    "country": country_shp_path
}

region_col_dict = {
    "continent": "CONTINENT",
    "country": "NAME_0"
}


# Default thresholds for Hurdle model:
default_hurdle_thresholds = [0.95, 0.90, 0.8, 0.65, 0.5]


# Category colors
category_colors = {'Demographics': '#4E79A7',
                'Education': '#F28E2B',
                'Health': '#E15759',
                'Income': '#76B7B2',
                'Occupation': '#59A14F',
                'Household Assets':  "#D4AF37",
                'Agricultural Assets': '#A020F0',
                'Agriculture': '#EC008C',
                'Built Infrastructure': '#161616',
                'Natural Systems': '#964B00'
                }
# Category cmaps
category_cmaps = category_colors.copy()
for key in category_cmaps.keys():
    category_cmaps[key] = mcolors.LinearSegmentedColormap.from_list("", ["white", category_cmaps[key]])

