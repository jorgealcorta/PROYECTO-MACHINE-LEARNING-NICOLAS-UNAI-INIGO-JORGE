from featureSelection import *
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dataCollection import *

authentication = {"cid": "848eee75de054d86905af1859a58ebac", "secret": "eaf94b897f6e4948bdab8b4faff38f3c"}
client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


#read data from csv
df = pd.read_csv("datasets_kaggle/dataset_unido.csv", sep = ";")


for index, row in df.iterrows():

    id = row['id']
    #si el id es nulo, se elimina la fila
    if pd.isnull(id):
        cancion = row['song']
        artista = row['artist']
        
        #qwery = f"https://api.spotify.com/v1/search?q=track:"' + {cancion} + '"%20artist:"' + {artista} + '"&type=track&limit=1"
        qwery = f"https://api.spotify.com/v1/search?q=track:\"\' + { cancion } + \'\"\%20artist:\"\' + { artista } + \'\"&type=track"

        result = sp.search(qwery)
        #asignamos el id de la cancion
        try :
            id = result['tracks']['items'][0]['id']
            df.at[index, 'id'] = id
        except:
            print("problema con la cancion: " + cancion + " del artista: " + artista)


        #si index es multiplo de 100, se guarda el dataframe

    if index % 1000 == 0:
            df.to_csv("datasets_kaggle/dataset_unido.csv", sep = ";", index = False)
            print("Guardado en la iteración " + str(index))
        


        
df.to_csv("datasets_kaggle/dataset_unido.csv", sep = ";", index = False)