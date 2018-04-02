#!/usr/bin/env python
from __init__ import send_request
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from flask import Flask
from flask import jsonify
import requests



GRANT_TYPE = 'client_credentials'

SPOTIFY_TOKEN_URL='https://accounts.spotify.com/api/token'

SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search'

SPOTIFY_GET_ARTIST = 'https://api.spotify.com/v1/artists/'

SPOTIFY_GET_ARTIST_TOP_TRACKS = 'https://api.spotify.com/v1/artists/{}/top-tracks?country=GB'

SPOTIFY_GET_AUDIO_ANALYSIS_TRACK = 'https://api.spotify.com/v1/audio-analysis/'

app = Flask(__name__)


class Spotify:
    '''
    
    This class implements a basic communication tool with the Spotify API
    
    
    TODO
    -----------
    
    * Refresh the token
    * Choose a specific artist from a search by name
    
    
    Attributes
    -----------
    
    client_id : str
        Client identifier needed to communicate with the API 
    
    client_secret : str
        Secret key needed to communicate with the API 
        
    acces_token : str
        Access token obtained after authentication
        
    headers : str
        Header to use on each request
    '''
    
    def __init__(self):
        if not SPOTIFY_CLIENT_ID:
            raise ValueError('The client ID is empty')
        if not SPOTIFY_CLIENT_SECRET:
            raise ValueError('The client secret is empty')
        
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.acces_token = None
        self.headers = None
    
    
    def generate_access_token(self):
        '''    
        Generate an access token after a client creditentails authentication   
        '''
        data = {'grant_type' : GRANT_TYPE}  
        response = send_request(SPOTIFY_TOKEN_URL, data=data, auth = (self.client_id, self.client_secret), type='post', format=None)           
        self.acces_token = response['access_token']
        self.headers = {'Authorization': 'Bearer ' + self.acces_token}
    
    '''   
    Information of an artist
    
    Parameters
    -----------
    
    id : str
        Spotify ID of the artist
        
    Returns
    -----------
    
    json
        Return a json string with the complete response from the Spotify API request 'https://api.spotify.com/v1/artists/'
    '''
    
    def get_artist_info(self, id):
        return send_request(SPOTIFY_GET_ARTIST + id, headers = self.headers)
    
    '''   
    The 10 most popular tracks of an artist (Great-Britain)
    
    Parameters
    -----------
    
    id : str
        Spotify ID of the artist
        
    Returns
    -----------
    
    json
        Return a json string with the complete response from the Spotify API request 'https://api.spotify.com/v1/artists/{}/top-tracks?country=GB'
    '''
    def get_artist_tracks_info(self, id):
        return send_request(SPOTIFY_GET_ARTIST_TOP_TRACKS.format(id), headers = self.headers)

    '''   
    Audio analysis of a track
    
    Parameters
    -----------
    
    id : str
        Spotify ID of the track
        
    Returns
    -----------
    
    json
        Return a json string with the complete response from the Spotify API request 'https://api.spotify.com/v1/audio-analysis/'
    '''        
    def get_audio_analysis(self, id):
        return send_request(SPOTIFY_GET_AUDIO_ANALYSIS_TRACK + id, headers = self.headers)
sp = Spotify()
sp.generate_access_token()
        
 
@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "available_uris": {
            "artists": "/spotify/artist/<id>",
            "artist": "/spotify/artist/<id>/tracks",
            "tracks": "/spotify/track/<id>/audio-analysis",
        }
    })
 
@app.route('/spotify/artist/<id>', methods=['GET']) 
def get_artist_info(id):
    return sp.get_artist_info(id) 
    
@app.route('/spotify/artist/<id>/tracks', methods=['GET']) 
def get_artist_tracks_info(id):
    return sp.get_artist_tracks_info(id)

    
@app.route('/spotify/track/<id>/audio-analysis', methods=['GET'])
def get_audio_analysis(id):
    return sp.get_audio_analysis(id)
    
if __name__ == '__main__':
    app.run(port=5001, debug=True)