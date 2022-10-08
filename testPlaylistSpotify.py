
from tkinter import NE
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

#Authentication - without user

initial_columns = ["artist_id", "album_type", "popularity", "number_markets", "release_date", "release_precision", "restrictions_bool", "total_tracks" ,"tracks_ids"]

cid = "a81a443313b743118c9d25e93533a5c2"
secret = "3b77b9e8c7bb4b64a1cf47bbecd87451"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/5TlJI9IeMhCIBceIN2bTte?si=71c98728458b400b"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

album_ids = []

for track in sp.playlist_tracks(playlist_URI)["items"]:

    album = track["track"]["album"]["id"]
    album_ids.append(album)
    
first_dataframe = pd.DataFrame ( )
album_ids = list(dict.fromkeys(album_ids))


for album in album_ids:
    album = sp.album(album_ids[0])
    
    artist_id = album["artists"][0]["id"] #puede haber + d 1 artista ¿ 
    album_type = album["album_type"]
    album_pop = album["popularity"]
    album_market = album["available_markets"]
    album_release = album["release_date"]
    album_precision = album["release_date_precision"]
    album_restrictions = "restrictions" in album.keys() #se podria añadir el tipo de restriccion
    album_number_songs = album["total_tracks"]

    # Tracks (nº of tracks + length total length + avg length +  nº of explicit (igual mejor meter porcentaje de explicit?))
    # [artists + duration + explicit  + ext artists ]

    
    tracks = []
    for track in album["tracks"]["items"]:
        tracks.append([track["name"], track["duration_ms"], track["explicit"]])
        print(tracks)

    album_total_length = 0
    nExplicit = 0
    for i in range(0,len(tracks)):
        album_total_length += tracks[i][1]
        if tracks[i][2]: nExplicit+=1

    album_prct_explicit = nExplicit / len(tracks)
    album_avg_length = album_total_length // len(tracks) #Le he quitado decimales porque ya esta en milisegundos como para ponernos a pillar 6 decimales

    break



    

    