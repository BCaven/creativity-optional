"""
Send audio stream to Docker

TODO: stretch goal - use multicast to find docker container so the user does not need to manually pass the docker IP addr

Grab audio with pyaudio and send the raw chunks to the docker container using the requests package
"""
import requests
import pyaudio
import numpy as np
from time import time_ns
import sys

# Docker globals
DOCKER_IP="http://192.168.86.34:8000/audio_in"

# response code that signals time to shutdown
QUIT=400

# audio settings
# TODO: automatically find these by pinging the audio source
# TODO: check for loopback devices and make one if not already present
CHUNK = 2**11
RATE = 44100

def main():
    """
    Rocking and rolling but mostly crashing and burning.

    In the current setup: all computation should be done by the docker server, all this does is send the data.


    TODO: good sync method

    Initialization post:
    - sync information
    

    Post needs:
    - The packet
    - The timestamp of the packet
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=RATE,
                    input=True,
                    # default audio out
                    frames_per_buffer=CHUNK)
    while True:
        # TODO: make it so the docker server can kill this application
        try:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            # TODO: send data to docker
            peak = np.average(np.abs(data)) * 2
            max_val = np.max(data)
            payload = {
                "peak": peak,
                "max_val": max_val,
                "timestamp": time_ns()
            }
            response = requests.post(DOCKER_IP, data=payload).json()
            rpeak = float(response['peak'])
            rmax = float(response['max_val'])
            bars = "#" * int(100 * rpeak / 2 ** 16)
            mbars = "-" * int((100 * rmax / 2 ** 16) - (50 * rpeak / 2 ** 16))
            print("%05d %s" % (peak, bars + mbars))
            
            #peak = np.average(np.abs(data)) * 2
            #max_val = np.max(data)            
            #bars = "#" * int(50 * peak / 2 ** 16)
            #mbars = "-" * int((50 * max_val / 2 ** 16) - (50 * peak / 2 ** 16))
            #print("%05d %s" % (peak, bars + mbars))
            # tempo, beat_frames = librosa.beat.beat_track(y=data, sr=RATE)
            # print(f"tempo: {tempo}\nbeat_frames: {beat_frames}")
        except Exception:
            stream.stop_stream()
            stream.close()
            p.terminate()


if __name__ == "__main__":
    main()