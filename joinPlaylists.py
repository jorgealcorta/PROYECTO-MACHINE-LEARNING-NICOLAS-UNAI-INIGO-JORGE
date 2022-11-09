import pandas as pd
import os

path = "/Users/unaiigartua/git/PROYECTO-MACHINE-LEARNING-NICOLAS-UNAI-INIGO-JORGE/Playlists/"

files = os.listdir(path)

dataframes = []

for file in files:
    dataframes.append(pd.read_csv(path + "/" + file))

df = pd.concat(dataframes)

df = df.drop_duplicates()

df.to_csv("/Users/unaiigartua/git/PROYECTO-MACHINE-LEARNING-NICOLAS-UNAI-INIGO-JORGE/AllPlaylists.csv", index=False)

