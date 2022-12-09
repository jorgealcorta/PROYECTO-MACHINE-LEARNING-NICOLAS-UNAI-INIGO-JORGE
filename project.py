
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

# load the dataset

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DataConversionWarning)


column_names = {"id", "song", "artist", "duration_ms", "danceability", "energy", "key", "loudness", "mode", "loudness", "mode", "speechiness", "acousticness", 
                "instrumentalness", "liveness", "valence", "tempo", "popularity",  "popularity", "artist_followers", "number_of_artists", "number_of_markets"}
target_column = {"popularity"}

string_columns = {"id", "song", "artist"}


df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";")

df = preprocess(df, target_column)

df = object_column_to_categorical(df, "key")

df = df.drop(columns = string_columns)



scaler = std_scaler(df, target_column = target_column)

print("Full dataframe shape is: ", df.shape)

train_df , (X_test, Y_test) = split_train_test_df(df, target_column,train_sample=0.9)



#train_df = undersample(train_df , global_undersample= 1, local_undersample= 0.8)

X_train, Y_train = split_XY(train_df, target_column)

print ("X_train: ", X_train.shape)
print ("Y_train: ", Y_train.shape)
print ("X_test: ", X_test.shape)
print ("Y_test: ", Y_test.shape)

#--------------- XGBOOST

#XGBOOST PARAMETER TUNING
#tuneXGBoost(scaler, X_test, Y_test, X_train, Y_train)

# model = XGBRegressor()
# #(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8)
# model.fit(scaler.transform(X_train), Y_train)

# model_evaluate(model, scaler, X_test, Y_test)
# model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
# model_evaluate(model, scaler, X_test, Y_test, pop_max=30)


# ----------------------- SVM model -----------


# model = svm.SVR(kernel="linear", gamma=10)
# print("test PRE FIT")


# model.fit(scaler.transform(X_train), Y_train)
# print("test Post fit")


# model_evaluate(model, scaler, X_test, Y_test)
# model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
# model_evaluate(model, scaler, X_test, Y_test, pop_max=30)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     





# ----------------------- neural network model -----------
model = model_1(X_train.shape[1])
results = []

for i in range(15):
        

    model.fit(scaler.transform(X_train), Y_train,
            batch_size=40,
            epochs=30+i*2,
            verbose=0,
            validation_data=(scaler.transform(X_test), Y_test)
    )

    results.append([5+i*3,model_evaluate(model, scaler, X_test, Y_test) + model_evaluate(model, scaler, X_test, Y_test, pop_max=30) + model_evaluate(model, scaler, X_test, Y_test, pop_min=70)])

print(results)
