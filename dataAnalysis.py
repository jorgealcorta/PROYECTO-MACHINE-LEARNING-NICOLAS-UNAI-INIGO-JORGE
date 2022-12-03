# analysis of the dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep=";")

print(df.head())
'''
                       id            song            artist  duration_ms  danceability  energy  ... valence    tempo popularity  artist_followers  number_of_artists  number_of_markets
0  6FhRQ0y2RVoG2dyKaTXKoV        Mask Off            Future       204600         833.0   434.0  ...  286.00  150.062        6.0        12489395.0                1.0                1.0
1  0YsGMHid6sFq5PcToe3JZE         Redbone  Childish Gambino       326933         743.0   359.0  ...  588.00  160.083       79.0        10020401.0                1.0              183.0
2  0BzDQgmeRdA4V71VhfBvXT    Xanny Family            Future       185707         838.0   412.0  ...  173.00   75.044       55.0        12489395.0                1.0              183.0
3  3stWWPN41byqp8loPdy92u  Master Of None       Beach House       199413         494.0   338.0  ...    0.23   86.468       61.0         1675703.0                1.0              183.0
4  2
'''

print(df.describe())
'''
        duration_ms   danceability         energy       loudness    speechiness  ...          tempo     popularity  artist_followers  number_of_artists  number_of_markets
count  2.433920e+05  243392.000000  243392.000000  243392.000000  243392.000000  ...  243392.000000  243392.000000      1.104820e+05      110482.000000      110482.000000
mean   2.339042e+05     499.153647     514.250948     -10.339878      81.562189  ...     117.810627      39.614252      2.779372e+06           1.312494         127.235115
std    1.185771e+05     244.628401     307.418228      27.025737     189.054130  ...      30.874459      19.703754      7.204838e+06           0.817782          81.177486
min    4.693000e+03       0.000000       0.000020    -997.000000       0.000000  ...       0.000000       0.000000      0.000000e+00           1.000000           0.000000
25%    1.818350e+05     367.000000     275.000000     -11.848000       0.037800  ...      93.010000      27.000000      1.164240e+05           1.000000           2.000000
50%    2.195985e+05     545.000000     566.000000      -7.764000       0.055400  ...     116.011000      42.000000      5.637800e+05           1.000000         182.000000
75%    2.647470e+05     679.000000     769.000000      -5.491000      66.000000  ...     139.145000      55.000000      2.143792e+06           1.000000         183.000000
max    5.552917e+06     989.000000     999.000000     954.000000     967.000000  ...     242.903000     100.000000      1.054486e+08          23.000000         183.000000
'''

print(df.info())
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 243392 entries, 0 to 243391
Data columns (total 19 columns):
 #   Column             Non-Null Count   Dtype  
---  ------             --------------   -----  
 0   id                 243392 non-null  object 
 1   song               243392 non-null  object 
 2   artist             243392 non-null  object 
 3   duration_ms        243392 non-null  int64  
 4   danceability       243392 non-null  float64
 5   energy             243392 non-null  float64
 6   key                243392 non-null  object 
 7   loudness           243392 non-null  float64
 8   mode               243392 non-null  object 
 9   speechiness        243392 non-null  float64
 10  acousticness       243392 non-null  float64
 11  instrumentalness   243392 non-null  float64
 12  liveness           243392 non-null  float64
 13  valence            243392 non-null  float64
 14  tempo              243392 non-null  float64
 15  popularity         243392 non-null  float64
 16  artist_followers   110482 non-null  float64
 17  number_of_artists  110482 non-null  float64
 18  number_of_markets  110482 non-null  float64
dtypes: float64(13), int64(1), object(5)
memory usage: 35.3+ MB
None
'''

print(df.columns)
'''
Index(['id', 'song', 'artist', 'duration_ms', 'danceability', 'energy', 'key',
       'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
       'liveness', 'valence', 'tempo', 'popularity', 'artist_followers',
       'number_of_artists', 'number_of_markets'],
      dtype='object')
'''

print(df.shape)
'''
(243392, 19)
'''

print(df.isnull().sum())
'''
id                        0
song                      0
artist                    0
duration_ms               0
danceability              0
energy                    0
key                       0
loudness                  0
mode                      0
speechiness               0
acousticness              0
instrumentalness          0
liveness                  0
valence                   0
tempo                     0
popularity                0
artist_followers     132910
number_of_artists    132910
number_of_markets    132910
dtype: int64
'''

print(df.duplicated().sum())
'''
40930
'''
print(df['key'].value_counts())

