# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:39:08 2019

@author: yili.peng
"""

import sys
sys.path.append('E:/packages/single_factor_model')
from basic_functions import functions
from RNWS import read_df
from data_box import data_box
import numpy as np

start=20140801
end=20181019

cap=read_df(r'\\goodnight\public\个人工作记录\汤旻玮\Investment\data\Cap','cap',start=start,end=end,header=0,dat_col='cap')
low,vwap,close,volume,adjfactor,sus,md=read_df(r'\\goodnight\public\个人工作记录\汤旻玮\Investment\data\MktPrice','mkt'
                                        ,start=start,end=end,header=0,dat_col=['low','vwap','close','volume','adjfactor','susp_days','maxupordown'])
ind1=read_df(r'\\goodnight\Public\个人工作记录\彭一立\Stock\stock_data\CH_2011\Industry_num','ind',start=start,end=end,header=0,dat_col='level1')
ind_weight=read_df(r'\\goodnight\Public\个人工作记录\彭一立\Stock\stock_data\CH_2011\ZZ800_weight','Stk_ZZ800',dat_col=3,inx_col=1,start=start,end=end)

vwap=vwap.replace('None',np.nan).astype(float)
ind_weight=ind_weight.replace('None',np.nan).astype(float)

A4=functions.rank(low) # -0.66
#A5=functions.ts_std(close,-2.95) # -0.33
#A9=functions.ts_rank2(volume,-4.9) #  -0.79
#A11=functions.ts_product(volume,0.43759) # -5.72
#A15=functions.ts_rank(A4,-1.87) # -3.03
A26=functions.ts_std(A4,6.8)

db=data_box()\
    .set_lag(freq='d',day_lag=0)\
    .load_adjPrice(vwap*adjfactor)\
    .load_indestry(ind1)\
    .load_indexWeight(ind_weight)\
    .load_suspend(sus.ne(0)|md.ne(0))\
    .calc_indweight()\
    .add_factor('A4',A4)\
    .add_factor('A26',A26)\
    .align_data()

V,T=run_back_test(db,n=5,back_end='loky',n_jobs=3,double_side_cost=0.003
              ,weight_path=r'E:\packages\single_factor_model\detail.csv'
              ,verbose=40,temp_folder=r'E:\packages\single_factor_model\tmp')

import pandas as pd
D=pd.read_csv(r'E:\packages\single_factor_model\test\detail.csv',parse_dates=['dt'],infer_datetime_format=True)
