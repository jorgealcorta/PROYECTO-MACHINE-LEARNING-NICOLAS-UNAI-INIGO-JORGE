
from tkinter import NE
import spotipy
import pandas as pd
import numpy as np
import time
from spotipy.oauth2 import SpotifyClientCredentials



def get_albums_from_playlist(playlist_uri, sp):
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

def get_albums_from_playlists(playlist_uris, sp):
    album_ids = []

    for uri in playlist_uris:
        album_ids.extend(get_albums_from_playlist(uri, sp))

    return album_ids



def generate_dataset(authentication, playlists, columns, max):
    
    
    client_credentials_manager = SpotifyClientCredentials(client_id= authentication["cid"], client_secret= authentication["secret"])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        
    playlists_URI = [playlist.split("/")[-1].split("?")[0] for playlist in playlists]
    
    dataframe = pd.DataFrame (columns= columns)
    album_ids = list(dict.fromkeys(get_albums_from_playlists(playlists_URI, sp)))


    # TOAS LAS VARIABLES CON '_', SI SON DE ALBUM QUE EMPIECE POR ALBUM Y NADA DE CAMELCASE

    counter = 0

    
    number_of_albums = len(album_ids)
    print("Total albums to scrape: ", number_of_albums)

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
        
        album_in_US = 'US' in markets
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
        album_number_markets, album_in_US, album_in_CA, album_in_BR, album_in_CN, album_in_DE, album_in_ES, album_in_SA, album_in_UK, album_in_RU, album_in_MX]

        
        
        print("albums scraped: ", counter, " / ",  number_of_albums, "Album id: ", album["id"])

        if counter >= max: break
        
        dataframe.loc[counter] = row
        
        if not counter%5: time.sleep(35)
        
        counter += 1
        

    return dataframe
