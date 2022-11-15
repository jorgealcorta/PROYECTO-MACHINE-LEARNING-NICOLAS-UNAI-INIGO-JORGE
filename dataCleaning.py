import pandas as pd
import numpy as np

def clean_data(df):
    df2 = df.copy()
    longitd = len(df2)
    i = 0
    while i < longitd:
        avg_pop_index = i
        j=i+1
        while j < longitd:
            if df2["album_name"][avg_pop_index] == df2["album_name"][j]:
                if df2["avg_popularity"][avg_pop_index] > df2["avg_popularity"][j]:
                    df2.drop(j, inplace=True)
                    df2 = df2.reset_index(drop=True)
                    longitd = longitd - 1
                else:
                    avg_pop_index = j
                    df2.drop(avg_pop_index, inplace=True)
                    df2 = df2.reset_index(drop=True)
                    longitd = longitd - 1         
            j = j + 1   
        i = i + 1
    return df2
                

            
df = pd.read_csv("first_scrape_500.csv")
df = clean_data(df)
df.to_csv("first_scrape_500_cleaned.csv")
print(df["album_name"][39])
print(df["album_name"][323])
print(df["album_name"][39] == df["album_name"][323])