# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 16:20:14 2018

@author: yili.peng
"""
from .cprint import cprint
from .evaluate import evaluate
import pandas as pd
import numpy as np

def clf_model(clf,X_train,y_train,X_test,y_test,**kwargs):
    '''
    clf: sklearn classification model
    y_train: 0/1 or real_return
    y_test: 0/1 or real_return
    '''
    dt_list=(X_train.index.levels[0] & X_test.index.levels[0]).tolist()
    
    train_lst=[]
    test_lst=[]
    model_lst=[]
    
    for dt in dt_list:
        cprint('Modeling  {}'.format(dt.strftime('%Y-%m-%d')))
        X_train_sub,y_train_sub,X_test_sub,y_test_sub=X_train.xs(dt),y_train.xs(dt),X_test.xs(dt),y_test.xs(dt)
        if len(set(y_train_sub))>2:
            clf.fit(X_train_sub.values,y_train_sub.ge(0).astype(int).values)
        else:
            clf.fit(X_train_sub.values,y_train_sub.values)
        # train
        y_train_proba = pd.Series(clf.predict_proba(X_train_sub.values)[:,1],index=X_train_sub.index,name='fw_return_proba')
        trained_eval_srs=evaluate(y_train_sub,y_train_proba,**kwargs)
        train_lst.append(trained_eval_srs.rename(dt))
        # test
        y_test_proba = pd.Series(clf.predict_proba(X_test_sub.values)[:,1],index=X_test_sub.index,name='fw_return_proba') 
        test_eval_srs=evaluate(y_test_sub,y_test_proba,**kwargs)
        test_lst.append(test_eval_srs.rename(dt))
        
        all_features=dir(clf)
        if 'feature_importances_' in all_features:
            try:
                model_lst.append(pd.Series(clf.feature_importances_,index=X_train_sub.columns,name=('feature_importances_',dt)))
            except:
                pass
        if 'coef_' in all_features:
            try:
                model_lst.append(pd.Series(clf.coef_.reshape(-1),X_train_sub.columns,name=('coef_',dt)))
            except:
                pass
    
    tn=pd.concat(train_lst,axis=1).T
    tt=pd.concat(test_lst,axis=1).T
    ml=pd.concat(model_lst,axis=1).T if len(model_lst)>0 else None
    return tn,tt,ml

def reg_model(reg,X_train,y_train,X_test,y_test,**kwargs):
    '''
    reg: sklearn regression model
    y_train: real_return
    y_test: real_return
    '''
    dt_list=(X_train.index.levels[0] & X_test.index.levels[0]).tolist()
    
    train_lst=[]
    test_lst=[]
    model_lst=[]
    
    for dt in dt_list:
        cprint('Modeling  {}'.format(dt.strftime('%Y-%m-%d')))
        X_train_sub,y_train_sub,X_test_sub,y_test_sub=X_train.xs(dt),y_train.xs(dt),X_test.xs(dt),y_test.xs(dt)
        reg.fit(X_train_sub.values,y_train_sub.values)
        # train
        y_train_hat = pd.Series(reg.predict(X_train_sub.values),index=X_train_sub.index,name='fw_return_proba')
        trained_eval_srs=evaluate(y_train_sub,y_train_hat,**kwargs)
        train_lst.append(trained_eval_srs.rename(dt))
        # test
        y_test_hat = pd.Series(reg.predict(X_test_sub.values),index=X_test_sub.index,name='fw_return_proba')
        test_eval_srs=evaluate(y_test_sub,y_test_hat,**kwargs)
        test_lst.append(test_eval_srs.rename(dt))
        
        all_features=dir(reg)
        if 'feature_importances_' in all_features:
            try:
                model_lst.append(pd.Series(reg.feature_importances_,index=X_train_sub.columns,name=('feature_importances_',dt)))
            except:
                pass            
        if 'coef_' in all_features:
            try:
                model_lst.append(pd.Series(reg.coef_.reshape(-1),X_train_sub.columns,name=('coef_',dt)))
            except:
                pass
    
    tn=pd.concat(train_lst,axis=1).T
    tt=pd.concat(test_lst,axis=1).T
    ml=pd.concat(model_lst,axis=1).T if len(model_lst)>0 else None
    return tn,tt,ml

class combine_clf_models:
    def __init__(self,silent=True):
        self.model_list=[]
        self.silent=silent
    def add_clf(self,name,clf,weight=1):
        self.model_list.append((name,clf,weight))
        return self
    def fit(self,X,y):
        for i in self.model_list:
            if not self.silent:
                cprint('training {}'.format(i[0]),c='p')
            i[1].fit(X,y)
        return self
    def predict_proba(self,X):
        '''
        average proba as new proba
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            if not self.silent:
                cprint('predicting {}'.format(i[0]),c='p')
            Value.append(i[1].predict_proba(X))
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)
    @property
    def coef_(self):
        '''
        average coef
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            assert 'coef_' in dir(i[1]), 'no coef_ found in {}'.format(i[0])
            Value.append(i[1].coef_.reshape(-1))
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)
    @property
    def feature_importances_(self):
        '''
        rank and average feature_importances_
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            assert 'feature_importances_' in dir(i[1]), 'no feature_importances_ found in {}'.format(i[0])
            Value.append(i[1].feature_importances_.argsort().argsort())
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)

class combine_reg_models:
    def __init__(self,silent=True):
        self.model_list=[]
        self.silent=silent
    def add_reg(self,name,reg,weight=1):
        self.model_list.append((name,reg,weight))
        return self        
    def fit(self,X,y):
        for i in self.model_list:
            if not self.silent:
                cprint('training {}'.format(i[0]),c='p')
            i[1].fit(X,y)
        return self            
    def predict(self,X):
        '''
        average predict as new predict
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            if not self.silent:
                cprint('predicting {}'.format(i[0]),c='p')
            Value.append(i[1].predict(X))
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)
    @property
    def coef_(self):
        '''
        average coef_
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            assert 'coef_' in dir(i[1]), 'no coef_ found in {}'.format(i[0])
            Value.append(i[1].coef_.reshape(-1))
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)
    @property
    def feature_importances_(self):
        '''
        rank and average feature_importances_
        '''
        Value=[]
        Weight=[]
        for i in self.model_list:
            assert 'feature_importances_' in dir(i[1]), 'no feature_importances_ found in {}'.format(i[0])
            Value.append(i[1].feature_importances_.argsort().argsort())
            Weight.append(i[2])
        return np.average(Value,axis=0,weights=Weight)