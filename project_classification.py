import pandas as pd
import numpy as np
from dataCleaning import *
from dataAnalysis import *
from parameterTuning import *
from parameterTuning import *
from regression_models import *
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from xgboost import XGBRegressor

from sklearn.exceptions import DataConversionWarning
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeRegressor

# load the dataset

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DataConversionWarning)


column_names = {"id", "song", "artist", "duration_ms", "danceability", "energy", "key", "loudness", "mode", "loudness", "mode", "speechiness", "acousticness", 
                "instrumentalness", "liveness", "valence", "tempo", "popularity",  "popularity", "artist_followers", "number_of_artists", "number_of_markets"}
target_column = {"clusters_popularity", "popularity"}
popularity = {"popularity"}

string_columns = {"id", "song", "artist"}


df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";")

# Preprocess the data
df = preprocess(df, target_column)
df = df.drop(columns = string_columns)
df = create_clusters(df)




# Create the RFE model and select all features
model = DecisionTreeRegressor()
rfe = RFE(model,n_features_to_select= 9)

# Fit the model to the data
rfe.fit(df.drop(columns = target_column), df[popularity])

selected_columns = df.drop(columns = target_column).columns[rfe.support_]
y = df["clusters_popularity"]
x = df[selected_columns]

scaler = std_scaler(x)

print(y.head())
print(x.head())