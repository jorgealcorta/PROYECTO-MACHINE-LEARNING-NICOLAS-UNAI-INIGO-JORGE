import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import SelectKBest, SelectPercentile, mutual_info_classif

def preprocess (df, target_column):
    df = correct_key(df)
    df = correct_mode(df)
    df = df.dropna()
    df = df.drop_duplicates()
    create_clusters(df)
    df = object_column_to_categorical(df, "key")
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

def create_clusters(df):
    df2 = df.copy()
    
    df2["clusters_popularity"] = pd.cut(df2["popularity"],bins =5,labels=["Unpopular", "Disliked", "Average", "Liked", "Popular"])
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

def split_train_test_df(feature_df:pd.DataFrame, target_column:str, train_sample:float=0.8):
    assert train_sample <= 1.0, "train_sample must be less than 1.0"

    original_df = feature_df.copy(deep=True)
    train_df = original_df.sample(frac=train_sample, replace=False)
    test_df = original_df.loc[list(filter(lambda index: index not in train_df.index, original_df.index))]

    # Split data into X and Y
    #train_data = split_XY(train_df, target_column)
    test_data = split_XY(test_df, target_column)
    
    return train_df, test_data


def split_XY(feature_df:pd.DataFrame, target_column:str):
    original_df = feature_df.copy(deep=True)
    X = original_df.drop(columns = target_column).values
    Y = original_df[target_column]
    
    return X, Y
       
def filter_mutual_info(df, target_column, k_num):
 
   
   y = df[target_column]
   y_2 = df[string_colunms]
   df = df.drop(columns=string_colunms)
   X = df.drop(columns=target_column)
   
    
   selector = SelectKBest(mutual_info_classif, k=k_num)
   X_reduced = selector.fit_transform(X, y)
   
   return X.join(y).join(y_2)

def std_scaler(feature_df:pd.DataFrame, target_column:str= "popularity"):
    scaler = StandardScaler()
    if target_column in feature_df.columns:
        scaler.fit(feature_df.drop(columns = target_column).values)
    else:
        scaler.fit(feature_df.values)
    return scaler

def object_column_to_categorical(feature_df: pd.DataFrame, column:str, set_of_values:list=None):
    df = feature_df.copy(deep=True)
    df[column] = df[column].astype(str)

    if set_of_values is None:
        set_of_values = set(df[column].values)

    value_columns = [column + "_is_" + str(value) for value in set_of_values]


    loc_column = df.columns.get_loc(column)

    for value in set_of_values:
        loc_column += 1
        categorical_values = (df[column] == value) * 1.0
        df.insert(loc=loc_column, column=column + "_is_" + str(value), value=categorical_values)

    
    df = df.drop(columns = column)
    
    return df



def undersample(df, global_undersample = 1, local_undersample = 0.2):
    
    assert local_undersample <= 1.0 and global_undersample <=1.0 , "undersample fractions must be lesser than 1.0"
    print("Train dataframe before undersampling", df.shape)

    
    average_dataframe =df[ np.logical_and(df['popularity']>30 , df['popularity']<70)]
    edges_dataframe = df[np.logical_or(df['popularity']<=30 , df['popularity']>=70)]


    average_dataframe = average_dataframe.sample(frac = local_undersample).reset_index(drop=True)
    
    
    all_dataframe = pd.concat([average_dataframe, edges_dataframe], axis = 0)
    all_dataframe = all_dataframe.sample(frac = global_undersample).reset_index(drop=True)
    
    print("Train dataframe before undersampling", df.shape)

    return all_dataframe






# -------------------------------------------------------------------------------------------------




