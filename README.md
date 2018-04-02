# MusicPy

This tool aims to create a karaoke version from the song available on spotify and lyrics available through musixmatch.

Currently, this version contains two services and a RESTful API:

- spotify.py: service that uses the spotify api. All usable routes are accessible at http://127.0.0.1:5001/
- musixmatch.py: service that uses the api musixmatch. All usable routes are accessible at http://127.0.0.1:5002/
- gateway.py: service that provides information from spotify and musixmatch. All usable routes are accessible at http://127.0.0.1:5000/

For the moment, the use is done by an artist name belonging to the list available at the address http://127.0.0.1:5000/artists


Obviously the request to retrieve the 10 best-known pieces of an artist with lyrics and audio analysis does not make much sense but gives an idea of what is feasible.

Similarly, the job of matching lyrics to audio analysis has not been done.

## Install

Python Version >= 3.4

`pip3 install requirements.txt`


## Config

Configuration

The file `MusicPy/src/config.py` makes it possible to define the authentication keys of the services Spotify and Musixmatch


## Note 

For the moment, MusicPy can only work if the Spotify and musixmatch services are well configured and usable. This is voluntary since the goal is to use both services simultaneously


## Launch

The easiest way to launch all the services is :

`cd MusicPy/src`

`python3 spotify.py & python3 musixmatch.py & python3 gateway.py`

Go to page http://127.0.0.1:5000/


## Examples

http://127.0.0.1:5000/

http://127.0.0.1:5000/artists/plastikman/tracks

Spotify results for artist Faithless

http://127.0.0.1:5001/spotify/artist/5T4UKHhr4HGIC0VzdZQtAE

Musixmatch results with lyrics for Faithless - Insomnia

http://127.0.0.1:5002/musixmatch/lyric/faithless/insomnia
