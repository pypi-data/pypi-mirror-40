This programme is built for back-testing factors.

Dependencies
------------

-  python 3.5
-  pandas 0.23.0
-  numba 0.38.0
-  empyrical 0.5.0
-  data_box
-  pickle
-  multiprocessing

Example
-------

Data Box: pre-process
=====================

.. code:: bash

   from data_box import data_box
   db=data_box()\
       .load_indestry(ind)\
       .load_indexWeight(ind_weight)\
       .calc_indweight()\
       .load_suspend(sus)\
       .load_adjPrice(price)\
       .add_factor('factor0',factor0)\
       .add_factor('factor1',factor1)\
       .set_lag(freq='d',day_lag=1)\
       .align_data()
   # freq can be 'd' or 'm', for detail please refer to db.set_lag doc. 

Where ``price,ind,ind_weight,sus,factor0,factor1`` are all dataframes
with index as date (yyyymmdd,int) and column as tickers. You can save
and load this data box object by ``db.save('path')`` and
``db.load('path')``. You can find more in data_box project.

Back Test
=========

.. code:: bash

   from single_factor_model import run_back_test

single process

.. code:: bash

   Value,Turnover=run_back_test(data_box=db,back_end=None,n=5,weight_path=None,double_side_cost=0.003)

multi process

.. code:: bash

   Value,Turnover=run_back_test(data_box=db,back_end='loky',n=5,weight_path=None,verbose=50)

or

.. code:: bash

   with __name__=='__main__':
       Value,Turnover=run_back_test(data_box=db,back_end='multiprocessing',n=5,weight_path=None)

To check detailed position of each portfolio each day, just assign
``weight_path``.

Summary and Plot
================

calculate return including long short portfolio(and reverse)

.. code:: bash

   from single_factor_model import calc_return
   Return = calc_return(Value,Turnover,long_short,double_side_cost=0.003)

summary

.. code:: bash

   from single_factor_model import summary
   S=summary(Return)

plot

.. code:: bash

   run_plot(Return,show=True)


