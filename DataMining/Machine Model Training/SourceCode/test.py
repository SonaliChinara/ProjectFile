#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import pickle
test_df = pd.read_csv('test.csv', low_memory = False, header = None)
def testClassification(df):
    cgm_max = df.max(axis=1)
    cgm_meal = df[0]
    D_cgm = cgm_max - cgm_meal
    Normalized_D_cgm = D_cgm/cgm_meal

    df['0'] = D_cgm
    df['1'] = Normalized_D_cgm

    p = pickle.load(open('model.sav', 'rb'))
    result = p.predict(df[['0','1']].to_numpy())

    df = pd.DataFrame(result)
    df.to_csv('Result.csv', index = False, header = None)
    print('test completed, please review Result.csv')
testClassification(test_df)

