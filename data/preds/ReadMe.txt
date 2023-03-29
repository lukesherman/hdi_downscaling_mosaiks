 # ReadMe.txt # 
 
 
 Global High Resolution Estimates of the Human Development Index, Beta Version
 
 Note that our methods have not undergone peer review and this data is only a preliminary
 (beta) data release. 

## BACKGROUND
This `ReadMe` file provides information necessary to understand and interpret the accompanying 
raster (.tif) and tabular (.csv) HDI data files.

Note that these data should be used cautiously. These are only estimates and may contain
noise, systematic bias, compressed variance, and other errors. 


GitHub github.com/lukesherman/hdi_downscaling_mosaiks
Email: lsherman@berkeley.edu



## RASTER DATA
Layer 1: 		HDI Grid Level Estimates
					- These are the predictions generated from the machine learning model 
					  combining MOSAIKS daytime image and nightlight (NL) features
					  
					- These predictions are clipped to have values that fall within 0 and 1.
					
					- These estimates are centered such that the population-weighted average
					   of the 0.01 x 0.01 degree tile HDI estimates matches the ADM1 data
					   from Smits and Permanyer (https://globaldatalab.org/shdi).
					   
					- Population density weights come from the Gridded Population of the 
					  World (GPW) V4 (https://sedac.ciesin.columbia.edu/data/collection/gpw-v4).
					  
					- We also use a more precise population mask to ensure we only release 
					estimates where human settlements are known to exist. To do this, we 
					mask our raw model predictions using data from the Human Settlement
	 					Data Layer (at https://ghsl.jrc.ec.europa.eu/).


resolution: 		0.1 x 0.1 degree
no data value:		numpy.nan
raster extent:		[-180,180, -56, 74]





## TABULAR DATA
Tablular data can be merged with the CGAZ ADM2 administrative geojson from geoBoundaries. 

Specifically, you will need the CGAZ version 3.0.0 data product. The archived data release has a GitHub available here:
https://github.com/wmgeolab/geoBoundariesArchive_3_0_0/
 
The specific file used in our analysis is also available here: 
https://www.geoboundaries.org/data/geoBoundariesCGAZ-3_0_0/ADM2/simplifyRatio_100/geoBoundariesCGAZ_ADM2.geojson


Columns:
predicted_adm2_HDI: 		- Predictions generated from the machine learning model 
					  		   combining MOSAIKS daytime image and nightlight (NL) features
					  		   
					  		- Predictions are centered such that the average
					   		  of the ADM2 estimates contained by each ADM1 region matches
					   		  the ADM1 value from Smits and Permanyer (https://globaldatalab.org/shdi).
					   		
					   		- Estimates are not released where Smits and Permanyer have not
					   		  produced ADM1 HDI estimates.
					   		  
					   		- ADM2 estimates for Ireland are not released as the ADM2 units 
					   		  from geoBoundaries are so small that they cannot be
					   		  adequately verified.
					   		  
est_total_pop:				- Total population count contained in each ADM2 region. This 
							  data comes from GPW V4.
							  
adm1_HDI_Smits:				- 2019 HDI estimate for the parent Global Data Lab
							  ADM1 administrative unit. Please cite Smits and Permanyer (2019)
							  https://www.nature.com/articles/sdata201938 if using these data.
							  
percent_overlap_GDL_ADM1 	- Indicates the percent of the geoBoundaries ADM2 unit
								that overlaps the Global Data Lab ADM1 shapefile (using a 
								WGS84 projection). Lower overlap implies more uncertainty 
								in the re-centering.

GDL_ADM1					- ADM1 code used by the Global Data Lab (GDL) and can be
							  used to merge with their data. 
							  
ADM1_shapeID				- Parent ADM1 code used by geoBoundaries. Note that
							  this is not an exact match with the GDL shapefile

shapeGroup					- Standard ISO3 code identifying the parent country

shapeName					- Common name for the ADM2 unit from geoBoundaries

shapeID						- Unique identifier for each ADM2 unit from geoBoundaries (primary key)
							
	
	