
from tkinter import NE
import spotipy
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials

#maximum number of albums to scrap
max = 10

columns = ["album_name", "number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date","release_precision",
"restrictions","total_tracks","total_length_min","avg_popularity", "max_popularity","number_of_collabs", "Max_popularity_collab", "Avg_popularity_collab","number_of_markets", 
"NA_market", "CA_market", "BR_market", "CN_market", "DE_market", "ES_market", "SA_market" ,"UK_market", "RU_market", "MX_markets"]

columns_to_follow = ["avg_popularity", "max_popularity"]
columns_variables = ["album_name", "number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date","release_precision",
"restrictions","total_tracks","total_length_min","number_of_collabs", "Max_popularity_collab", "Avg_popularity_collab","number_of_markets", 
"NA_market", "CA_market", "BR_market", "CN_market", "DE_market", "ES_market", "SA_market" ,"UK_market", "RU_market", "MX_markets"]

#Authentication - user 
cid = "a81a443313b743118c9d25e93533a5c2"
secret = "3b77b9e8c7bb4b64a1cf47bbecd87451"


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#playlist to scrape data from:
test_playlist = "https://open.spotify.com/playlist/03VUXoB1kyUKVS2DSlHdtk?si=45574b8f384b4b6d"
rap_caviar = "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd"
a_team = "https://open.spotify.com/playlist/0v4l2wuBE1OvKQxAJrHjlP"
training_montage = "https://open.spotify.com/playlist/7lXPmVSLwJ3LsUUM4fSkSq"
lyrical_rap = "https://open.spotify.com/playlist/7F9HRKYa97J2u6pnCUgDKm"
rap_and_things = "https://open.spotify.com/playlist/6XDVMtbaCVYVMIumo35QAR"
mumble_rap = "https://open.spotify.com/playlist/7lA28B6lUp5NRNe6exWKda"
hiphop = "https://open.spotify.com/playlist/219Diy2i20SU3c8LFEYjkN?si=9UESq3drRSejRlebTXZL5A&utm_source=whatsapp&nd=1"

playlists = [test_playlist, rap_and_things, rap_caviar, training_montage, a_team, lyrical_rap, mumble_rap, hiphop]
playlists_URI = [playlist.split("/")[-1].split("?")[0] for playlist in playlists]


def get_albums_from_playlist(playlist_uri):
    album_ids = []
    offset = 0

    #do while in python:

    while True:
        for track in sp.playlist_tracks(playlist_uri, fields=None, limit=100, offset=offset, market=None)["items"]:

            album = track["track"]["album"]["id"]
            album_ids.append(album)

        offset+=100

        if (len(album_ids) % 100 != 0): break

    return album_ids

def get_albums_from_playlists(playlist_uris):
    album_ids = []

    for uri in playlist_uris:
        album_ids.extend(get_albums_from_playlist(uri))

    return album_ids


first_dataframe = pd.DataFrame ( columns= columns)
album_ids = list(dict.fromkeys(get_albums_from_playlists(playlists_URI)))     #dict.fromkeys() removes duplicates, print(any(album_ids.count(element) > 1 for element in album_ids)) returns True if list has duplicates


# TOAS LAS VARIABLES CON '_', SI SON DE ALBUM QUE EMPIECE POR ALBUM Y NADA DE CAMELCASE

counter = 0

print("Total albums to scrape: ", len(album_ids))

for album in album_ids:
    #album = sp.album(album_ids[0])
    album = sp.album(album)
    album_name = album["name"]
    album_artist_number = len(album["artists"])
    album_artist_followers_total = 0
    album_artist_followers_avg = 0
    album_artist_popularity = 0
    #lista con los ids de los artistas
    album_artist_ids = []


    for artist_partial in album["artists"] :
        artist_id = artist_partial["id"]
        artist = sp.artist(artist_id)
        album_artist_followers_total += artist["followers"]["total"]
        album_artist_followers_avg += artist["followers"]["total"]/ album_artist_number
        album_artist_popularity += artist["popularity"]/ album_artist_number
        album_artist_ids.append(artist_id)


    album_type = album["album_type"]
    album_market = album["available_markets"]
    album_release = album["release_date"]
    album_precision = album["release_date_precision"]
    album_restrictions = "restrictions" in album.keys() #se podria añadir el tipo de restriccion
    album_number_songs = album["total_tracks"]

    # Tracks (nº of tracks + length total length + avg length +   + avg popularity + min/max popularity  nº of explicit (igual mejor meter porcentaje de explicit?))
    # [artists + duration + explicit  + ext artists ]


    album_number_explicit = 0   # buscar en funcion de que el album es explicit o no --------
    album_avg_popularity = 0
    album_max_popularity = 0
    album_total_duration = 0
    album_avg_duration = 0
    
    external_artist_id = []

    for track in album["tracks"]["items"]:
        song = sp.track(track["id"])


        song_duration = song["duration_ms"]
        album_total_duration += song_duration // (1000 * 60)    #minutes
        album_avg_duration += song_duration // album_number_songs

        song_popularity = song["popularity"]
        album_avg_popularity += (song_popularity/album_number_songs)
        if song_popularity > album_max_popularity: album_max_popularity = song_popularity


        #add external artisst of the song 
        for artist in song["artists"]:
            if(artist["id"] not in album_artist_ids):  external_artist_id.append(artist["id"])


    album_colab_max_pop = 0
    album_colab_avg_pop = 0
    album_colab_number = len(external_artist_id)
    
    for artist_id in external_artist_id:
        
        artist = sp.artist(artist_id)
        album_colab_avg_pop = artist["popularity"] / len(external_artist_id)

        if artist["popularity"] > album_colab_max_pop : album_colab_max_pop = artist["popularity"]
        

    markets = album["available_markets"]
    album_number_markets = len(markets)
    
    album_in_NA = 'NA' in markets
    album_in_CA = 'CA' in markets
    album_in_BR = 'BR' in markets
    album_in_CN = 'CN' in markets
    album_in_DE = 'DE' in markets
    album_in_ES = 'ES' in markets
    album_in_SA = 'SA' in markets
    album_in_UK = 'UK' in markets
    album_in_RU = 'RU' in markets
    album_in_MX = 'MX' in markets

   
    row = [album_name, album_artist_number, album_artist_followers_total, album_artist_followers_avg, album_artist_popularity, album_type, album_release, album_precision, album_restrictions, 
    album_number_songs, album_total_duration, album_avg_popularity, album_max_popularity, album_colab_number, album_colab_max_pop, album_colab_avg_pop, 
    album_number_markets, album_in_NA, album_in_CA, album_in_BR, album_in_CN, album_in_DE, album_in_ES, album_in_SA, album_in_UK, album_in_RU, album_in_MX]
     
    
    if len(first_dataframe.index)>=max: break
    
    first_dataframe.loc[len(first_dataframe.index)] = row
    
    if not len(first_dataframe.index)%10: print(f"Scraped {len(first_dataframe.index)} albums.")



print(np.shape(first_dataframe))

#first_dataframe.to_csv('first_dataframe.csv', index=False, encoding='utf-8')

