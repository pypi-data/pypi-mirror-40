# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 09:52:41 2018

@author: yili.peng
"""
import pandas as pd
from sklearn.metrics import roc_auc_score,accuracy_score,r2_score,mean_squared_error

def evaluate(y_true,y_score,delta_n=100,top_thresh=None,bot_thresh=None,delta_quantile=None):
    '''
    y_train: pd.Series (0/1 or float)
    y_score: pd.Series (float)
    delta_n: top/bottom number
    top_thresh: threhold to mark as top (None or (0 ~ 1))
    bot_thresh: threhold to mark as bottom (None or (0 ~ 1))
    delta_quantile: set quantile as thresh hold (None or (0 ~ 1))
    return:
        -- if y_true in (0,1)
            *auc
            *accuracy
            *top win rate
            *bench win rate
            *bottom win rate
        -- if y_true is float
            *mse 
            *r2
            *top mean return
            *bench mean return
            *bottom mean return
    '''
    if delta_quantile is not None:
        if delta_quantile < 0.5:
            bot_thresh,top_thresh = y_score.quantile(delta_quantile),y_score.quantile(1-delta_quantile)
        else:
            top_thresh,bot_thresh = y_score.quantile(delta_quantile),y_score.quantile(1-delta_quantile)
    top=y_score.nlargest(delta_n).index.tolist() if top_thresh is None else y_score.index[y_score.ge(top_thresh)].tolist()
    bot=y_score.nsmallest(delta_n).index.tolist() if bot_thresh is None else y_score.index[y_score.le(bot_thresh)].tolist()

    if len(set(y_true)) <= 2:        
        auc=roc_auc_score(y_true=y_true.values,y_score=y_score.values)
        acc=accuracy_score(y_true=y_true.values,y_pred=y_score.ge(0).astype(int).values)
        top_win=y_true.loc[top].mean()
        ben_win=y_true.mean()
        bot_win=y_true.loc[bot].mean()
        return pd.Series((auc,acc,top_win,ben_win,bot_win),index=('auc','acc','top_win','bench_win','bottom_win'))
    else:
        mse=mean_squared_error(y_true=y_true,y_pred=y_score)
        r2=r2_score(y_true=y_true,y_pred=y_score)        
        top_ret=y_true.loc[top].mean()
        ben_ret=y_true.mean()
        bot_ret=y_true.loc[bot].mean()       
        return pd.Series((mse,r2,top_ret,ben_ret,bot_ret),index=('mse','r2','top_ret','bench_ret','bottom_ret'))
