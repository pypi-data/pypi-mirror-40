from pyroSAR.gamma.parser import parse_command

# command = '/usr/local/GAMMA_SOFTWARE-20180703/LAT/bin/validate'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/IPTA/bin/dis_data'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/DIFF/bin/gc_map'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/LAT/bin/stokes'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/LAT/bin/comb_hsi'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/LAT/bin/product'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/ISP/bin/par_ESA_ERS'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/DIFF/bin/create_dem_par'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/IPTA/bin/ras_data_pt'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/IPTA/bin/rasdt_cmap_pt'
# command = '/usr/local/GAMMA_SOFTWARE-20180703/DIFF/bin/ras_clist'
command = '/usr/local/GAMMA_SOFTWARE-20180703/ISP/bin/SLC_interp_map'

print(parse_command(command))
