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

# ## Download NorESM reference grid
#
# for INP special issue: nird/projects/NS9600K/shofer/Rob/INP_base_new/atm/hist in h2 file
#

# +
# supress warnings
import warnings
warnings.filterwarnings('ignore') # don't output warnings

from imports import (xr)

# reload imports
# %load_ext autoreload
# %autoreload 2
# -

noresm_file = '/home/franzihe/nird_NS9600K/shofer/Rob/INP_base_new/atm/hist/INP_base.cam.h2.2008-10-01-00000.nc'
out_file = './NorESM_2.5deg.nc'

fnx = xr.open_dataset(noresm_file)

# create dataset
ds = xr.Dataset({
    'lat': xr.DataArray(
                data   = fnx.lat.values,   # enter data here
                dims   = ['lat', ],
                ),
    'lon': xr.DataArray(
                data   = fnx.lon.values,   # enter data here
                dims   = ['lon', ],
                 ),
            },
        attrs = {'NorESM grid': 'taken from NorESM file'}
    )

ds.to_netcdf(path=out_file, mode='w', format="NETCDF4", )


