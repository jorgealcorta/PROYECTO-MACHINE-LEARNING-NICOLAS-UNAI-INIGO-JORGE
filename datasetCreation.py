import pandas as pd
import numpy as np
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
import warnings

def canciones():
    
    print("start scraping")
    warnings.filterwarnings("ignore")
    authentication = {"cid": "359f1923f1c0402784fb0213c1d33a46", "secret": "e32979702a7d471090ea1a9aa2d47ea8"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";")

    #df_canciones = pd.DataFrame(columns = ["id", "number_of_artists", "artist_followers", "number_of_markets"])
    df_canciones = pd.read_csv("datasets_kaggle/canciones.csv")

    ids = []
    contador = 0
    
    if "number_of_artists" not in df.columns:
        print("Resetting columns")
        df["artist_followers"] = np.nan
        df["number_of_artists"] = np.nan
        df["number_of_markets"] = np.nan
        
    
    for index, row in df.iterrows():
        
        if(np.isnan(row["artist_followers"]) or np.isnan(row["number_of_artists"]) or np.isnan(row["number_of_markets"])):
            #guardar el id
            ids.append(row["id"])

            if len(ids) == 50:
                print("Scraping")               
                
                tracks = sp.tracks(ids)
                print("sraped")
                for track in tracks["tracks"]:
                    #si el id de la cancion no se enctra en el dataframe, añadirlo junto con sus datos
                    if track["id"] not in df_canciones["id"].values:
                        artist_followers = 0
                        for artist in track["artists"]:
                            # obtener los followers de cada artista y sumarlos mediant el href
                            result = sp.artist(artist["href"])


                            artist_followers += result["followers"]["total"]/len(track["artists"])
                        df_canciones = df_canciones.append({"id": track["id"], "number_of_artists": len(track["artists"]), "artist_followers": artist_followers, "number_of_markets": len(track["available_markets"])}, ignore_index = True)
                                
                ids = []
                #df_canciones.to_csv("datasets_kaggle/canciones.csv", index = False)
            
            contador += 1

        if contador % 4000 == 0 and contador !=0:
            #espera 2 minutos para no sobrepasar el limite de llamadas a spotify
            print("Waiting 2 minutes")
            time.sleep(120)
            print("Continuing")
        
        if index % 400 == 0 and index !=0:
                df_canciones.to_csv("datasets_kaggle/canciones.csv", index = False)
                print("Guardado en la iteración " + str(index))
                
            
    df_canciones.to_csv("datasets_kaggle/canciones.csv", index = False)    
    


def fechas():
    
    print("start scraping")
    warnings.filterwarnings("ignore")
    authentication = {"cid": "8acb4c7a2a4a498b8e957c81942ad91d", "secret": "a9f7f92142c245f68e8006f5399ef9f0"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos2.csv", sep = ";")

    #df_fechas = pd.DataFrame(columns = ["id", "number_of_artists", "artist_followers", "number_of_markets"])
    df_fechas = pd.read_csv("datasets_kaggle/fechas.csv")

    ids = []
    contador = 0
    
    if "date" not in df.columns:
        print("Resetting columns")
        df["date"] = np.nan
        df["precision"] = np.nan
        
    
    for index, row in df.iterrows():
        
        if(np.isnan(row["date"])):
            #guardar el id
            ids.append(row["id"])

            if len(ids) == 50:
                tracks = sp.tracks(ids)
                for track in tracks["tracks"]:
                    #si el id de la cancion no se enctra en el dataframe, añadirlo junto con sus datos
                    if track["id"] not in df_fechas["id"].values:
                        df_fechas = df_fechas.append({"id": track["id"], "date": track["album"]["release_date"], "precision": track["album"]["release_date_precision"] }, ignore_index = True)
                                
                ids = []
                #df_fechas.to_csv("datasets_kaggle/fechas.csv", index = False)
            
            contador += 1

        if index % 500 == 0 and index !=0:
                df_fechas.to_csv("datasets_kaggle/fechas.csv", index = False)
                print("Guardado en la iteración " + str(index))
                
            
    df_fechas.to_csv("datasets_kaggle/fechas.csv", index = False)    


def completarCanciones():
    df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";")

    df_canciones = pd.read_csv("datasets_kaggle/canciones.csv")
    
    print("Merging datasets...")

    df = df.merge(df_canciones, on="id")

    df.to_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";", index = False)
    print("Done.")



def completarFechas():
    df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos2.csv", sep = ";")
    df_fechas = pd.read_csv("datasets_kaggle/fechas2.csv")

    if "date" not in df.columns:
        print("Resetting columns")
        df["date"] = np.nan
        df["precision"] = np.nan
    
    print("Merging datasets...")

    df = df.merge(df_fechas, on="id")

    df.to_csv("datasets_kaggle/dataset_unido_anyadidos2.csv", sep = ";", index = False)
    print("Done.")

def moreAttributes():
    
    print("start scraping")
    
    authentication = {"cid": "56820a2a52db42dfb355bd3859048827", "secret": "c080c32769c445a5af776276949f91e4"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    df = pd.read_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";")
    
    
    if "number_of_artists" not in df.columns:
        print("Resetting columns")
        df["artist_followers"] = np.nan
        df["number_of_artists"] = np.nan
        df["number_of_markets"] = np.nan
    
    for index, row in df.iterrows():
        
        
        
        if(np.isnan(row["artist_followers"]) or np.isnan(row["number_of_artists"]) or np.isnan(row["number_of_markets"])):

            track = sp.track(row["id"])
            
            
                    
            df.at[index, 'number_of_artists'] = len(track["artists"])  
            
            artist_followers = 0
            for artist in track["artists"]:
                artistR = sp.artist(artist["id"])
                artist_followers += artistR["followers"]["total"]/len(track["artists"]) 
                
            df.at[index, 'artist_followers'] = artist_followers
            
            df.at[index, "number_of_markets"] = len(track["available_markets"])
            print("Scraped index", index)
            
            
                
        
        if index % 500 == 0 and index !=0:
                df.to_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";", index = False)
                print("Guardado en la iteración " + str(index))
                
            
    df.to_csv("datasets_kaggle/dataset_unido_anyadidos.csv", sep = ";", index = False)    
    
def moreAttributes_test():
    
    authentication = {"cid": "848eee75de054d86905af1859a58ebac", "secret": "eaf94b897f6e4948bdab8b4faff38f3c"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    

    
    df = pd.read_csv("datasets_kaggle/dataset_unido_base.csv", sep = ";")
    
    if "num_artists" not in df.columns:
        df["artist_followers"] = np.nan
        df["num_artists"] = np.nan
        df["num_markets"] = np.nan
    
    for index, row in df.iterrows():

        #track = sp.track(row["id"])
        track = sp.track("0VhfZo2uwcWnQGExuOxNKq")
        
        print ("Number of artists: ", len(track["available_markets"]))
        
        for artist in track["artists"]:
            artistR = sp.artist(artist["id"])
            print("followers: ", artistR["followers"])
            
            #print("number of markets: ", len(artist["available_markets"]))
        
        break
            
            
def fillPopularity():
    
    authentication = {"cid": "d1eba31fe2384b13a3ed8d5a2f9731bf", "secret": "b7295ec832ac4818b6673fa587aeb053"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    
    df = pd.read_csv("datasets_kaggle/dataset_unido_test.csv", sep = ";")
    df = df[-(df["id"].isnull())]
    
    for index, row in df.iterrows():
        
        if pd.isnull(row["popularity"]) or row["popularity"] ==  0 :
            track = sp.track(row["id"])
            df.at[index, 'popularity'] = track["popularity"]


        if index % 3000 == 0 and index != 0:
                df.to_csv("datasets_kaggle/dataset_unido_test.csv", sep = ";", index = False)

                print("Guardado en la iteración " + str(index))
                
   
            
            
    df.to_csv("datasets_kaggle/dataset_unido_test.csv", sep = ";", index = False)
    print("Guardado Final")
    
    
def completeDataset():
    dataset = pd.read_csv("datasets_kaggle/dataset_unido.csv", sep = ";")
    
    no_id = dataset.loc[dataset['id'].isnull()]
    with_id = dataset.loc[- dataset['id'].isnull()]
    
    authentication = {"cid": "848eee75de054d86905af1859a58ebac", "secret": "eaf94b897f6e4948bdab8b4faff38f3c"}
    
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    cancion = "despacito"
    artista = "luis fonsi"
    
    qwery2 = f"https://api.spotify.com/v1/search?q=track:"' + {cancion} + '"%20artist:"' + {artista} + '"&type=track&limit=1"
    qwery = f"https://api.spotify.com/v1/search?q=track:\"\' + { cancion } + \'\"\%20artist:\"\' + { artista } + \'\"&type=track"
    qwery3 = "https://api.spotify.com/v1/search?q=track: + {cancion} + %20artist: + {artista} + &type=track"
    result = sp.search(qwery)
    print(result["tracks"]["items"][0]["popularity"])


def fillingId_dataset():

    authentication = {"cid": "b589320bba584c588e4bd1cae505b4fb", "secret": "8c0f3d1b77fa4404b49c06df29d1c64f"}
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

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
    
    
def completeDataset():
    dataset = pd.read_csv("datasets_kaggle/dataset_unido.csv", sep = ";")
    
    no_id = dataset.loc[dataset['id'].isnull()]
    with_id = dataset.loc[- dataset['id'].isnull()]
    
    authentication = {"cid": "848eee75de054d86905af1859a58ebac", "secret": "eaf94b897f6e4948bdab8b4faff38f3c"}
    
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    cancion = "despacito"
    artista = "luis fonsi"
    
    qwery2 = f"https://api.spotify.com/v1/search?q=track:"' + {cancion} + '"%20artist:"' + {artista} + '"&type=track&limit=1"
    qwery = f"https://api.spotify.com/v1/search?q=track:\"\' + { cancion } + \'\"\%20artist:\"\' + { artista } + \'\"&type=track"
    qwery3 = "https://api.spotify.com/v1/search?q=track: + {cancion} + %20artist: + {artista} + &type=track"
    result = sp.search(qwery)
    print(result["tracks"]["items"][0]["popularity"])