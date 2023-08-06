##############################################################
# demonstration script for resampling, stacking, mosaicking and subsetting SAR images
# John Truckenbrodt 2017
##############################################################

import sys

sys.path = ['', '/geonfs02_vol2/software/local/lib/python2.7/site-packages/GDAL-2.2.1-py2.7-linux-x86_64.egg',
            '/usr/local/lib/python2.7/site-packages/GDAL-2.0.0-py2.7-linux-x86_64.egg',
            '/geonfs02_vol2/software/local/lib/python2.7/site-packages',
            '/geonfs01_vol1/01_EMS_SALDI_KNP_S1/xx_2_mosaicing', '/usr/local/lib/python27.zip',
            '/usr/local/lib/python2.7', '/usr/local/lib/python2.7/plat-linux2', '/usr/local/lib/python2.7/lib-tk',
            '/usr/local/lib/python2.7/lib-old', '/usr/local/lib/python2.7/lib-dynload',
            '/homes2/geoinf/c3urma/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/site-packages']

import os
import re
from time import mktime, strptime

from pyroSAR.ancillary import finder
from pyroSAR.spatial.vector import Vector
from pyroSAR.spatial.raster import stack


# function to extract time stamp from file name. Images processed with pyroSAR functionalities via module snap or gamma will contain this information.
def seconds(name): return mktime(strptime(re.findall('[0-9T]{15}', name)[0], '%Y%m%dT%H%M%S'))


# define input directory containing file sto be stacked
dir_in = '/geonfs01_vol1/01_EMS_SALDI_KNP_S1/01_S1_GRD/02_processed'

# define output file name
dstfile = '/geonfs01_vol1/01_EMS_SALDI_KNP_S1/01_S1_GRD/03_mosaic/01_A_VH/S1_A_VH_mosaic_KNP_0515_0517'

# shapefile (for stack boundaries)
shp = finder('/geonfs01_vol1/01_EMS_SALDI_KNP_S1/01_S1_GRD/xx_study_area', ['KNP_Area.shp'])
# shp = '/geonfs01_vol1/01_EMS_SALDI_KNP_S1/xx_study_area/KNP_Area.shp'

# store results in separate files or one single stack file? If separate then dstfile is used as a directory.
sep = False

# define
# srcfiles = finder(dir_in, [sensor + '*' + orbit + year + '*' + pol + '*.tif'])
srcfiles = finder(dir_in, ['*_201505*VH*db.tif'])
srcfiles.extend(finder(dir_in, ['*_201506*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201507*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201508*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201509*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201510*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201511*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201512*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_2016*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201701*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201701*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201703*VH*db.tif']))
srcfiles.extend(finder(dir_in, ['*_201704*VH*db.tif']))

if os.path.isfile(dstfile):
    raise IOError('dstfile already exists')

site = Vector(shp)

# sort images by time stamp
srcfiles = sorted(srcfiles, key=seconds)

# print srcfiles

# create groups of similar time stamps for mosaicking. All images with a time stamp of less than 30s difference will be mosaicked
# groups = []
# temp = []
# for item in srcfiles:
# if len(temp) == 0:
# temp.append(item)
# else:
# if 0 < abs(seconds(item)-seconds(temp[-1])) < 30:
# temp.append(item)
# else:
# groups.append(temp) if len(temp) > 1 else groups.append(temp[0])
# temp = [item]

# # final function call
# stack(srcfiles=groups, dstfile=dstfile, resampling='bilinear', targetres=[10, 10], srcnodata=-99, dstnodata=-99, shapefile=site, sortfun=seconds, separate=sep, overwrite=True)


for tile in shp:
    
    tile_no = os.path.splitext(os.path.basename(tile))[0]
    print
    'Processing Tile: ' + tile_no
    
    srcfiles = sorted(srcfiles, key=seconds)
    groups = []
    temp = []
    
    for item in srcfiles:
        if len(temp) == 0:
            temp.append(item)
        else:
            if abs(seconds(item) - seconds(temp[-1])) < 3600:
                temp.append(item)
            else:
                groups.append(temp) if len(temp) > 1 else groups.append(temp[0])
                temp = [item]
    
    groups.append(temp)
    
    if not os.path.exists(os.path.normpath(os.path.join(dstpath, str(tile_no)))):
        os.mkdir(os.path.join(dstpath, str(tile_no)))
    
    dstfile = os.path.join(dstpath, str(tile_no), "S1_A_VH_mosaic_" + str(tile_no))
    
    if not os.path.isfile(dstfile):
        try:
            stack(srcfiles=groups, dstfile=dstfile, resampling='near', targetres=[10, 10], srcnodata=-99, dstnodata=-99,
                  shapefile=shp, sortfun=seconds, separate=sep, overwrite=overwrite)
        except StandardError:
            print
            "No files for %s" % tile_no
