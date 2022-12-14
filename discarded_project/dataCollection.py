
from tkinter import NE
import spotipy
import pandas as pd
import numpy as np
import time
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import warnings


#attempt to override the retry_after method:

from urllib3.util.retry import Retry
orig_parse_retry_after = Retry.parse_retry_after
Retry.parse_retry_after = lambda self, retry_after: min(10, orig_parse_retry_after(self, retry_after))

class Albums:

    name = ""
    album_ids = []
    tracks = []
    playlist_uri = ""

    def __init__(self):
        self.name = "'Albums' <class>"

    def __str__(self):
        return f'Containing {len(self.album_ids)} album ids && {len(self.tracks)} tracks.'

    def get_albums_from_playlist(self, playlist_uri, sp):
        offset = 0
        scraped_counter = 0
        #do while in python:

        while True:
            tracks = sp.playlist_tracks(playlist_uri, fields=None, limit=100, offset=offset, market=None)["items"]
            for track in tracks:

                album = track["track"]["album"]["id"]
                if track not in self.tracks: self.tracks.append(track)
                if album not in self.album_ids: self.album_ids.append(album)
                scraped_counter+=1

            offset+=100

            if (scraped_counter % 100 or len(tracks) == 0): break

        return self.album_ids

    def get_albums_from_playlists(self, playlist_uris, sp):

        for uri in playlist_uris: self.get_albums_from_playlist(uri, sp)

        return self.album_ids

    def get_album_ids(self):
        return self.album_ids

    def to_csv(self, playlists_URI, sp):

        #rellena la variable tracks y hace return de los ids

        self.get_albums_from_playlists(playlists_URI, sp)

        tracks = pd.DataFrame(self.tracks)
        albums = pd.DataFrame(self.album_ids)
        tracks.to_csv('album_tracks1.csv', header=None)
        albums.to_csv('album_ids1.csv', header=None)

def remove_ids(tracks, last_scraped, new_dataset_name):   #removes already scraped ids. 
    #                    
    #               - tracks holds every playlists's track data scraped (specified in testPlaylistSpotify.py)
    #               - last_scraped contains the lastly scraped albums.
    #               - new_album_ids will contain the ids that have not yet been scraped
    #                    
    #               -> substitute these variables with the necessary resources to gather unscraped album ids from the playlists.
    #                   

    names_and_release_tracks = []

    for track in tracks:
        names_and_release_tracks.append([[eval(track)["album"]["name"], eval(track)["album"]["release_date"]], eval(track)["album"]["id"]])

    names_and_release_first_scrape = []

    names = last_scraped["album_name"]
    dates = last_scraped["release_date"]

    for i in range(min(len(names), len(dates))):
        names_and_release_first_scrape.append([names[i], dates[i]])

    new_album_ids = []

    for names_and_release in names_and_release_tracks:
        if names_and_release[0] not in names_and_release_first_scrape:
            new_album_ids.append(names_and_release[1])
    
    new_ids = pd.DataFrame(list(set(new_album_ids)))
    new_ids.to_csv(new_dataset_name, header=None)

    return new_ids



def generate_dataset(sp, columns, max, fileName):
    
    dataframe = pd.DataFrame (columns= columns)
    #album_ids debe ser actualizado cada vez que se haya conseguido scrapear ??lbumes nuevos.
    album_ids = pd.read_csv(fileName, header=None)[1]
    

    # TOAS LAS VARIABLES CON '_', SI SON DE ALBUM QUE EMPIECE POR ALBUM Y NADA DE CAMELCASE

    albums_scraped = 0
    songs_scraped = 0
    last = time.time()
    interval = 5   #interval in seconds
    attributeErrorCount = 0

    number_of_albums = len(album_ids)
    print("Total albums to scrape: ", number_of_albums)

    for album in album_ids:
        albums_scraped += 1

        #album = sp.album(album_ids[0])
        #if songs_scraped - last_songs_scraped > 200:
            #print("waiting on main thread...")
            #time.sleep(65)
            #print(f"retaking the task. Songs scraped: {songs_scraped}, Albums scraped: {albums_scraped}")
            #last_songs_scraped = songs_scraped

        now = time.time()
        if now - last >= interval:
            print("waiting to trick the max requests time window...")
            time.sleep(3)
            last = now
        
        #It is lately stopping at 400+ albums scraped. So lets wait for a bit every 400 albums:
        if not albums_scraped % 400:
            print(f"{albums_scraped} albums have been scraped. Chilling for 62 secs...")
            time.sleep(62)

        #hace falta scrapear los albumes y que necesitamos todos los ids de sus canciones, es algo que no nos da sp.playlist_tracks()
        try:
            album = sp.album(album)
        except AttributeError:
            attributeErrorCount += 1
            print(f"There was one attribute error. Number of errors: {attributeErrorCount}")
            continue

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
        album_restrictions = "restrictions" in album.keys() #se podria a??adir el tipo de restriccion
        album_number_songs = album["total_tracks"]

        # Tracks (n?? of tracks + length total length + avg length +   + avg popularity + min/max popularity  n?? of explicit (igual mejor meter porcentaje de explicit?))
        # [artists + duration + explicit  + ext artists ]

        album_number_explicit = 0   # buscar en funcion de que el album es explicit o no --------
        album_avg_popularity = 0
        album_max_popularity = 0
        album_total_duration = 0
        album_avg_duration = 0
        
        external_artist_id = []

        for track in album["tracks"]["items"]:
            #Esto tarda demasiado. comentado en caso de ser ??til en el futuro
            #we may already have that song.
            #for t in tracks:
                #if eval(t)["id"] == track["id"]:
                    #song = eval(t)
                    #break
            #else:
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
            album_colab_avg_pop += artist["popularity"] / len(external_artist_id)

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

        dataframe.loc[albums_scraped] = row

        songs_scraped += album["total_tracks"]

        if not albums_scraped%10: print(f"Scraped {albums_scraped} / {len(album_ids)} albums.")

        if albums_scraped == 2500: dataframe.to_csv('fourth_scrape_2500.csv', index=False, encoding='utf-8')
        if albums_scraped == 2000: dataframe.to_csv('fourth_scrape_2000.csv', index=False, encoding='utf-8')
        if albums_scraped == 1500: dataframe.to_csv('fourth_scrape_1500.csv', index=False, encoding='utf-8')
        if albums_scraped == 1000: dataframe.to_csv('fourth_scrape_1000.csv', index=False, encoding='utf-8')
        if albums_scraped == 750: dataframe.to_csv('fourth_scrape_750.csv', index=False, encoding='utf-8')
        if albums_scraped == 500: dataframe.to_csv('fourth_scrape_500.csv', index=False, encoding='utf-8')
        if albums_scraped == 400: dataframe.to_csv('fourth_scrape_400.csv', index=False, encoding='utf-8')
        if albums_scraped == 250: dataframe.to_csv('fourth_scrape_250.csv', index=False, encoding='utf-8')

        if albums_scraped >= max: break

def get_average_popularities(sp, columns, max, fileName):
    
    dataframe = pd.DataFrame (columns= columns)
    #album_ids debe ser actualizado cada vez que se haya conseguido scrapear ??lbumes nuevos.
    album_ids = pd.read_csv(fileName, header=None)[1]
    

    # TOAS LAS VARIABLES CON '_', SI SON DE ALBUM QUE EMPIECE POR ALBUM Y NADA DE CAMELCASE

    albums_scraped = 0
    songs_scraped = 0
    last = time.time()
    interval = 5   #interval in seconds
    attributeErrorCount = 0

    number_of_albums = len(album_ids)
    print("Total albums to scrape: ", number_of_albums)

    for id in album_ids:
        albums_scraped += 1

        now = time.time()
        if now - last >= interval:
            print("waiting to trick the max requests time window...")
            time.sleep(3)
            last = now
        
        #It is lately stopping at 400+ albums scraped. So lets wait for a bit every 400 albums:
        if not albums_scraped % 400:
            print(f"{albums_scraped} albums have been scraped. Chilling for 62 secs...")
            time.sleep(62)

        #hace falta scrapear cada ??lbum ya que necesitamos los ids de todas las canciones que contiene, es algo que no nos da sp.playlist_tracks()
        try:
            album = sp.album(id)
        except AttributeError:
            attributeErrorCount += 1
            print(f"There was one attribute error. Number of errors: {attributeErrorCount}")
            continue

        album_name = album["name"]
        album_artist_number = len(album["artists"])
        album_artist_popularity = 0
        #lista con los ids de los artistas
        album_artist_ids = []


        for artist_partial in album["artists"] :
            artist_id = artist_partial["id"]
            artist = sp.artist(artist_id)
            album_artist_popularity += artist["popularity"]/ album_artist_number
            album_artist_ids.append(artist_id)
            
        album_number_songs = album["total_tracks"]
        album_avg_popularity = 0
        external_artist_id = []

        for track in album["tracks"]["items"]:
            song = sp.track(track["id"])

            song_popularity = song["popularity"]
            album_avg_popularity += (song_popularity/album_number_songs)


            #add external artisst of the song 
            for artist in song["artists"]:
                if(artist["id"] not in album_artist_ids):  external_artist_id.append(artist["id"])

        album_colab_avg_pop = 0
        album_colab_number = len(external_artist_id)
        
        for artist_id in external_artist_id:
            
            artist = sp.artist(artist_id)
            album_colab_avg_pop += artist["popularity"] / album_colab_number

        row = [album_name, album_avg_popularity, album_colab_avg_pop]

        dataframe.loc[albums_scraped] = row

        songs_scraped += album["total_tracks"]

        if not albums_scraped%10: print(f"Scraped {albums_scraped} / {len(album_ids)} albums.")

        if albums_scraped == 2500: dataframe.to_csv('popularity_first_scrape_2500.csv', index=False, encoding='utf-8')
        if albums_scraped == 2000: dataframe.to_csv('popularity_first_scrape_2000.csv', index=False, encoding='utf-8')
        if albums_scraped == 1500: dataframe.to_csv('popularity_first_scrape_1500.csv', index=False, encoding='utf-8')
        if albums_scraped == 1000: dataframe.to_csv('popularity_first_scrape_1000.csv', index=False, encoding='utf-8')
        if albums_scraped == 750: dataframe.to_csv('popularity_first_scrape_750.csv', index=False, encoding='utf-8')
        if albums_scraped == 500: dataframe.to_csv('popularity_first_scrape_500.csv', index=False, encoding='utf-8')
        if albums_scraped == 400: dataframe.to_csv('popularity_first_scrape_400.csv', index=False, encoding='utf-8')
        if albums_scraped == 250: dataframe.to_csv('popularity_first_scrape_250.csv', index=False, encoding='utf-8')

        if albums_scraped >= max: break

    return dataframe

