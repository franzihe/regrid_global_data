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

# +
# supress warnings
import warnings
warnings.filterwarnings('ignore') # don't output warnings

from imports import (np, xr, fct, glob)

# reload imports
# %load_ext autoreload
# %autoreload 2

# +
cmip_models = [
    'BCC-CSM2-MR',
#    'CAS-ESM2-0',
    'CESM2',
    'CESM2-WACCM-FV2',
    'CMCC-CM2-SR5',
    'E3SM-1-0',
    'E3SM-1-1',
    'E3SM-1-1-ECA',
    'FGOALS-f3-L',
    'GFDL-CM4',
    'GFDL-ESM4',
    'MPI-ESM1-2-HR',
    'NorESM2-MM',
    'SAM0-UNICON',
    'TaiESM1',
    'MRI-ESM2-0',    
]

### Data location for file of reference grid
#cmip_path   = '/home/franzihe/nird_CMIP6/NorESM2-MM/r1i1p1f1/'
cmip_path   = '/projects/NS9252K/CMIP6/historical/NorESM2-MM/r1i1p1f1/'

variable = {
            'prsn': 'snowfall_flux',
            'tas' : 'air_temperature',
            'ta'  : 'air_temperature_pl',
            'cli' : 'mass_fraction_of_cloud_ice_in_air', 
            'clw' : 'mass_fraction_of_cloud_liquid_water_in_air'
            }
# -

for _cc in cmip_models:
    for keys, var in variable.items(): 
        ### Define data location for CMIP6 file which shall be regridded
#        regrid_path = '/home/franzihe/nird_CMIP6/{}/r1i1p1f1'.format(_cc)
        regrid_path   = '/projects/NS9252K/CMIP6/historical/{}/r1i1p1f1'.format(_cc)


        for years in np.arange(1985,1986):
            ### Input data from CMIP6 model to be regridded
            cr_file = glob('{}/{}_Amon_{}_historical_r1i1p1f1_*12.nc'.format(regrid_path, keys, _cc, ))
            if len(cr_file) == 1:
                ds_in = xr.open_dataset(cr_file[0]).sel(time = slice(str(years)+'01', str(years)+'12'))
            else:
                cr_file.sort()
                ds_in = xr.open_mfdataset(cr_file).sel(time = slice(str(years)+'01', str(years)+'12'))
            
        ### Read in the regridder data (NorESM)
        cmip_file = glob('{}prsn_Amon_NorESM2-MM_historical_r1i1p1f1_*12.nc'.format(cmip_path))
        cmip_file.sort()
        ds_out = xr.open_dataset(cmip_file[0]).sel(time = slice(str(years)+'-01', str(years)+'-12'))

        ### Regrid and save to file to nc_out
#        nc_out = '/home/franzihe/nird_NS9600K/data/cmip6_hist/1deg/{}_Amon_{}_1deg_{}01_{}12.nc'.format(keys,_cc, years, years)
        nc_out = '/projects/NS9600K/franzihe/data/cmip6_hist/1deg/{}_Amon_{}_1deg_{}01_{}12.nc'.format(keys,_cc, years, years)

        fct.regrid_save_data(ds_in.drop(['time_bnds', 'lat_bnds', 'lon_bnds'] ), ds_out, nc_out)


