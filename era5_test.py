import climtas.nci
import xarray as xr
import numpy as np
import pandas as pd
import glob

def preprocessing(ds):
    # Preprocess to extract the required data
    ds = ds.sel(time = slice('2010-01-01', '2022-08-01'), longitude = slice(-180, 180), latitude = slice(75, -65))
    # Resample to daily via averaging
    ds = ds.resample(time = '1D').mean('time')
    #ds = ds.resample(time = '1D').mean('time', keepdims=True)
    return ds


if __name__ == '__main__':
    c = climtas.nci.GadiClient()

    path_era5_daily = '/g/data/rt52/era5/single-levels/reanalysis/'
    #variables = ['mtpr', 'mn2t', 'mx2t', '10fg']
    variables = ['mx2t']

    data = {}
    for v in variables:
        print('Opening: '+v)
        listv = np.sort(glob.glob(path_era5_daily+v+'/20*/*.nc'))
        data[v] = xr.open_mfdataset(listv, chunks = {'time': -1})
        print('Opened')

    data_process = {}
    for i in data:
        print('Processing: '+i)
        data_process[i] = preprocessing(data[i])
        print('Processed')

    comp = dict(zlib=True, complevel=5)
    encoding = {var: comp for var in data_process['mx2t'].data_vars}

    data_process['mx2t'].to_netcdf('/g/data/w40/sg7549/ERA5_stuff/max_temp_mx2t.nc')