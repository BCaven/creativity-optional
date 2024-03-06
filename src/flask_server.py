"""
Server that runs in the docker container

This is the http implementation

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
from flask import Flask, render_template
from flask import request
from flask import jsonify
import numpy as np
import logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='.')



audio_str = ""
audio_source = ""
# TODO: find a good way to store many past chunks (preferably both push and pop are o(1))
audio_chunk = []
all_audio = {}
@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/audio_source", methods = ['POST'])
def get_audio_source():
    """
        This might end up being obsolete, but adding the header for now
    """
    global all_audio
    global audio_source
    if request.method == "POST":
        data = request.form
        if "mics" in data:
            all_audio = data["mics"]
        if "source" in data:
            audio_source = data["source"]
        return audio_source
    else:
        return audio_source


@app.route("/audio_in", methods=['GET', 'POST'])
def audio_in():
    """
        How the local application to the server.
        It is also called by the frontend UI to test the dynamic site,
        although this will likely change
    """
    # TODO: change this later, it is just for testing
    global audio_str
    global audio_source
    global audio_chunk
    if request.method == 'POST':
        data = request.json
        #print(data)
        #print(data['data'])
        audio_chunk = np.array(data['data']).reshape(-1)
        rpeak = float(data['peak'])
        ravg = float(data['avg'])
        bars = "#" * int(50 * ravg)
        mbars = "-" * int((50 * rpeak) - (50 * ravg))
        audio_str = bars + mbars

        response = {"bars": audio_str}
        if "source" in data:
            if data["source"] != audio_source:
                print(audio_source)
                response["source"] = audio_source
        response = jsonify(response)
        #response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        response = jsonify({"bars": audio_str, "source": audio_source})
        # TODO: the actual CORS policy
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route("/pico_audio", methods=['GET'])
def pico_audio():
    """
    Do a FFT and return the data
    """
    num_motors = 8
    if len(audio_chunk) > 0:
        #return audio_chunk.tolist()
        fft = np.fft.fft(audio_chunk).real
        chunk_size = fft.size / num_motors
        avg_chunks = np.abs(np.average(fft.reshape(-1, int(chunk_size)), axis=1))
        normalized_chunks = avg_chunks # / avg_chunks.size
        return jsonify({"motors": normalized_chunks.tolist()})
    else:
        return [0, 0, 0, 0, 0, 0, 0, 0]

if __name__ == "__main__":
    app.run()