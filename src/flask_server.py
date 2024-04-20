"""
Server that runs in the docker container
It serves the pre-built vue frontend

NOTE: technically, the "client" application "serves" raw audio/data to this application


Technical:
audio is posted to ip/audio_in
video should be available at ip/output and ip/output/stream


might want to open a second port for the audio if we are *slow* because of the constant audio requests
- this is not a concern at the moment

Server: Flask

Tasks:
[TODO] support caching for general data
[TODO] handle general data
[TODO] make general data accessable to frontend via api calls for specific keys
[TODO] add route to send available keys to frontend
[TODO] clean up audio handling
[TODO] deal with keep-alive connections
[TODO] websockets

"""
from flask import Flask, render_template, request, jsonify, abort
from flask_socketio import SocketIO, emit
from werkzeug.serving import WSGIRequestHandler
import numpy as np
import logging


flask_app = Flask(__name__, template_folder='.')
flask_app.logger.setLevel(logging.DEBUG)
socketio = SocketIO(flask_app)

audio_str = ""
audio_raw_max = 0
AUDIO_SAVED_CHUNKS = 5
audio_last = []
audio_max_last = audio_raw_max
# TODO: find a good way to store many past chunks (preferably both push and pop are o(1))
audio_chunk = []
# TODO: gracefully handle client settings
change_settings = False
client_audio_settings = dict()
json_settings_path = 'node-settings.json'

# general data
general_data = dict()


@flask_app.route("/")
def main_page():
    return render_template('index.html')

@flask_app.route("/audio_settings", methods = ['GET', 'POST'])
def get_audio_settings():
    """
    This might end up being obsolete, but adding the header for now
    """
    global client_audio_settings
    global change_settings
    if request.method == "POST":
        data = request.form
        response = {}
        flask_app.logger.info(f"received {data}")
        if "settings" in data:
            response['message'] = f"Updated: {','.join(token for token in data['settings'])}"
            for token in data['settings']:
                client_audio_settings[token] = data[token]
            change_settings = True
        else:
            response['message'] = "Error: settings must be a dict in a 'settings' key"
        return jsonify(response)
    else:
        return jsonify({"settings": client_audio_settings})


@flask_app.route("/audio_in", methods=['GET', 'POST'])
def audio_in():
    """
    HTTP implementation to send audio data to server
    Keeping it for compatability
    How the local application to the server.
    It is also called by the frontend UI to test the dynamic site,
    although this will might change in the future.
    When compared to performance of minimal udp packets, there was only a difference of 0.01 seconds of latency (0.22 vs 0.21)


    TODO: change how setting changes are communicated back to the client
    client is expecting 'settings' key that contains any updated settings
    """
    # TODO: change this later, it is just for testing and the MVP apparently
    global audio_str
    global audio_source
    global audio_chunk
    global audio_raw_max
    global audio_last
    global audio_max_last
    global AUDIO_SAVED_CHUNKS
    global change_settings
    if request.method == 'POST':
        data = request.json
        audio_chunk = np.array(data['data']).reshape(-1)
        rpeak = float(data['peak'])
        ravg = float(data['avg'])
        audio_raw_max = rpeak
        # NOTE: all of this computation is better done in a celery task, but since those arent set up yet,
        # doing basic analysis here
        # NOTE: celery tasks may never be implemented because we no longer have a need for them (no librosa)
        audio_last.append(rpeak)
        if (len(audio_last) > AUDIO_SAVED_CHUNKS):
            audio_last.pop(0)

        audio_max_last = max(audio_last)
        bars = "#" * int(50 * ravg)
        mbars = "-" * int((50 * rpeak) - (50 * ravg))
        audio_str = bars + mbars
        response = {"bars": audio_str}

        if change_settings:
            response['setting_change'] = change_settings
            change_settings = False
        return jsonify(response)
    else:
        response = jsonify({"bars": audio_str, "peak": audio_max_last, "source": audio_source})
        # TODO: the actual CORS policy
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@flask_app.route("/general_in", methods=['POST'])
def general_in():
    """
    Recieve misc information of the form
    { 
    key: data,
    type: type(data)
    }

    At the moment, only int is supported as a data type and
    all data is assumed to be a range between 0 and 100
    """
    global general_data
    assert request.method == 'POST', "the route /general_in only supports POSTs"
    data = request.json
    assert 'type' in data, "request to /general_in did not specify the data type"
    for key in data:
        if key == 'type':
            continue
        flask_app.logger.info(f"Updating general data: {key}: {data[key]}")
        general_data[key] = data[key]
        # send new data over to the front-end
        emit('incoming data', data)
    response = {"message": f"received data for {key in data if key != 'type' else ''}"}
    return jsonify(response)

@flask_app.route("/general_keys", methods=['GET'])
def general_keys():
    """
    Return a list of all known general_data keys
    """
    response = {"keys": [key for key in general_data]}
    return jsonify(response)

@flask_app.route("/general_keys/<string:key>", methods=['GET'])
def get_key(key):
    """
    Return the data for a specific key

    This route will be used by the front-end to pull each key when it has been updated
    """
    response = {}
    if key in general_data:
        response[key] = general_data[key]
    else:
        abort(404)
    
    return jsonify(response)

@flask_app.route("/page_settings", methods=['GET'])
def send_initial_settings():
    """
    Send the json settings file to the front-end

    This should be called once on startup
    """
    response = {}
    # load json
    with open(json_settings_path, 'r') as f:
        pass
    # send json
    return jsonify(response)

    
@flask_app.route("/fft_audio", methods=['GET'])
def fft_audio():
    """
    Do a FFT and return the data
    TODO: shift array to only capture useful frequency range
    """
    num_motors = 8
    if len(audio_chunk) > 0:
        #return audio_chunk.tolist()
        fft = np.fft.fft(audio_chunk).real
        chunk_size = fft.size / num_motors
        avg_chunks = np.abs(np.average(fft.reshape(-1, int(chunk_size)), axis=1))
        normalized_chunks = avg_chunks # / avg_chunks.size
        return jsonify({"frequencies": normalized_chunks.tolist()})
    else:
        return jsonify({'frequencies': [0, 0, 0, 0, 0, 0, 0, 0]})


@flask_app.route("/output", methods=['GET'])
def output_page():
    """
    Display just the threejs scene.
    This is how other programs get our output (as html)
    """
    return render_template("outputscene/outputscene.html")

@flask_app.route("/output/stream", methods=['GET'])
def output_stream():
    """
    Serve next frame of video

    Plan:
    use the server-side rendering aspects of threejs
    that most likely means we will have a node application constantly rendering the scene that output images to a folder
    this method then grabs the most recent one and sends it to the client

    this would *only* be useful when running the server on a second device because it would introduce more overhead
    that and, why send it back and forth if you are just rendering locally anyways
    """
    return jsonify({'error': 'not implemented, look at creativity-optional wiki'})

@flask_app.errorhandler(404)
def page_not_found(error):
    """
    Error page.
    May someone please make this
    """
    return "page not found", 404

# sockets!
@socketio.on("message")
def handle_message(data):
    """
    use a websocket to talk to the frontend
    """
    flask_app.logger.info(f"recieved {data}")

@socketio.on('connect')
def connect():
    flask_app.logger.info("Someone connected to the websocket!")
    emit('my response', {'data': 'Connected'})

    

if __name__ == "__main__":
    """
    Start the server


    NOTE: this is a development server and will need to be changed when rolling out
    using this for development only (although who knows, if you see this in the next release, plz submit
    a pr to fix it :D)
    """
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    socketio.run(flask_app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=8000)