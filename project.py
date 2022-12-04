
import pandas as pd
import numpy as np
from dataCleaning import *
from regression_models import *
from sklearn.metrics import r2_score, mean_squared_error
from itertools import compress


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

model = model_1(X_train.shape[1])

model.fit(scaler.transform(X_train), Y_train,
          batch_size=128,
          epochs=10,
          verbose=1,
          validation_data=(scaler.transform(X_test), Y_test)
)

print("--------------------------------------------------------------------------------------------------")

# we test our model with the unused rest of the dataset stored in X_test

#~~~~~~~~~~~~~~~~~~~~  DATASET METRICS
Y_validate1 = model.predict(scaler.transform(X_test))

coef_determination = r2_score(Y_test, Y_validate1.flatten())
mse = mean_squared_error(Y_test, Y_validate1.flatten())

print(f"--> Dataset's coefficient of determination: {coef_determination}")
print(f"--> Dataset's mean squared error: {mse}")
print("--------------------------------------------------------------------------------------------------")



#~~~~~~~~~~~~~~~~~~~~  METRICS FOR HIGH POPULARY

popularity_min = 70

# take the ones that have >= {popularity_min} popularity:

high_pop_tuples = ((Y_test >= popularity_min).values).flatten()

X_test_high = pd.DataFrame(X_test)[high_pop_tuples]
Y_test_high = pd.DataFrame(Y_test)[high_pop_tuples]

Y_validate2 = model.predict(scaler.transform(X_test_high))

coef_determination = r2_score(Y_test_high, Y_validate2.flatten())
mse = mean_squared_error(Y_test_high, Y_validate2.flatten())

print(f"--> Coefficient of determination for tracks with >= {popularity_min} popularity: {coef_determination}")
print(f"--> Mean squared error for tracks with >= {popularity_min} popularity: {mse}")
print("--------------------------------------------------------------------------------------------------")



#~~~~~~~~~~~~~~~~~~~~  METRICS FOR LOW POPULARITY

popularity_max = 30

# take the ones that have <= {popularity_max} popularity:

low_pop_tuples = ((Y_test <= popularity_max).values).flatten()

X_test_low = pd.DataFrame(X_test)[low_pop_tuples]
Y_test_low = pd.DataFrame(Y_test)[low_pop_tuples]

Y_validate3 = model.predict(scaler.transform(X_test_low))

coef_determination = r2_score(Y_test_low, Y_validate3.flatten())
mse = mean_squared_error(Y_test_low, Y_validate3.flatten())

print(f"--> Coefficient of determination for tracks with <= {popularity_max} popularity: {coef_determination}")
print(f"--> Mean squared error for tracks with <= {popularity_max} popularity: {mse}")
