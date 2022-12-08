
import pandas as pd
import numpy as np
from dataCleaning import *
from dataAnalysis import *
from regression_models import *
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from xgboost import XGBRegressor

from sklearn import svm

# load the dataset

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


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

(X_train, Y_train), (X_test, Y_test) = split_train_test_df(df, target_column)

print ("X_train: ", X_train.shape)
print ("Y_train: ", Y_train.shape)
print ("X_test: ", X_test.shape)
print ("Y_test: ", Y_test.shape)

#--------------- XGBOOST

model = XGBRegressor()
#(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8)
model.fit(scaler.transform(X_train), Y_train)

model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

#XGBOOST PARAMETER TUNING

'''
print("\n################ MODEL EVALUATION - eta ################")
#eta: it makes the model more robust by shrinking the weights on each step
print("\neta=0.2")
model = XGBRegressor(eta = 0.2)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\neta=0.1")
model = XGBRegressor(eta = 0.1)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\neta=0.5")
model.fit(scaler.transform(X_train), Y_train)
model = XGBRegressor(eta = 0.05)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\nIt makes sense that the coefficient of determination is a bit worse for smaller values of eta, as it is not fitting as well for the sample data")

'''
'''

print("\n################ MODEL EVALUATION - gamma ################")
#gamma: specifies the minimum loss reduction required to make a split
print("\ngamma=0")
model = XGBRegressor(gamma = 0)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\ngamma=100")
model = XGBRegressor(gamma = 100)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\ngamma=500000")
model.fit(scaler.transform(X_train), Y_train)
model = XGBRegressor(gamma = 500000)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\nIt makes sense that the algorithm becomes more conservative with an increase on gamma. At the default value, 0, it is fine. As soon as it goes up, the model gets a lot less accurate.")

'''


print("\n################ MODEL EVALUATION - max_depth ################")
#max_depth: t is used to control over-fitting as higher depth will allow model to learn relations very specific to a particular sample.

# for i in range(15, 20): #BEST MAX_DEPTH=15
#     print(f"\nMODEL EVALUATION MAX_DEPTH={i}")
#     model = XGBRegressor(max_depth = i)
#     model.fit(scaler.transform(X_train), Y_train)
#     model_evaluate(model, scaler, X_test, Y_test)
#     model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
#     model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

'''

print("\n################ MODEL EVALUATION - min_child_weight ################")
#min_child_weight: 
print("\nmin_child_weight=0")
model = XGBRegressor(min_child_weight = 0)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\nmin_child_weight=200")
model = XGBRegressor(min_child_weight = 200)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

print("\nmin_child_weight=500")
model.fit(scaler.transform(X_train), Y_train)
model = XGBRegressor(min_child_weight = 500)
model.fit(scaler.transform(X_train), Y_train)
model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)
print("\Min child weight does not seem to make a huge difference. We have to increase it a lot for it to make a difference.")
'''

# ----------------------- SVM model -----------

print("#############SVM#############")
model = svm.SVC(kernel="rbf", gamma=10)
model.fit(X_train, Y_train)

model_evaluate(model, scaler, X_test, Y_test)
model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
model_evaluate(model, scaler, X_test, Y_test, pop_max=30)





# ----------------------- neural network model -----------
# model = model_1(X_train.shape[1])
# results = []

# for i in range(20):
        

#     model.fit(scaler.transform(X_train), Y_train,
#             batch_size=40,
#             epochs=30+i*2,
#             verbose=0,
#             validation_data=(scaler.transform(X_test), Y_test)
#     )

#     results.append([5+i*3,model_evaluate(model, scaler, X_test, Y_test, pop_max=30) + model_evaluate(model, scaler, X_test, Y_test, pop_min=70)])







