#!/usr/bin/env python
from __init__ import send_request
from config import MUSIXMATCH_KEY
from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

MUSIXMATCH_SEARCH_TRACK_URL = 'http://api.musixmatch.com/ws/1.1/matcher.lyrics.get'


'''
    TODO
    -----------
    
    * Get specific information to complete a profile obtained from another service
'''

class Musixmatch():
    '''
    
    This class implements a basic communication tool with the Musixmatch API
    
    Attributes
    -----------
    
    api_key : str
        User key needed to communicate with the API 
    
    '''
    
    def __init__(self):
        if not MUSIXMATCH_KEY:
            raise ValueError('The Api Key is empty')
        self.api_key = MUSIXMATCH_KEY
    
    '''
    
    Search the lyrics of a song
    
    Parameters
    -----------
    
    artist : str
        Name of the artist
    track :
        Name of the song related to the artist
        
    Returns
    -----------
    
    json
        Return a json string with the complete response from the Musixmatch API request matcher.lyrics.get 
    '''
    
    def get_lyrics(self, artist, track):
        params = { 'apikey' : self.api_key, 'q_track' : track, 'q_artist' : artist}       
        return send_request(MUSIXMATCH_SEARCH_TRACK_URL, params=params)

        
mm = Musixmatch()

@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "available_uris": {
            "artists": "/musixmatch/lyric/<artist>/<track>",
        }
    })

@app.route('/musixmatch/lyric/<artist>/<track>', methods=['GET']) 
def get_lyrics(artist, track):
    return mm.get_lyrics(artist, track)

            
if __name__ == '__main__':
    app.run(port=5002, debug=True)