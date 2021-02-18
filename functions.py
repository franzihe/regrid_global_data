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

from imports import (xr, glob, os, xe)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def rename_coords_lon_lat(ds):
    for k in ds.indexes.keys():
        if k == 'longitude':
            ds = ds.rename({'longitude':'lon'})
        if k == 'latitude':
            ds = ds.rename({'latitude':'lat'})
            
    return(ds)


def regrid_save_data(ds_in, ds_out, nc_out,):
    
    ds_in = rename_coords_lon_lat(ds_in)
    
    ### Regridder data
    regridder = xe.Regridder(ds_in, ds_out, 'bilinear')
    regridder.clean_weight_file()
    regridder

    ### Apply regridder to data
    # the entire dataset can be processed at once
    ds_in_regrid = regridder(ds_in)

    # verify that the result is the same as regridding each variable one-by-one
    for k in ds_in.data_vars:
        print(k, ds_in_regrid[k].equals(regridder(ds_in[k])))

        if ds_in_regrid[k].equals(regridder(ds_in[k])) == True:
            ### Assign attributes from the original file to the regridded data
          #  ds_in_regrid.attrs['Conventions'] = ds_in.attrs['Conventions']
           # ds_in_regrid.attrs['history']     = ds_in.attrs['history']
            ds_in_regrid.attrs = ds_in.attrs
            
            ds_in_regrid[k].attrs['units']         = ds_in[k].attrs['units']
            ds_in_regrid[k].attrs['long_name']     = ds_in[k].attrs['long_name']
            try:
                ds_in_regrid[k].attrs['standard_name'] = ds_in[k].attrs['standard_name']
                ds_in_regrid[k].attrs['comment']       = ds_in[k].attrs['comment']
                ds_in_regrid[k].attrs['original_name'] = ds_in[k].attrs['original_name']
                ds_in_regrid[k].attrs['cell_methods']  = ds_in[k].attrs['cell_methods']
                ds_in_regrid[k].attrs['cell_measures'] = ds_in[k].attrs['cell_measures']
            except KeyError:
                continue
    
    ### Save to netcdf file
    
    ds_in_regrid.to_netcdf(nc_out)
    ds_in_regrid.close(); ds_in.close(); ds_out.close()
    print('file written: .{}'.format(nc_out[29:]))


