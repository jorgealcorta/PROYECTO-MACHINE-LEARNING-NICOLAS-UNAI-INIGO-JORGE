

import pandas as pd
from sklearn.datasets import fetch_openml
import category_encoders as ce
import numpy as np
from sklearn.feature_selection import SelectKBest, SelectPercentile, mutual_info_classif



def pre_process ( dataframe, categorical_columns):

   return None 

def filter_by_mutual(dataframe, target_column, k_num):
    
    target = 'Who_Pays_for_Access_Work'
    y = df[target]
    X_cat = data.data.drop(columns=['Who_Pays_for_Access_Dont_Know',
       'Who_Pays_for_Access_Other', 'Who_Pays_for_Access_Parents',
       'Who_Pays_for_Access_School', 'Who_Pays_for_Access_Self'])

    
    selector = SelectKBest(mutual_info_classif, k=k_num)
    X_reduced = selector.fit_transform(X, y)
    X_reduced.shape

   return None

