# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:13:02 2018

@author: yili.peng
"""
from .utilise import pre_sus,change_index,monthmove,check_time
from datetime import datetime
import pandas as pd
from pandas.api.types import is_numeric_dtype
from functools import reduce
import pickle
import numpy as np

class ci_transformer:
    def __init__(self):
        self.columns=None
        self.index=None
    def fit_columns(self,*args):
        a=list(reduce(lambda x,y: set(x)&set(y),[i.columns for i in args]))
        a.sort()
        self.columns=a
    def fit_index(self,*args):
        a=list(reduce(lambda x,y: set(x)&set(y),[i.index for i in args]))
        a.sort()
        self.index=a
    def fit(self,*args):
        self.fit_columns(*args)
        self.fit_index(*args)
    def transform_columns(self,*args):
        return [a.reindex(columns=self.columns) for a in args]
    def transform_index(self,*args):
        return [a.reindex(index=self.index) for a in args]
    def transform(self,*args):
        return [a.reindex(index=self.index,columns=self.columns) for a in args]


class data_box(object):
    def __init__(self):
        self._factorDF=None
        self._freq='d'
        self._day_lag=0
        self._period_lag=0
        self._fixed_date=None
        self._start_time=None
        self._end_time=None
        
        self._Factors={}
        self._suspend=None
        self._price=None
        self._industry=None
        self._industry_weight=None
        self._index_weight=None
        self._factorDF=None

    @property
    def Price(self):
        assert self._price is not None,'Load Price first'
        return self._price.loc[self._start_time:self._end_time]
    @property
    def Sus(self):
        assert self._suspend is not None,'Load Suspend first'
        return self._suspend.loc[self._start_time:self._end_time]
    @property
    def Ind(self):
        assert self._industry is not None,'Load Industry first'
        return self._industry.loc[self._start_time:self._end_time]
    @property
    def Ind_weight(self):
        assert self._industry_weight  is not None,'Load IndexWeight and compile first'
        return self._industry_weight.loc[self._start_time:self._end_time]
    @property
    def Index_weight(self):
        assert self._index_weight is not None,'Load IndexWeight first'
        return self._index_weight
    @property
    def Factor(self):
        if self._factorDF is None:
            assert len(self._Factors) is not 0,'Load Factor first'
            return pd.concat(self._Factors.values(),axis=1,keys=self._Factors.keys()).loc[self._start_time:self._end_time]
        else:
            return self._factorDF.loc[self._start_time:self._end_time]
        
    def set_lag(self,freq='d',period_lag=0,day_lag=0,fixed_date=None,**kwargs):
        '''
        freq: 'd'/'m' daily or monthly
        day_lag: int
            Lags between the factor exposure date (T) and the factor exposure calculated date (T+n).
            lag = 0 means factor can be used T+1 
        period_lag: int
            Lags between the factor exposure period (T) and the factor exposure calculated period (T+n)
            For freq='d', period_lag and  day_lag are the same, the max of these two would be used.
            But for freq='m', total lag is the plus of day_lag and period_lag
        fixed_date: int
            Fixed calulate date when freq = 'm', combined with period_lag and day_lag if set.
        '''
        
        assert freq.lower() in ('d','m'), 'freq must in "d" / "m"'
        assert (fixed_date is None) or (type(fixed_date) is int), 'fixed_date must be None or int'
        
        self._freq=freq
        if freq is 'd':
            self._day_lag=self._period_lag=max(period_lag,day_lag)
        else:
            self._day_lag=day_lag
            self._period_lag=period_lag
            self._fixed_date=fixed_date
        return self
    def set_time(self,start_time=None,end_time=None,**kwargs):
        '''  
        set time span
        '''
        self._start_time=(datetime.strptime(str(start_time),'%Y%m%d') if start_time is not None else None)
        self._end_time=(datetime.strptime(str(end_time),'%Y%m%d') if end_time is not None else None)
        return self
    def add_factor(self,factor_name,factor_df,change_index_to_date=True,factor_pool=None,**kwargs):
        '''
        factor_name: str
        factor_df: DataFrame (times*tickers). Monthly factor should be have only one index each month
        factor_pool: Pool of factors to be included. Default None (all)
        '''
        if (factor_pool is None) or (factor_name in factor_pool):
            assert factor_df.apply(is_numeric_dtype).all(), 'Factor DataFrame contains Non-numeric type'
            
            
            self._Factors[factor_name]=(change_index(factor_df) if change_index_to_date else factor_df)
        return self
    def load_adjPrice(self,price_df,change_index_to_date=True,**kwargs):
        
        assert price_df.apply(is_numeric_dtype).all(), 'Open DataFrame contains Non-numeric type'
        self._price=(change_index(price_df) if change_index_to_date else price_df)
        return self
    def load_suspend(self,suspend_df,change_index_to_date=True,**kwargs):
        
        assert suspend_df.apply(is_numeric_dtype).all(), 'Suspend DataFrame contains Non-numeric type'
        suspend_df2=suspend_df.astype(int).apply(pre_sus)
        self._suspend=(change_index(suspend_df2) if change_index_to_date else suspend_df2)
        return self
    def load_indestry(self,industry_df,change_index_to_date=True,mapping=False,**kwarg):
        
        if mapping:
            stacked=industry_df.stack()
            lst=stacked.unique()
            mapping=pd.Series(range(len(lst)),index=lst)
            industry_df=pd.Series(mapping.reindex(stacked).values,index=stacked.index).unstack()
            
        assert industry_df.apply(is_numeric_dtype).all(), 'Industry DataFrame contains Non-numeric type'
        self._industry = (change_index(industry_df) if change_index_to_date else industry_df)
        return self
    def load_indexWeight(self,index_weight_df,change_index_to_date=True):
        
        assert index_weight_df.apply(is_numeric_dtype).all(), 'Index Weight DataFrame contains Non-numeric type'
        self._index_weight = (change_index(index_weight_df) if change_index_to_date else index_weight_df)
        return self
    def compile_data(self):
        '''
        This process would align tickers and time for all data.
        '''
        CI=ci_transformer()
        #columns
        CI.fit_columns(self._industry,self._suspend,self._price,self.Factor.stack(dropna=False,level=0))
        self._industry,self._suspend,self._price,factors =  CI.transform_columns(self._industry,self._suspend,self._price,self.Factor.stack(dropna=False,level=0))
        
        if self._freq=='d':
            # daily
            CI.fit_index(self._industry,self._suspend,self._price,self._index_weight)
            # transform
            self._industry,self._suspend,self._price,self._index_weight,factors2 = CI.transform_index(self._industry,self._suspend,self._price,self._index_weight,factors.unstack())
            self._industry_weight=pd.concat([self._index_weight,self._industry],axis=1,keys=['weight','ind']).stack(dropna=False).fillna(0).groupby(['dt','ind']).aggregate(sum)['weight'].unstack()
            
            self._factorDF=factors2.shift(self._day_lag)\
                                    .swaplevel(axis=1)\
                                    .sort_index(axis=1)
            # clean
            factors=factors2=None
            
        elif self._freq=='m':
            # monthly
            # Monthly factor should be have only one index each month
            
            CI.fit_index(self._industry,self._suspend,self._price,self._index_weight)
            trading_calendar=CI.index
            factors2=factors.unstack().shift(self._period_lag)
            lst = [int(i.strftime('%Y%m%d')[:6]) for i in factors2.index] # original index
            
            assert len(set(lst)) == len(lst), 'Monthly factor have a invalid frequency'
                       
            if self._fixed_date is None:
                # no fixed date
                
                # change index                           
                new_index=pd.DataFrame([[i,int(i.strftime('%Y%m%d')[:6])] for i in trading_calendar],columns=['dt','ym'])\
                                .groupby('ym').agg({'dt':max})['dt']\
                                .reindex(lst).values
                factors3=factors2.assign(dt=new_index)\
                        .loc[~pd.Series(new_index).isna().values]\
                        .set_index('dt')

            else:
                # fixed date
                target_lst=[check_time(monthmove(l)+str(self._fixed_date).zfill(2)) for l in lst]
                new_index=[pd.Series(trading_calendar).loc[pd.Series(trading_calendar).le(l)].max() for l in target_lst]
                factors3=factors2.assign(dt=new_index)\
                        .loc[~pd.Series(new_index).eq(pd.Series(new_index).shift()).values]\
                        .set_index('dt')

            # transform
            self._industry,self._suspend,self._price,self._index_weight,factors4 = CI.transform_index(self._industry,self._suspend,self._price,self._index_weight,factors3)
            self._industry_weight=pd.concat([self._index_weight,self._industry],axis=1,keys=['weight','ind']).stack(dropna=False).fillna(0).groupby(['dt','ind']).aggregate(sum)['weight'].unstack()
            self._factorDF=factors4.shift(self._day_lag)\
                                    .swaplevel(axis=1)\
                                    .sort_index(axis=1)

            # clean
            factors=factors2=factors3=factors4=None
        return self
    def clean_factor(self):
        self._factorDF=None
        self._Factors={}
        return self
    def save(self,path):
        with open(path,'wb') as f:
            f.write(pickle.dumps(self.__dict__))
        return self
    def load(self,path):
        with open(path,'rb') as f:
            dataPickle = f.read()
        self.__dict__=pickle.loads(dataPickle)
        return self

class sample_pipeline:
    '''
    method order:
        X:
            .factor_rank
            .factor_zscore
        y:
            .fw_return_ind_neutral
            .fw_return_rank
            .fw_return_I
    All returns are amplified by 100 for better model training 
    '''
    def __init__(self):
        self._fw_return_n=1
        self._sample_n=1
        self._fw_return_thresh=0
        self._factor_zscore_flag=False
        self._ind_neutral=False
        self._fw_return_I_flag=False
        self._factor_rank_flag=False
        self._fw_return_rank_flag=False
    def set_fw_return_n(self,n=1):
        '''
        set n days(months) forward return as y
        '''
        self._fw_return_n=n
        return self
    def fw_return_ind_neutral(self):
        '''
        make set return as industry neutraled returns (and reverse)
        '''
        self._ind_neutral=(self._ind_neutral is False)
        return self
    def fw_return_I(self,thresh=0):
        '''
        change fw_return as 0/1 type
        '''
        self._fw_return_I_flag=(self._fw_return_I_flag is False)
        self._fw_return_thresh=thresh
        return self
    def fw_return_rank(self):
        self._fw_return_rank_flag=(self._fw_return_rank_flag is False)
        return self
    def factor_rank(self):
        self._factor_rank_flag=(self._factor_rank_flag is False)
        return self
    def factor_zscore(self):
        self._factor_zscore_flag=(self._factor_zscore_flag is False)
        return self
    def set_sample_n(self,n=1):
        '''
        use n days(months) factor as X
        '''
        self._sample_n=n
        return self
    def _trans_sample(self,sample2):
        inx_lst=[]
        spl_lst=[]
        for i in range(self._sample_n,sample2.shape[0]+1):
            sub_sample=sample2.iloc[i-self._sample_n:i]
            inx_lst.append(sub_sample.index[-1])
            sub_sample.index=('day_{}'.format(len(sub_sample.index)-i) for i in range(len(sub_sample.index)))
            spl_lst.append(sub_sample.stack(dropna=True))
        all_sample=pd.concat(spl_lst,keys=inx_lst,axis=0).rename_axis(['dt','days','ticker'])
        return all_sample
    def train_set(self,databox):
        '''
        transform a databox to samples that can be fed into models directly (for train)
        
        sample at t0 
        ---------------------------------------------------------------------------------------------------
              day       |      factors (a.k.a. X)       |              fw_return (a.k.a y) * 100           
        ---------------------------------------------------------------------------------------------------
             day_1      |   f_{t0-fw_return_n-1}        |     price_t0/price_{t0-fw_return_n} - 1
        ---------------------------------------------------------------------------------------------------
             day_2      |   f_{t0-fw_return_n-2}        | price_{t0-1}/price_{t0-fw_return_n-1} - 1
        ---------------------------------------------------------------------------------------------------
                                    ......
        ---------------------------------------------------------------------------------------------------
          day_sample_n  |   f_{t0-fw_return_n-sample_n}  | price_{t0-sample_n+1}/price_{t0-fw_return_n-sample_n+1} - 1
        ---------------------------------------------------------------------------------------------------
        '''
        assert databox.Price.shape[0]>=self._fw_return_n+self._sample_n, 'databox period is not enough'
        fw_return=databox.Price.pct_change(periods=self._fw_return_n).stack().rename('fw_return').mul(100)
        if self._ind_neutral:
            fw_return_ind=pd.concat([fw_return,databox.Ind.stack().rename('ind')],axis=1)
            fw_return-=fw_return_ind.groupby(['dt','ind']).fw_return.transform(np.mean)
        sample=databox.Factor.shift(self._fw_return_n+1).stack()
        sample['fw_return']=fw_return.reindex(sample.index).values
        sample2=sample.unstack()
        all_sample=self._trans_sample(sample2)\
                        .dropna()
        X,y=all_sample.drop('fw_return',axis=1),all_sample['fw_return']
        if self._factor_rank_flag:
            X=X.groupby('dt').rank(method='min')
        if self._factor_zscore_flag:
            X=(X-X.groupby('dt').transform(np.mean))/X.groupby('dt').transform(np.std)
            
        if self._fw_return_rank_flag:
            y=y.groupby('dt').rank(method='min')
        if self._fw_return_I_flag:
            y=y.ge(self._fw_return_thresh).astype(int)
        return X,y
    def test_set(self,databox):
        '''
        transform a databox to samples that can be fed into models directly (for test)
        
        sample at t0
        --------------------------------------------------------------------------------
              factors (a.k.a. X)    |               fw_return (a.k.a y)  * 100  
        --------------------------------------------------------------------------------
                     f_t0           |    price_{t0+fw_return_n+1}/price_{t0+1} - 1
        --------------------------------------------------------------------------------
        '''
        assert databox.Price.shape[0]>=self._fw_return_n+self._sample_n, 'databox period is not enough'
        
        fw_return=databox.Price.pct_change(periods=self._fw_return_n).shift(-(1+self._fw_return_n)).stack().rename('fw_return').mul(100)
        if self._ind_neutral:
            fw_return_ind=pd.concat([fw_return,databox.Ind.stack().rename('ind')],axis=1)
            fw_return-=fw_return_ind.groupby(['dt','ind']).fw_return.transform(np.mean)
        sample=databox.Factor.stack()
        sample['fw_return']=fw_return.reindex(sample.index).values
        sample2=sample.unstack()
        all_sample=self._trans_sample(sample2)\
                        .dropna()
        X,y=all_sample.drop('fw_return',axis=1),all_sample['fw_return']
        if self._factor_rank_flag:
            X=X.groupby('dt').rank(method='min')
        if self._factor_zscore_flag:
            X=(X-X.groupby('dt').transform(np.mean))/X.groupby('dt').transform(np.std)
            
        if self._fw_return_rank_flag:
            y=y.groupby('dt').rank(method='min')
        if self._fw_return_I_flag:
            y=y.ge(self._fw_return_thresh).astype(int)        
        return X.xs('day_1',level=1),y.xs('day_1',level=1)
    def test_X(self,databox):
        '''
        transform a databox to samples that can be fed into models directly (for X and make new factor)
        
        sample at t0
        -------------------------------
              factors (a.k.a. X)
        -------------------------------
                     f_t0
        -------------------------------
        '''
        assert databox.Price.shape[0]>=self._sample_n, 'databox period is not enough'
        X=self._trans_sample(databox.Factor).dropna()
        if self._factor_rank_flag:
            X=X.groupby('dt').rank(method='min')
        if self._factor_zscore_flag:
            X=(X-X.groupby('dt').transform(np.mean))/X.groupby('dt').transform(np.std)
        return X.xs('day_1',level=1)
