import pandas as pd
import os

path = "Playlists/"

files = os.listdir(path)

dataframes = []

for file in files:
    dataframes.append(pd.read_csv(path + "/" + file))

df = pd.concat(dataframes)

df = df.drop_duplicates()

df.to_csv("Playlists/AllPlaylists.csv", index=False)

