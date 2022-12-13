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

from sklearn.naive_bayes import GaussianNB

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


#NAIVE BAYES    
gnb = GaussianNB()

gnbModel = gnb.fit(x_train, y_train)
y_pred = gnbModel.predict(x_test)

print("X TRAIN")
print(x_train)
print("Y TRAIN")
print(y_train)

print("Number of mislabeled points out of a total %d points : %d" % (x_test.shape[0], (y_test != y_pred).sum()))

print("\nTEST FOR VERY UNPOPULAR")
y_test_very_unpopular = y_test[y_test=="Very unpopular"]
x_test_very_unpopular = x_test[y_test=="Very unpopular"]
y_pred_very_unpopular = gnbModel.predict(x_test_very_unpopular)
print("Number of mislabeled VERY UNPOPULAR points out of a total %d points : %d" % (x_test_very_unpopular.shape[0], (y_test_very_unpopular != y_pred_very_unpopular).sum()))


print("\nTEST FOR UNPOPULAR")
y_test_unpopular = y_test[y_test=="Unpopular"]
x_test_unpopular = x_test[y_test=="Unpopular"]
y_pred_unpopular = gnbModel.predict(x_test_unpopular)
print("Number of mislabeled UNPOPULAR points out of a total %d points : %d" % (x_test_unpopular.shape[0], (y_test_unpopular != y_pred_unpopular).sum()))


print("\nTEST FOR AVERAGE")
y_test_average = y_test[y_test=="Average"]
x_test_average = x_test[y_test=="Average"]
y_pred_average = gnbModel.predict(x_test_average)
print("Number of mislabeled AVERAGE points out of a total %d points : %d" % (x_test_average.shape[0], (y_test_average != y_pred_average).sum()))


print("\nTEST FOR POPULAR")
y_test_popular = y_test[y_test=="Popular"]
x_test_popular = x_test[y_test=="Popular"]
y_pred_popular = gnbModel.predict(x_test_popular)
print("Number of mislabeled POPULAR points out of a total %d points : %d" % (x_test_popular.shape[0], (y_test_popular != y_pred_popular).sum()))


print("\nTEST FOR VERY POPULAR")
y_test_very_popular = y_test[y_test=="Very popular"]
x_test_very_popular = x_test[y_test=="Very popular"]
y_pred_very_popular = gnbModel.predict(x_test_very_popular)
print("Number of mislabeled VERY POPULAR points out of a total %d points : %d" % (x_test_very_popular.shape[0], (y_test_very_popular != y_pred_very_popular).sum()))

