import os
import sys
import struct
import numpy as np
import time
import requests
import pyaudiowpatch as pyaudio

def translator():
    DOCKER_IP = "http://0.0.0.0:8000/"
    print("TRANSLATOR IS RUNNING")

    # open PyAudio manager via context manager
    with pyaudio.PyAudio() as p:
        # open audio stream via context manager
        with p.open(format=pyaudio.paInt32, channels=2, rate=48000, input=True, frames_per_buffer=1024) as stream:
            print("Recording started...")
            while True:
                # read a chunk of raw audio data from the stream
                raw_audio_data = stream.read(1024)

                # convert raw audio data to floating-point values
                float_audio_data = np.frombuffer(raw_audio_data, dtype=np.int32) / (2 ** 31)  # normalize to range [-1.0, 1.0]

                # gather audio data in real time
                data = np.abs(float_audio_data[-20:])
                avg = np.average(float_audio_data[-20:])
                peak = np.max(float_audio_data[-20:])

                payload = {
                    "avg": float(avg),
                    "peak": float(peak),
                    "data": data.tolist(),
                    "source": "Windows Device"
                }

                # send audio data to Docker container
                with requests.Session() as session:
                    response = session.post(DOCKER_IP + "audio_in", json=payload).json()

def main():
    # make sure the fifo file exists (if required)
    # not needed for Windows adaptation

    try:
        translator()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
