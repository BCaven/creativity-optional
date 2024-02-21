"""
Server that runs in the docker container

This server should call the blackbox processes and receive requests from the audio client
NOTE: technically, the "client" application "serves" raw audio to this application


Technical:
audio is posted to ip/audio_in
video should be available at ip/video/id

A Vue site should be the only thing that has direct communication with this application
it should not be available outside of the docker container (except MAYBE the video stream)
although for now it is available because the Vue site doesnt exist and I needed to test
the audio input

might want to open a second port for the audio if we are *slow* because of the constant audio requests
- this is not a concern at the moment

Server: Flask

TODO: make api calls for Vue front end 
TODO: decide on a format for the api calls
TODO: 
"""
from flask import Flask
from flask import request
from flask import jsonify
from time import time_ns

#we need to set NUMDA_CACHE_DIR before we import librosa
import os
os.environ[ 'NUMBA_CACHE_DIR' ] = '/tmp/'
from librosa_analysis import getData as getLibrosaData

app = Flask(__name__)
AUDIO_STR = ""
AUDIO_SOURCE = ""
AUDIO_CHUNK = []
ALL_AUDIO = {}
blockrate = 512
samplerate = 48000
librosa_data = {}
@app.route("/")
def main_page():
    return "<p>Hello world</p>"

@app.route("/audio_source", methods = ['POST'])
def audio_source():
    """
        This might end up being obsolete, but adding the header for now
    """
    global ALL_AUDIO
    global AUDIO_SOURCE
    global samplerate
    global blockrate
    if request.method == "POST":
        data = request.form
        if "mics" in data:
            ALL_AUDIO = data["mics"]
        if "source" in data:
            AUDIO_SOURCE = data["source"]
        if "samplerate" in data:
            samplerate = samplerate
        if "blockrate" in data:
            blockrate = blockrate
        return AUDIO_SOURCE
    return AUDIO_SOURCE


@app.route("/audio_in", methods=['GET', 'POST'])
def audio_in():
    """
        How the local application to the server.
        It is also called by the frontend UI to test the dynamic site,
        although this will likely change
    """
    # TODO: change this later, it is just for testing
    global AUDIO_STR
    global AUDIO_SOURCE
    global AUDIO_CHUNK
    global librosa_data
    if request.method == 'POST':
        data = request.form
        AUDIO_CHUNK = data['data']
        rpeak = float(data['peak'])
        ravg = float(data['avg'])
        bars = "#" * int(50 * ravg)
        mbars = "-" * int((50 * rpeak) - (50 * ravg))
        AUDIO_STR = bars + mbars

        #get librosa data
        if samplerate:
            librosa_data = getLibrosaData(AUDIO_CHUNK, samplerate)

        response = {"bars": AUDIO_STR}
        if "source" in data:
            if data["source"] != AUDIO_SOURCE:
                print(AUDIO_SOURCE)
                response["source"] = AUDIO_SOURCE
        response = jsonify(response)
        #response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        response = jsonify({"bars": AUDIO_STR, "source": AUDIO_SOURCE, "librosa_data": librosa_data})
        # TODO: the actual CORS policy
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
