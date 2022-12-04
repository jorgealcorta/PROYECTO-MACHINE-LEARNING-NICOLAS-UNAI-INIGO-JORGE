import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def preprocess (df):
    df = correct_key(df)
    df = correct_mode(df)
    df = df.dropna()
    df = df.drop_duplicates()
    return df


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

def correct_key(df):
    df2 = df.copy()
    key_mapping = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11, "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11}
    df2["key"] = df2["key"].map(key_mapping)
    df2["key"] = df2["key"].astype(int)
    return df2

def correct_mode(df):
    df2 = df.copy()
    mode_mapping = {"Major": 1, "Minor": 0, "1": 1, "0": 0}
    df2["mode"] = df2["mode"].map(mode_mapping)
    df2["mode"] = df2["mode"].astype(int)
    return df2

'''         
df = pd.read_csv("first_scrape_500.csv")
df = clean_data(df)
df.to_csv("first_scrape_500_cleaned.csv")
print(df["album_name"][39])
print(df["album_name"][323])
print(df["album_name"][39] == df["album_name"][323])
'''


# -------------------------------------------------------------------------------------------------

def split_train_test_df(feature_df:pd.DataFrame, target_column:str, train_sample:float=0.8, to_categorical:bool=True):
    assert train_sample <= 1.0, "train_sample must be less than 1.0"

    original_df = feature_df.copy(deep=True)
    train_df = original_df.sample(frac=train_sample, replace=False)
    test_df = original_df.loc[list(filter(lambda index: index not in train_df.index, original_df.index))]

    # Split data into X and Y
    train_data = split_XY(train_df, target_column, to_categorical)
    test_data = split_XY(test_df, target_column, to_categorical)
    
    return train_data, test_data


def split_XY(feature_df:pd.DataFrame, target_column:str, to_categorical:bool=True):
    original_df = feature_df.copy(deep=True)
    X =  df = df.drop(target_column, index = 1).values
    Y = original_df[target_column]

    if to_categorical:
        num_classes = len(set(original_df[target_column].tolist()))
        Y = keras.utils.to_categorical(Y, num_classes)
    
    return X, Y
       
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
    df = drop

    loc_column = df.columns.get_loc(column)

    for value in set_of_values:
        loc_column += 1
        categorical_values = (df[column] == value) * 1.0
        df.insert(loc=loc_column, column=column + "_is_" + str(value), value=categorical_values)
    
    df = df.drop(column, index = 1)
    return df

# -------------------------------------------------------------------------------------------------




