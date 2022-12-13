import pandas as pd
import numpy as numpy
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from dataCleaning import *
from dataAnalysis import *
from parameterTuning import *
from parameterTuning import *
from regression_models import *

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
# warnings.simplefilter(action='ignore', category=DataConversionWarning)


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
rfe.fit(df.drop(columns = target_column), df[popularity])

selected_columns = df.drop(columns = target_column).columns[rfe.support_]

df = undersample(df , global_undersample= 0.1, local_undersample= 1)

train, test = train_test_split(df, test_size=0.2)

y_train = train["clusters_popularity"]
x_train = train[selected_columns]

y_test = test["clusters_popularity"]
x_test = test[selected_columns]


scaler = std_scaler(x_train)
svm = SVC()
print("test pre fit")

svm.fit(scaler.transform(x_train), y_train)

predictions = svm.predict(scaler.transform(x_test))

confusion_matrix = confusion_matrix(y_test, predictions)
accuracy = accuracy_score(y_test, predictions)

# Print the confusion matrix and accuracy score
print("Confusion matrix:")
print(confusion_matrix)
print("Accuracy:", accuracy)