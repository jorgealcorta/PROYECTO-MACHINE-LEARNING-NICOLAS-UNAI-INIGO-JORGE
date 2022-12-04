
import pandas as pd
import numpy as np
from dataCleaning import *
from regression_models import *


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

Y_validate = model.predict(scaler.transform(X_test[0:10]))

print(Y_validate)
print(Y_test[0:10])

