from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def run_spotify_etl():

    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")


    # Set up authorization
    # client_credentials_manager object is responsible for obtaining an access token from the Spotify API, which is used to make requests to the API.
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get artist ID
    artist_name = 'Ed Sheeran'
    results = sp.search(q=artist_name, type='artist')
    artist_id = results['artists']['items'][0]['id']

    # get top 10 tracks for artist
    top_tracks = sp.artist_top_tracks(artist_id)['tracks']

    # create dataframe
    df = pd.DataFrame(columns=['Track Name', 'Artist Name', 'Album Name', 'Number of Listeners'])
    for track in top_tracks:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        num_listeners = sp.track(track['id'])['popularity']
        df = df.append({'Track Name': track_name,
                        'Artist Name': artist_name,
                        'Album Name': album_name,
                        'Number of Listeners': num_listeners}, ignore_index=True)

    # save dataframe to csv
    df.to_csv('s3://ann-spotify-bucket/top_10_tracks.csv', index=False)
    print("The dataframe has been saved")
