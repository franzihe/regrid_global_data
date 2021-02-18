# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Regrid xarray data
# https://xesmf.readthedocs.io/en/latest/ 
#
# Regrid xarray Dataset with multiple variables for ERA5 data to NorESM2-MM grid.

# +
# supress warnings
import warnings
warnings.filterwarnings('ignore') # don't output warnings

from imports import (np, xr, fct, glob, )

# reload imports
# %load_ext autoreload
# %autoreload 2

# +
### Define data location for ERA5 and CMIP6

era_path     = '/home/franzihe/nird_NS9600K/data/ERA5/3_hourly/2008/'

### Data location for file of reference grid
cmip_path   = '/home/franzihe/nird_NS9600K/shofer/Rob/INP_nimax_fix/'
variable = {
#            '2t':   '2m_temperature', 
 #           'msr'  :'mean_snowfall_rate',
            'sf'   :'snowfall',                         # ERA5 single level variables
  #          't'   :'temperature',
   #         'clwc':'specific_cloud_liquid_water_content',
    #        'clic':'specific_cloud_ice_water_content',
     #       'cswc':'specific_snow_water_content'        # ERA5 pressure level variables
           }





# -
year = 2008

# +
### Read in the regridder data (NorESM)
cmip_file = sorted(glob('{}INP_fixed_nimax.cam.h2.2008*.nc'.format(cmip_path)))[0]
ds_out = xr.open_dataset(cmip_file)

for keys, var in variable.items(): 
    for month in np.arange(1,13):
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            t = np.arange(1, 32)
        elif month == 2:
            t = np.arange(1, 30)
        elif month == 4 or month == 6 or month == 9 or month == 11:
            t = np.arange(1,31)

        if int(month) < 10:
            month = '0{}'.format(int(month))
        for day in t:
            if int(day) < 10:
                day = '0{}'.format(int(day))
                
            Date = '{}-{}-{}'.format(year, month, day)
            

            ### Input data from ERA5 with a resolution of 0.25x0.25 deg
            era_file = glob('{}{}_3hourly_ERA5_2008{}.nc'.format(era_path, keys, month))[0]
            ds_in = xr.open_dataset(era_file, ).sel(time = slice('{}'.format(Date)))

            ### Regrid and save to file to nc_out
            fct.createFolder('{}/NorESMgrid/'.format(era_file[:51]))
            nc_out = '{}/NorESMgrid/{}_3hourly_ERA5_{}{}{}.nc'.format(era_file[:51], keys, year, month, day)
            fct.regrid_save_data(ds_in, ds_out, nc_out,)


# -

