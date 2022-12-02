#from featureSelection import *
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dataCollection import *

#crear dataset canciones de 0 con los siguientes atributos id;number_of_artists;artist_followers;number_of_markets

#df_canciones = pd.DataFrame(columns = ["id", "number_of_artists", "artist_followers", "number_of_markets"])
#guardar en csv
#df_canciones.to_csv("datasets_kaggle/canciones.csv", index = False)



#moreAttributes()
try:
    canciones()
except:
    pass

completarCanciones()