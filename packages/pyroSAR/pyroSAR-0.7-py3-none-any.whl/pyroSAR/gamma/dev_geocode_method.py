from pyroSAR.gamma import geocode
from pyroSAR import Archive
from pyroSAR.S1 import OSV

from swos.config import dbfile, S1_osvdir
from swos.ancillary import load_site, create_dem

resolution = 20
res_osv = False
sitename = 'Greece_Eastern-Macedonia'

site = load_site(sitename, 'delimitation')

with OSV(S1_osvdir) as osv:
    maxdate = osv.maxdate(osvtype='POE', datetype='stop')

with Archive(dbfile) as archive:
    selection_proc = archive.select(vectorobject=site,
                                    maxdate=maxdate,
                                    sensor=('S1A', 'S1B'),
                                    product='GRD',
                                    acquisition_mode='IW',
                                    vv=1)

demfile = create_dem(sitename)

# scene = selection_proc[0]
scene = '/geonfs02_vol3/swos/data/S1A_IW_GRDH_1SDV_20141115T181801_20141115T181826_003296_003D12_0F6C.zip'

for geomethod in [1, 2]:
    tempdir = '/geonfs01_vol1/ve39vem/test/proc_gamma/temp_{}'.format(geomethod)
    outdir = '/geonfs01_vol1/ve39vem/test/proc_gamma/out_{}'.format(geomethod)
    
    geocode(scene, dem=demfile,
            tempdir=tempdir, outdir=outdir,
            targetres=resolution, scaling='db',
            func_geoback=2, func_interp=0, sarSimCC=False,
            osvdir=S1_osvdir, cleanup=False, allow_RES_OSV=res_osv,
            geocode_method=geomethod)
