# -*- coding: utf-8 -*-
"""
Created on Mon May 21 09:56:57 2018

@author: MichaelEK
"""
import statsmodels as sm
import numpy as np
import pandas as pd
from pdsql import mssql
import os
import geopandas as gpd
from shapely.geometry import Point
from hydrolm.lm import LM
import matplotlib.pyplot as plt
from gistools.vector import sel_sites_poly

pd.options.display.max_columns = 10


############################################
### Parameters

server = 'sql2012test01'
database = 'hydro'
ts_daily_table = 'TSDataNumericDaily'
ts_hourly_table = 'TSDataNumericHourly'
ts_summ_table = 'TSDataNumericDailySumm'
sites_table = 'ExternalSite'

recent_date = '2018-01-01'
min_date = '2000-01-01'
end_date = '2018-06-30'
min_count = 8
search_dis = 50000

dep_loss = 0.04
nobs_loss = 0.002

rec_datasets = [5, 1521, 4503, 4515]
man_datasets = [8, 1637, 4558, 4564, 4570]

qual_codes = [200, 400, 500, 520, 600]

############################################
### Extract summary data and determine the appropriate sites to use

rec_summ_data = mssql.rd_sql(server, database, ts_summ_table, where_col={'DatasetTypeID': rec_datasets})
rec_summ_data.FromDate = pd.to_datetime(rec_summ_data.FromDate)
rec_summ_data.ToDate = pd.to_datetime(rec_summ_data.ToDate)

rec_sites = rec_summ_data[(rec_summ_data.ToDate > recent_date)]

x_sites = rec_sites[rec_sites.Count > 19000].copy()

y_sites = rec_sites[rec_sites.Count < 2500].copy()


#man_summ_data = mssql.rd_sql(server, database, ts_summ_table, where_col={'DatasetTypeID': man_datasets})
#man_summ_data.FromDate = pd.to_datetime(man_summ_data.FromDate)
#man_summ_data.ToDate = pd.to_datetime(man_summ_data.ToDate)

## Get a full list of sites to retrieve site data for

all_sites = set(x_sites.ExtSiteID.tolist())
all_sites.update(y_sites.ExtSiteID.tolist())

###########################################
### Get site data

site_xy = mssql.rd_sql(server, database, sites_table, ['ExtSiteID', 'ExtSiteName', 'NZTMX', 'NZTMY'], where_col={'ExtSiteID': list(all_sites)})

geometry = [Point(xy) for xy in zip(site_xy['NZTMX'], site_xy['NZTMY'])]
site_xy1 = gpd.GeoDataFrame(site_xy['ExtSiteID'], geometry=geometry, crs=2193)

y_xy = site_xy1[site_xy1.ExtSiteID.isin(y_sites.ExtSiteID)].set_index('ExtSiteID').copy()
x_xy = site_xy1[site_xy1.ExtSiteID.isin(x_sites.ExtSiteID)].set_index('ExtSiteID').copy()

###########################################
### Iterate through the low flow sites


## Extract all ts data
y_data = mssql.rd_sql(server, database, ts_daily_table, ['ExtSiteID', 'DateTime', 'Value'], where_col={'DatasetTypeID': rec_datasets, 'ExtSiteID': y_sites.ExtSiteID.tolist(), 'QualityCode': qual_codes}, to_date=end_date, date_col='DateTime')
y_data.DateTime = pd.to_datetime(y_data.DateTime)
y_data.loc[y_data.Value <= 0, 'Value'] = np.nan

x_data = mssql.rd_sql(server, database, ts_daily_table, ['ExtSiteID', 'DateTime', 'Value'], where_col={'DatasetTypeID': rec_datasets, 'ExtSiteID': x_sites.ExtSiteID.tolist(), 'QualityCode': qual_codes}, to_date=end_date, date_col='DateTime')
x_data.DateTime = pd.to_datetime(x_data.DateTime)
x_data.loc[x_data.Value <= 0, 'Value'] = np.nan


## Re-organise the datasets
x_data1 = x_data.pivot_table('Value', 'DateTime', 'ExtSiteID')
y_data1 = y_data.pivot_table('Value', 'DateTime', 'ExtSiteID')

### Autocorrelation
#
#def autocorr(df, limit=0.05, nlags=400):
#    auto_dict = {}
#    for name, values in df.iteritems():
#        a1 = sm.tsa.stattools.acf(values, nlags=nlags, fft=True, missing='drop')
#        days = np.argmax(a1 < limit)
#        auto_dict.update({name: days})
#    return auto_dict
#
#x_auto_dict = autocorr(x_data1, 0.05)
#
#y_auto_dict = autocorr(y_data1)
#
#pd.plotting.autocorrelation_plot(y_data1['69520'].dropna())
#pd.plotting.autocorrelation_plot(x_data1['65104'].dropna())

## regressions!
lm1 = LM(x_data1, y_data1)

ols1_log1 = lm1.predict('ols', 2, x_transform='log', y_transform='log', min_obs=min_count, autocorr=0.1)

ols1_log2 = lm1.predict('ols', 1, x_transform='log', y_transform='log', min_obs=min_count, autocorr=None)

ols1_log3 = lm1.predict('ols', 1, x_transform='log', y_transform='log', min_obs=min_count, autocorr=0.05)


##################################################
### Testing




