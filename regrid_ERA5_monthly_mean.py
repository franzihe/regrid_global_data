# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
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

from imports import (np, xr, fct, glob)

# reload imports
# %load_ext autoreload
# %autoreload 2

# +
### Define data location for ERA5 and CMIP6
era_path    = '/home/franzihe/nird_ERA5/'
#era_path    = '/projects/NS1000K/franzihe/data/ERA5/'

### Data location for file of reference grid
cmip_path   = '/home/franzihe/nird_CMIP6/NorESM2-MM/r1i1p1f1/'
#cmip_path   = '/projects/NS9252K/CMIP6/historical/NorESM2-MM/r1i1p1f1/'
variable = {
            '2t':   '2m_temperature', 
            'msr'  :'mean_snowfall_rate',
            'sf'   :'snowfall',                         # ERA5 single level variables
            't'   :'temperature',
            'clwc':'specific_cloud_liquid_water_content',
            'clic':'specific_cloud_ice_water_content',
            'cswc':'specific_snow_water_content'        # ERA5 pressure level variables
           }



# + jupyter={"outputs_hidden": true}
for keys, var in variable.items(): 
    for years in np.arange(2014,2015):
        if years <= 1989:
            yy = 1989
        elif years <= 1999:
            yy = 1999
        elif years <= 2009:
            yy = 2009
        elif years <= 2014:
            yy = 2014

        ### Input data from ERA5 with a resolution of 0.25x0.25 deg
        era_file = glob('{}{}_Amon_ERA5_*{}12.nc'.format(era_path, keys, yy))[0]
        ds_in = xr.open_dataset(era_file, ).sel(time = slice(str(years)+'-01', str(years)+'-12'))

        ### Read in the regridder data (NorESM)
        cmip_file = glob('{}prsn_Amon_NorESM2-MM_historical_r1i1p1f1*{}12.nc'.format(cmip_path,yy))[0]
        ds_out = xr.open_dataset(cmip_file).sel(time = slice(str(years)+'-01', str(years)+'-12'))

        ### Regrid and save to file to nc_out
        nc_out = '{}/1deg/{}_Amon_ERA5_1deg_{}01_{}12.nc'.format(era_file[:24], keys, years, years)
        fct.regrid_save_data(ds_in, ds_out, nc_out)





# -

