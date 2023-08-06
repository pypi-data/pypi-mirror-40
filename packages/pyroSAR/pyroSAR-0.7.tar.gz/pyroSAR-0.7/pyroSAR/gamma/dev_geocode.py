evil = '/usr/local/lib/python2.7/site-packages/GDAL-2.0.0-py2.7-linux-x86_64.egg'
import sys

if evil in sys.path:
    del sys.path[sys.path.index(evil)]

from pyroSAR.gamma import geocode

from swos.config import dbfile, S1_osvdir
from swos.ancillary import load_site, create_dem

resolution = 20
res_osv = False
sitename = 'Greece_Eastern-Macedonia'

# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141115T181801_20141115T181826_003296_003D12_0F6C.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141006T043046_20141006T043111_002704_003061_3C03.zip'
scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141012T162337_20141012T162402_002799_00326F_8197.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141012T162402_20141012T162427_002799_00326F_864B.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141014T160713_20141014T160738_002828_003302_2775.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141014T160738_20141014T160803_002828_003302_60AF.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141018T043021_20141018T043046_002879_003422_95D5.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141018T043046_20141018T043111_002879_003422_0269.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141019T161539_20141019T161604_002901_003491_1BB2.zip'
# scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141024T162337_20141024T162402_002974_003618_AD11.zip'


demfile = create_dem(sitename)

tempdir = '/geonfs01_vol1/ve39vem/test/proc_gamma/temp'
outdir = '/geonfs01_vol1/ve39vem/test/proc_gamma/out'

geocode(scene, dem=demfile,
        tempdir=tempdir, outdir=outdir,
        targetres=resolution, scaling='db',
        func_geoback=2, func_interp=0, sarSimCC=False,
        osvdir=S1_osvdir, cleanup=False, allow_RES_OSV=res_osv,
        normalization_method=1)
