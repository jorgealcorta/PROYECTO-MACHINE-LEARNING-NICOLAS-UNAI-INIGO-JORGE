from featureSelection import *
import pandas as pd


dataframe = pd.read_csv("first_scrape_500.csv")
dataframe = popularity_cohesion(dataframe, "artist_popularity", "avg_popularity", "max_popularity", "type", ['release_precision', 'type'] )

filter_by_mutual(dataframe, 'avg_popularity', 10)

