Multi Factor Model
==================

This project is to merge alpha factors into one factor with machine
learning techniques.

Dependencies
------------

-  python 3.5
-  pandas 0.22.0
-  numpy 1.14.3
-  pickle
-  sklearn 0.19.1
-  databox

Example
-------

Preprocessing data
------------------

First create a databox object with original factors and market info.
More can be found in project ``databox``

.. code:: bash

   from databox import databox
   db=databox()\
       .load_indestry(ind)\
       .load_indexWeight(ind_weight)\
       .load_suspend(sus)\
       .load_adjPrice(price)\
       .set_lag(freq='d',day_lag=1)
   for fac_name,fac_df in factors_dictionary.items():
       db.add_factor(fac_name,fac_df)
   db.align_data()\
     .factor_ind_neutral()\
     .factor_size_neutral()

Then custmize your data for model training

.. code:: bash

   sp=sample_pipeline()\
       .set_fw_return_n(1)\
       .set_sample_n(1)\
       .factor_rank()\
       .factor_zscore()\
       .fw_return_ind_neutral()\
       .fw_return_rank()\
       .fw_return_I(thresh=2000)

Note all returns are multiplied by 100 for better modeling.

| Options:
| ``set_fw_return`` is to set the number of days to claculate forward
  return;
| ``set_sample_n`` is to set how many days to use in one sample;
| ``factor_rank`` is to rank all factors in each sample;
| ``factor_zscore`` is to normalize factors in each sample;
| ``fw_return_ind_neutral`` is to neutralize returns by industry. If the
  portfolio have industry constrain, this is likely to improve the
  training result;
| ``fw_return_rank`` is to convert returns to their rank in each sample;
| ``fw_return_I`` is to convert returns as 0 or 1, indicating whether
  the return value is geater than or equal to the threshold;

Now create sample as

.. code:: bash

   X_train,y_train=sp.train_set(db)
   X_test,y_test=sp.test_set(db)
   X_test_all=sp.test_X(db)

Modeling
--------

Classification Method

.. code:: bash

   from sklearn.ensemble import RandomForestClassifier
   clf=RandomForestClassifier()
   tn,tt,ml=clf_model(clf,X_train,y_train,X_test,y_test)

Where ``y`` can be 0/1 or float and result ``tn`` (train) and ``tt``
(test) would be different depending on this. If ``clf`` is a tree based
model, ``ml`` would be feature importance. If ``clf`` is a linear model,
``ml`` would be coeffient.

We can also creat a model by combining several models.

.. code:: bash

   from sklearn.ensemble import RandomForestClassifier
   from sklearn.linear_model import LogisticRegression
   from sklearn.svm import SVC
   clf1=RandomForestClassifier()
   clf2=LogisticRegression()
   clf3=SVC()
   from multi_factor_model import combine_clf_models
   CLF=combine_clf_models()\
       .add_clf('rf',clf1)\
       .add_clf('lr',clf2)\
       .add_clf('svc',clf3,weight=2)#default weight is 1
   tn,tt,ml=clf_model(CLF,X_train,y_train,X_test,y_test)    

Regression Method Same as Classification method with ``reg_model`` as
the replacement of ``clf_model`` and ``combine_reg_models`` as that of
``combine_clf_models``

Combined Factor
---------------

.. code:: bash

   import pandas as pd
   value=CLF.predict_proba(X_test_all)
   factor=pd.Series(value[:,1],index=X_test_all.index)


