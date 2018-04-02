#!/usr/bin/env python
from __init__ import send_request
from flask import Flask
from flask import jsonify
from werkzeug.exceptions import NotFound
import requests

app = Flask(__name__)

'''
    TODO
    -----------
    
    * Build a parial result when a service is not available
'''


'''
Dictionary of available artists
'''

artists = {
              "faithless" : {
                "spotify_id": "5T4UKHhr4HGIC0VzdZQtAE",
                "name": "Faithless",
              },
              "depeche-mode" : {
                "spotify_id": "762310PdDnwsDxAQxzQkfX",
                "name": "Depeche Mode",
              },
                "plastikman" : {
                "spotify_id": "7GoFQNOTX0suC6Tn59qx8n",
                "name": "Plastikman",
              },            
          }

          
@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "available_uris": {
            "artists": "/artists",
            "artist": "/artists/<artist>",
            "tracks": "/artists/<artist>/tracks",
        }
    })
       
@app.route("/artists", methods=['GET'])
def artists_list():
    return jsonify(artists)
    
    
@app.route("/artists/<artist>", methods=['GET'])
def artist_info(artist):
    if artist not in artists:
        raise NotFound('This artist does not exist ! You can check the available artists at address /artists/')      
    return send_request("http://127.0.0.1:5001/spotify/artist/" + artists[artist]['spotify_id'])

    
@app.route("/artists/<artist>/tracks", methods=['GET'])
def artist_tracks_info(artist):
    if artist not in artists:
        raise NotFound()
        
    artist__tracks_info_spotify = send_request("http://127.0.0.1:5001/spotify/artist/" + artists[artist]['spotify_id'] + "/tracks", format=None)    
    r = {'tracks':[]}
    
    for track in artist__tracks_info_spotify['tracks']:
        track_audio_analysis_spotify = send_request("http://127.0.0.1:5001/spotify/track/"+track['id']+"/audio-analysis", format=None)
        artist__lyrics_info_musixmatch = send_request("http://127.0.0.1:5002/musixmatch/lyric/" + artist + "/" + track['name'], format=None)
        lyrics = ''
        if(artist__lyrics_info_musixmatch['message']['header']['status_code'] != 404):
                lyrics = artist__lyrics_info_musixmatch['message']['body']['lyrics']['lyrics_body']
        if lyrics:
            r['tracks'].append({'name' : track['name'], 'lyrics' : lyrics, 'audio-analysis' : track_audio_analysis_spotify})
    return jsonify(r)   

if __name__ == '__main__':
    app.run(port=5000, debug=True)