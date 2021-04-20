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
# -

available_month = {
                   '01':['01'],
                   '02':['02'],
                   '03':['03'],
                   '04':['04'], 
                   '05':['05'], 
                   '06':['06'], 
                   '07':['07'],
                   '08':['08'], 
                   '09':['09'], 
                   '10':['10'], 
                   '11':['11'], 
                   '12':['12']
                  }

available_years = {
                   "07": ['2007',],
                   "08": ['2008',],
                   "09": ['2009',],
                   "10": ['2010',],
                    }

# +

### Data location for file of reference grid
#cmip_path   = '/home/franzihe/Documents/Python/regrid_global_data/'
cmip_path   = './'#../../regrid_global_data/'

variable = {
            'tp' :'total_precipitation',
            'sf' :'snowfall',                          # ERA5 single level variables
            't'   :'temperature',
            'crwc':'specific_rain_water_content',
            'cswc':'specific_snow_water_content',
            'clwc':'specific_cloud_liquid_water_content',
            'ciwc':'specific_cloud_ice_water_content'      # ERA5 pressure level variables
           }


# +
### Read in the regridder data (NorESM)
cmip_file = sorted(glob('{}NorESM_2.5deg.nc'.format(cmip_path)))[0]
ds_out = xr.open_dataset(cmip_file)

counter = 0
for keys, var in variable.items(): 
    for years in (available_years):
        ### Define data location for ERA5 and CMIP6
        era_path     = '../../../data/ERA5/3_hourly/{}'.format(available_years[years][0])
#        era_path     = '/home/franzihe/nird_NS9600K/data/ERA5/3_hourly/{}'.format(available_years[years][0])

        for months in available_month:
            nc_out = 'NorESMgrid/{}_3hourly_ERA5_{}{}.nc'.format(keys, available_years[years][0], available_month[months][0])
            files = glob('{path}/{nc_out}'.format(path = era_path, nc_out = nc_out))

            
            if '{path}/{nc_out}'.format(path = era_path, nc_out = nc_out) in files:
                print('{path}/{nc_out} regridded'.format(path = era_path, nc_out = nc_out))
                counter += 1
                print("Have regridded in total : " + str(counter) + " files")

            else:
                ### Input data from ERA5 with a resolution of 0.25x0.25 deg
                era_file = sorted(glob('{}/{}_3hourly_ERA5_{}{}_*.nc'.format(era_path, keys, available_years[years][0], available_month[months][0])))
                if len(era_file) != 2:
                    print('no files found: {}/{}_3hourly_ERA5_{}{}_*.nc'.format(era_path, keys, available_years[years][0], available_month[months][0]))
                    continue

                else:
                    ds_in_S = xr.open_dataset(era_file[0])
                    ds_in_N = xr.open_dataset(era_file[1])
                    
                    try:
                        ds_in_S.indexes['level']
                        ### assign variable name to ds_out
                        ds_out = ds_out.assign({
                            keys: xr.DataArray(
                                data   = np.full(shape = (ds_in_S.level.shape[0], ds_in_S.time.shape[0], ds_out.lat.shape[0], ds_out.lon.shape[0]) , 
                                                 fill_value = np.nan),   # enter data here
                                dims   = ['level', 'time', 'lat', 'lon'],
                                coords = {'level': ds_in_S.level, 'time': ds_in_S.time, 'lat': ds_out.lat, 'lon': ds_out.lon},
                            ),},)

                        ### regridding in each level
                        ds_in_regrid_S = fct.regrid_through_level(ds_in_S, ds_out.sel(lat = slice(-90, -30)))
                        ds_in_regrid_N = fct.regrid_through_level(ds_in_N, ds_out.sel(lat = slice(30, 90)))
                    
                    except KeyError:
                        ### assign variable name to ds_out
                        ds_out = ds_out.assign({
                            keys: xr.DataArray(
                                data   = np.full(shape = ( ds_in_S.time.shape[0], ds_out.lat.shape[0], ds_out.lon.shape[0]) , 
                                                 fill_value = np.nan),   # enter data here
                                dims   = ['time', 'lat', 'lon'],
                                coords = {'time': ds_in_S.time, 'lat': ds_out.lat, 'lon': ds_out.lon},
                            ),},)
                        ### Regridding surface variables
                        ds_in_regrid_S = fct.regrid_data(ds_in_S, ds_out.sel(lat = slice(-90, -30)))
                        ds_in_regrid_N = fct.regrid_data(ds_in_N, ds_out.sel(lat = slice(30, 90)))



                    ### concat all datasets 
                    ds = xr.concat([ds_in_regrid_S, ds_out.sel(lat = slice(-30,30)), ds_in_regrid_N], dim = 'lat')
                    ds.to_netcdf('{path}/{nc_out}'.format(path = era_path, nc_out = nc_out))

                    ds_in_S.close(); ds_in_N.close(); ds_in_regrid_S.close(), ds_in_regrid_N.close();
                    print('file written: {path}/{nc_out}'.format(path = era_path, nc_out = nc_out))
# -













# + active=""
# ### Read in the regridder data (NorESM)
# cmip_file = sorted(glob('{}NorESM_2.5deg.nc'.format(cmip_path)))[0]
# ds_out = xr.open_dataset(cmip_file)
# for keys, var in variable.items(): 
#     for years in (available_years):
#         ### Define data location for ERA5 and CMIP6
#         era_path     = '/home/franzihe/nird_NS9600K/data/ERA5/3_hourly/{}/'.format(available_years[years][0])
#
#         for months in available_month:
#
#             
#             ### Input data from ERA5 with a resolution of 0.25x0.25 deg
#             era_file = sorted(glob('{}{}_3hourly_ERA5_{}{}_*.nc'.format(era_path, keys, available_years[years][0], available_month[months][0])))
#             if len(era_file) != 2:
#                 print('no files found: {}{}_3hourly_ERA5_{}{}_*.nc'.format(era_path, keys, available_years[years][0], available_month[months][0]))
#                 continue
#             else:
#                 ds_in = xr.merge([xr.open_dataset(era_file[0]), xr.open_dataset(era_file[1])], )
#
#                 ### Regrid            
#                 ds_in_regrid = fct.regrid_data(ds_in, ds_out, )
#     
#                 ### Save to netcdf file nc_out
#                 nc_out = '{}/{}/NorESMgrid/{}_3hourly_EAR5_{}{}.nc'.format(era_file[0][:46], available_years[years][0], keys, available_years[years][0], available_month[months][0])
#                 fct.createFolder(nc_out[:-25])
#                 ds_in_regrid.to_netcdf(nc_out)
#                 ds_in_regrid.close(); ds_in.close(); 
#                 print('file written: .{}'.format(nc_out[-25:]))


# -


