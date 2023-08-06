This programme is used for statistical arbitrage with co integation
method

Dependencies
~~~~~~~~~~~~

-  python 3.5
-  pandas 0.22.0
-  spyder 3.2.8
-  joblib 0.12.3
-  RNWS 0.1.2
-  mini_exchange 0.0.7

Sample
~~~~~~

Back Test
---------

Calculate p_value of stationarity among all pairs along all history

.. code:: bash

   import pandas as pd
   from CointArbitrage.pairing_period import find_pair,filter_tickers

   price=pd.read('price.csv') # index:yyyymmdd(int),columns:tickers,values:adjusted price

   past_date=60 # use last 60 days to calculate p_value
   P=[]
   for i in range(past_date,price.shape[0]):
       # filter unavailable tickers, this step is optional
       df=filter_tickers(price.iloc[(i-past_date):i])
       # calculate p_value
       des=find_pair(df,mul=True,n_jobs=-1)
       dt=filter_tickers.index[i]
       P.append(pd.Series(des.p_value.values,index=des['ticker1'].str.cat(des['ticker2'],'|').values,name=dt))
   pairs=pd.concat(P,axis=1).T    

Make signal dataframe

.. code:: bash

   from CointArbitrage.trading_period import zscore_log_w,zscore_w,sig,sig_cut_tail
   window=20 # use 20 days to calculate zscore ( = normalize(stockPrice1/stockPrice2))
   ratio,zs=zscore_w(price_df=price,pair_lst=pairs.columns,window=window)
   # or use log zscore = normalize(log(stockPrice1/stockPrice2))
   ratio,zs=zscore_log_w(price_df=price,pair_lst=pairs.columns,window=window)
   # or use exponential moving to calculate zscore with function zscore_df and zscore_log_df

   # generate signal
   # k0: close position, int, float or pd.Series if need to specify different values for each pairs
   # k1: open position
   # k2: close out position
   k0,k1,k2=1,2,4
   sig_df=sig(zscore=zs,k0=k0,k1=k1,k2=k2)
   # sig_df contains value Nan,-3,-2,-1,0,1,2,3 
   # 3(-3) means close position and open another position in different direction
   # 2(-2) means close position
   # 1(-1) means open position
   # keep signal when stationary (i.e. p_val<0.1), others would be kept in Nan
   # and add a new signal 4(-4), which means reaching the end of stationarity period
   sig_result=sig_cut_tail(sig_df,pairs<0.1,n_jobs=-1,new_signal=4)

Simulate trade

::

   from CointArbitrage.trading_period import Trade
   start=20140101
   end=20180101
   TT=Trade(price,start=start,end=end)
   user_name='user01'
   TT.add_user(user_name,sig_result,start_amount=1000)
   # add signal 4 as close signal 
   # and leave close status as -1 (default close status is 0)
   # more reference can be found in mini_exchange package
   TT.add_close_signal(4,close_status=-1)
   TT.add_close_signal(-4,close_status=-1)
   # trade 10 dollars when opening position each time
   uad=pd.DataFrame({'user_name':[user_name],'amt_type':0,'value':10})
   TT.trade(uad)
   print(TT.summary())
   # to analysis in detail, get the account info and position info of user01
   account,position=TT.get_user(user_name)
   # more details can be found in mini_exchange package
   account.plot_history(by_pct=True)
   account.annual_return()
   account.draw_down()
   account.romad()
   position.win_rate(dual=True)
   position.log
   # plot one pair
   pair='0001.HK|0002.HK'
   TT.plot_trade_pair(user_name,pair,k0=k0,k1=k1,k2=k2,window=window)

Instant simulation in HK market with Wind Api
---------------------------------------------

Find New Pair

.. code:: bash

   # initialize
   from CointArbitrage.instant_with_wind import init_log
   init_log('log.csv')

   # last t trading days
   from WindPy import w
   from CointArbitrage.instant_with_wind import trading_times
   w.start()
   times=trading_times(w,length=60,text="TradingCalendar=HKEX")

   # download adjusted close price up to yesterday
   # price is kept in file price_yyyymmdd.csv with eachline as 'tickers,values'
   # more can be found in RNWS package
   from CointArbitrage.instant_with_wind import download_hist_price
   tickers=['0001.HK','0002.HK','0003.HK'...]
   download_hist_price(tickers,times,'price_path',w)

   # read in history price
   from RNWS import read_df
   hist_price=read_df('price_path',file_pattern='price',dt_range=times)

   # filter stationary pairs
   from CointArbitrage.pairing_period import filter_pval
   import pandas as pd
   pairs=['0001.HK|0002.HK','0001.HK|0003.HK',...]
   new_pairs=filter_pval(hist_price,pairs,n_jobs=-1)
   new_tickers=pd.Series(new_pairs).str.split('|',expand=True).unstack().unique().tolist()
   new_hist=hist_price[new_tickers]

   # lotsize and shortability
   ls=pd.DataFrame({'shortable':[0,0,1,...],'lotsize':[500,1000,500,...]},index=['0001.HK','0002.HK','0003.HK'...])

   # find new pairs
   from CointArbitrage.instant_with_wind import find_new_hk
   params={'log_path':'log.csv'
           ,'hist_price':hist_price
           ,'hist_log': pd.read_csv('history_log.csv') #from back test
           ,'pairs':new_pairs
           ,'tickers':new_tickers
           ,'zs_window':20
           ,'zs_log':False 
           ,'w':w
           ,'ls':ls
           ,'potential_path':'potential_path.csv'
           ,'potential_k':1.8
           ,'k0':1
           ,'k1':2
           ,'k1':4
           ,'match_max':50000
           }

   # update log.csv
   sign=find_new_hk(**params)

update file every 1800s at trading hour and refresh evrey 900s at lunch
break and before trading start

.. code:: bash

   from CointArbitrage.instant_with_wind import time_sleep
   time_sleep(sign={0:1800,1:900,2:'break',3:'break'})(find_new_hk)(**params)

Refresh log and check close status

.. code:: bash

   params2={}
   for key in ['log_path','hist_price','w','hist_log','k0','k2','plot_mark','potential_path','zs_log','zs_window']:
       params2.update(params[key])
   refresh_hk(**params2)
   # to continue refresh every 1800s
   time_sleep(sign={0:1800,1:900,2:'break',3:'break'})(refresh_hk)(**params2)

Check stationarity by using the price at last 10min of all trading hours

.. code:: bash

   param3={}
   for key in ['log_path','hist_price','w','zs_window','zs_log','k0','k1']
       param3.update(key)
   time_sleep(sign={0:10,1:9000,2:'break',3:'break'})(last_hk)(**param3)

Notice: After using time_sleep, sleep loops will start directly. Thus
``find_new``, ``refresh`` and ``last`` should be running in 3 different
consules.


