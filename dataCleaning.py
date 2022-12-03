import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler



       
def filter_mutual_info(df, target_column, k_num):
 
   
   y = df[target_column]
   X = df.drop(columns=target_column )

    
   selector = SelectKBest(mutual_info_classif, k=k_num)
   X_reduced = selector.fit_transform(X, y)
   print(X_reduced.shape)

   return None         
                
def std_scaler(feature_df:pd.DataFrame, target_column:str= "popularity"):
   scaler = StandardScaler()
   scaler.fit(drop_columns_if_exist(feature_df, [target_column]).values)
   return scaler

def object_column_to_categorical(feature_df: pd.DataFrame, column:str, set_of_values:list=None):
    df = feature_df.copy(deep=True)
    df[column] = df[column].astype(str)

    if set_of_values is None:
        set_of_values = set(df[column].values)

    value_columns = [column + "_is_" + str(value) for value in set_of_values]
    df = drop_columns_if_exist(df, value_columns)

    loc_column = df.columns.get_loc(column)

    for value in set_of_values:
        loc_column += 1
        categorical_values = (df[column] == value) * 1.0
        df.insert(loc=loc_column, column=column + "_is_" + str(value), value=categorical_values)
    
    df = drop_columns_if_exist(df, [column])
    return df

def preprocess (df):

   return void