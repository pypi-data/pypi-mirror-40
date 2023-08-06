# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:13:02 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np

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
        fw_return=databox.Price.mask(databox.Sus.eq(1)).pct_change(periods=self._fw_return_n).stack().rename('fw_return').mul(100)
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
            X=(X-X.groupby('dt').transform(np.mean))/X.groupby('dt').transform(np.std,ddof=1)
            
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
        
        fw_return=databox.Price.mask(databox.Sus.eq(1)).pct_change(periods=self._fw_return_n).shift(-(1+self._fw_return_n)).stack().rename('fw_return').mul(100)
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
            X=(X-X.groupby('dt').transform(np.mean))/X.groupby('dt').transform(np.std,ddof=1)
            
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
