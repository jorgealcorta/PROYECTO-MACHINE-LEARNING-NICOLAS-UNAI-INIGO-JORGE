
from tkinter import NE
import spotipy
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials

from dataCollection import *
#from joinPlaylists import *

#maximum number of albums to scrap
MAX = 2008

columns = ["album_name", "number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date","release_precision",
"restrictions","total_tracks","total_length_min","avg_popularity", "max_popularity","number_of_collabs", "Max_popularity_collab", "Avg_popularity_collab","number_of_markets", 
"US_market", "CA_market", "BR_market", "CN_market", "DE_market", "ES_market", "SA_market" ,"UK_market", "RU_market", "MX_markets"]

columns_to_follow = ["avg_popularity", "max_popularity"]
columns_variables = ["album_name", "number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date","release_precision",
"restrictions","total_tracks","total_length_min","number_of_collabs", "Max_popularity_collab", "Avg_popularity_collab","number_of_markets", 
"US_market", "CA_market", "BR_market", "CN_market", "DE_market", "ES_market", "SA_market" ,"UK_market", "RU_market", "MX_markets"]
columns_date = []
columns_categorical = ["type", ]

authentication = {"cid": "a81a443313b743118c9d25e93533a5c2", "secret": "3b77b9e8c7bb4b64a1cf47bbecd87451"}



# client_credentials_manager = SpotifyClientCredentials(client_id=aut, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#playlist to scrape data from:
test_playlist = "https://open.spotify.com/playlist/03VUXoB1kyUKVS2DSlHdtk?si=45574b8f384b4b6d"
rap_caviar = "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd"
a_team = "https://open.spotify.com/playlist/0v4l2wuBE1OvKQxAJrHjlP"
training_montage = "https://open.spotify.com/playlist/7lXPmVSLwJ3LsUUM4fSkSq"
lyrical_rap = "https://open.spotify.com/playlist/7F9HRKYa97J2u6pnCUgDKm"
rap_and_things = "https://open.spotify.com/playlist/6XDVMtbaCVYVMIumo35QAR"
mumble_rap = "https://open.spotify.com/playlist/7lA28B6lUp5NRNe6exWKda"
hiphop = "https://open.spotify.com/playlist/219Diy2i20SU3c8LFEYjkN?si=9UESq3drRSejRlebTXZL5A&utm_source=whatsapp&nd=1"
best_rap_music_ever = "https://open.spotify.com/playlist/6qxdG8IKGOwfNvbLjLGxn2?si=92789a354a6e482a"
rap_no_skips_needed = "https://open.spotify.com/playlist/5rmOIm6Ps4G9bdyldHQ5iE?si=f4508139de134037"
hip_hop_mano_emoji = "https://open.spotify.com/playlist/1jvQJhPyI0p1x09iDxmJbA?si=747692d974b149f5"
best_hip_hop_of_all_time = "https://open.spotify.com/playlist/1PIy8ktH4S4BwZx9JAB5zN?si=aa347ad000094aca"
rap_dumpster = "https://open.spotify.com/playlist/6c1c8Hxdh6y80pckANQGan?si=cc23a614d87f4553"

playlists = [test_playlist, rap_and_things, rap_caviar, training_montage, a_team, lyrical_rap, mumble_rap, hiphop, best_rap_music_ever, hip_hop_mano_emoji, best_hip_hop_of_all_time]
playlists_URI = [playlist.split("/")[-1].split("?")[0] for playlist in playlists]

client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def getAlbumsAndTracks(playlists):
    albums = Albums()
    albums.to_csv(playlists, sp)

def create_dataset(playlists):
    #getAlbumsAndTracks(playlists, sp)

    dataset = generate_dataset(sp, columns, MAX)

    print(np.shape(dataset))
    dataset.to_csv('finalDataset.csv', index=False, encoding='utf-8')

#Ejecutar con precaución.

#Consigue los álbumes a scrapear desde las playlist especificadas
#getAlbumsAndTracks(playlists_URI)

#Scrapea de spotify. cada 5 segundos de programa dedica 2 a ejecutar requests y 3 a esperar para engañar a 
# la ventana de escucha de spotify y que no detecte límite de tarifa.
create_dataset(playlists_URI)

#!!!!!Cuidado
#Puede borrar datos necesarios si no ponemos los parámetros adecuados.
#scraped = pd.concat([
        #pd.read_csv('first_scrape_500.csv'),
        #pd.read_csv('second_scrape_400.csv'),
        #pd.read_csv('third_scrape_400.csv')], 
        #ignore_index=True)

#remove_ids(tracks = pd.read_csv('album_tracks1.csv', header=None)[5], 
           #last_scraped = scraped, 
           #new_dataset_name = 'new_id_dataset3.csv')
    