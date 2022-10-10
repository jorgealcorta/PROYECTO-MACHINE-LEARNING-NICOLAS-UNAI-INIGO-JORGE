
from tkinter import NE
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

#Authentication - without user

initial_columns = ["artist_id", "album_type", "popularity", "number_markets", "release_date", "release_precision", "restrictions_bool", "total_tracks" ,"tracks_ids"]
columns = ["number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date","release_precision","restrictions","total_tracks","total_length","avg_popularity", "max_popularity"]

cid = "a81a443313b743118c9d25e93533a5c2"
secret = "3b77b9e8c7bb4b64a1cf47bbecd87451"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/5TlJI9IeMhCIBceIN2bTte?si=71c98728458b400b"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

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

first_dataframe = pd.DataFrame ( columns= columns)
album_ids = list(dict.fromkeys(get_albums_from_playlist(playlist_URI)))     #dict.fromkeys() removes duplicates, print(any(album_ids.count(element) > 1 for element in album_ids)) returns True if list has duplicates


# TOAS LAS VARIABLES CON '_', SI SON DE ALBUM QUE EMPIECE POR ALBUM Y NADA DE CAMELCASE

for album in album_ids:
    #album = sp.album(album_ids[0])
    album = sp.album(album)
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


    for track in album["tracks"]["items"]:
        song = sp.track(track["id"])

        #print (song ["artists"])
        #print ("********************")
        #print (album_artist_ids)
        #sprint ("++++++++++++++++++++")
        song_duration = song["duration_ms"]
        album_total_duration += song_duration
        album_avg_duration += song_duration // album_number_songs

        song_popularity = song["popularity"]
        album_avg_popularity += (song_popularity/album_number_songs)
        if song_popularity > album_max_popularity: album_max_popularity = song_popularity


        #id song artisis
        external_artists_id = []
        for artist in song["artists"]:
            external_artists_id.append(artist["id"])

        #borrar los artistas de la cancion que aparecen en el album
        for artist in album_artist_ids:
            if artist in external_artists_id:
                external_artists_id.remove(artist)


        #extraer todo los datos de los artistas de la cancion
        external_artists = []
        for artist in song["artists"]:
            external_artists.append(sp.artist(artist["id"]))




        external_number = len(external_artists_id)
        external = (external_number != 0)
        external_monthly_followers = 0
        most_popular_artist = album_artist_ids[0]

        if external:
            for artist in external_artists:

                if artist["popularity"] > sp.artist(most_popular_artist)["popularity"]: most_popular_artist = artist["id"]

                external_monthly_followers += artist["followers"]["total"]

    row = [album_artist_number, album_artist_followers_total, album_artist_followers_avg, album_artist_popularity, album_type, album_release, album_precision, album_restrictions, album_number_songs, album_total_duration, album_avg_popularity, album_max_popularity]

    #["number_of_artists", "artist_followers_total","artist_followers_average","artist_popularity","type","release_date"
    # ,"release_precision","restrictions---------","total_tracks","total_length","avg_popularity", "max_popularity","markets_number"
    first_dataframe.loc[len(first_dataframe.index)] = row








    album_in_NA = False
    album_in_CA = False
    album_in_BR = False
    album_in_CN = False
    album_in_DE = False
    album_in_ES = False
    album_in_SA = False
    album_in_UK = False
    album_in_RU = False
    album_in_MX = False








    #break


print(first_dataframe)
