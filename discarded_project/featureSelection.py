

import pandas as pd
from sklearn.datasets import fetch_openml
import numpy as np
from sklearn.feature_selection import SelectKBest, SelectPercentile, mutual_info_classif


def pre_process ( dataframe, categorical_columns):
   dataframe = clean_data(dataframe)
   dataframe.loc[(dataframe[popularity_artist]==0) & (dataframe[typee] == "compilation")  & (dataframe[popularity_collab_avg] != 0)][popularity_artist] = dataframe[popularity_collab_avg]
   dataframe['restrictions'] = np.where(dataframe['restrictions'] == 'FALSE', 0,1)
   dataframe = pd.get_dummies(dataframe, columns=discrete_columns) 
   dataframe[popularity_collab_avg] = dataframe[popularity_collab_avg].round(0)
   dataframe['avg_popularity'] = dataframe['avg_popularity'].round(0)
   
   return None 

def filter_mutual_info(df, target_column, k_num):
 
   
   y = df[target_column]
   df = df.drop(columns = ['album_name','release_date'])
   X = df.drop(columns=target_column )

    
   selector = SelectKBest(mutual_info_classif, k=k_num)
   X_reduced = selector.fit_transform(X, y)
   print(X_reduced.shape)

   return None

def clean_data(df):
    df2 = df.copy()
    longitd = len(df2)
    i = 0
    while i < longitd:
        avg_pop_index = i
        j=i+1
        while j < longitd:
            if df2["album_name"][avg_pop_index] == df2["album_name"][j]:
                if df2["avg_popularity"][avg_pop_index] > df2["avg_popularity"][j]:
                    df2.drop(j, inplace=True)
                    df2 = df2.reset_index(drop=True)
                    longitd = longitd - 1
                else:
                    avg_pop_index = j
                    df2.drop(avg_pop_index, inplace=True)
                    df2 = df2.reset_index(drop=True)
                    longitd = longitd - 1         
            j = j + 1   
        i = i + 1
    return df2
                