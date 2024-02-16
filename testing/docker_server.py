"""
Server that runs in the docker container

This server should call the blackbox processes and receive requests from the audio client
NOTE: technically, the "client" "serves" raw audio to this application


Technical:
audio is posted to ip/audio_in
video should be available at ip/video/id

A Vue site should be the only thing that has direct communication with this application
it should not be available outside of the docker container (except MAYBE the video stream)
although for now it is available because the Vue site doesnt exist and I needed to test
the audio input

might want to open a second port for the audio if we are *slow* because of the constant audio requests


Server: Flask

TODO: make api calls for Vue front end 
"""
from flask import Flask
from flask import request
from time import time_ns

app = Flask(__name__)
AUDIO_STR = ""
@app.route("/")
def main_page():
    return "<p>Hello world</p>"


@app.route("/audio_in", methods=['GET', 'POST'])
def audio_in():
    # TODO: change this later, it is just for testing
    global AUDIO_STR
    if request.method == 'POST':
        data = request.form
        receive_time = time_ns()
        if "peak" in data:
            ravg = float(data['avg'])
            rpeak = float(data['peak'])
            bars = "#" * int(50 * ravg)
            mbars = "-" * int((50 * rpeak) - (50 * ravg))
            AUDIO_STR = bars + mbars
            return bars + mbars
        return data
    else:
        return f"<p>audio: {AUDIO_STR}</p>"
