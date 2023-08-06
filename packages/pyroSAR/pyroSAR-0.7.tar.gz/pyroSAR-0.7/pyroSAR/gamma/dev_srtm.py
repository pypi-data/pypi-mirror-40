evil = '/usr/local/lib/python2.7/site-packages/GDAL-2.0.0-py2.7-linux-x86_64.egg'
import sys

if evil in sys.path:
    del sys.path[sys.path.index(evil)]

from pyroSAR import identify
from pyroSAR.gamma.srtm import makeSRTM

filename = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141012T162337_20141012T162402_002799_00326F_8197.zip'

makeSRTM(scenes=[identify(filename)],
         srtmdir='/geonfs02_vol1/SRTM_1_HGT',
         outname='/geonfs01_vol1/ve39vem/test/proc_gamma/out/srtm')
