#!/usr/bin/env python
import pyaudio
import numpy as np
import requests
import json

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
DOCKER_IP="http://0.0.0.0:8000/"

# Find the index of the desired input device
def find_input_device_index(p, device_name):
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info["name"] == device_name:
            return i
    raise ValueError(f"Input device '{device_name}' not found")

# Specify the microphone input device name
MIC_NAME = "BlackHole 2ch"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Find the index of the specified microphone
mic_index = find_input_device_index(p, MIC_NAME)

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=CHUNK)

print("* Recording")

try:
    while True:
        # Read audio data from the stream
        raw_data = stream.read(CHUNK)
        
        # Convert binary data to numpy array
        data = np.frombuffer(raw_data, dtype=np.int16)

        # this makes the data small enough for me to see the cube (it'd be ~10,000 otherwise)
        data = data / max(1, np.max(data)) / 2
        
        avg = np.average(np.abs(data))
        peak = np.max(np.abs(data))
        

        payload = {
            "avg": float(avg),
            "peak": float(peak),
            "data": data.tolist(),
            "source": MIC_NAME
        }
        response = requests.post(DOCKER_IP + "audio_in", json=payload).json()

        # Print the audio data
        #print(audio_array)
                

except KeyboardInterrupt:
    print("* Stopped recording")

# Close the audio stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
