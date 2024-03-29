import soundcard as sc
import numpy as np
import sys
# will likely get rid of the `requests` library
import requests

# BUG: fuzzy search grabs loopback devices when given the name of the actual device (non-loopback)

DOCKER_IP="http://0.0.0.0:8000/"
LOOPBACK = False

blocksize = 2048
samplerate = 48000

mics = sc.all_microphones(include_loopback=LOOPBACK)
new_mic = sc.default_microphone().name

audio_devices = {
    "mics": [m.name for m in mics],
    "source": new_mic
}
# send the list
# for now we do not care about the response
_ = requests.post(DOCKER_IP + "audio_source", data=audio_devices)

while True:
    try:
        chosen_mic = sc.get_microphone(new_mic, include_loopback=LOOPBACK)
        new_mic = chosen_mic.name
        with chosen_mic.recorder(samplerate=samplerate, blocksize=blocksize) as mic:
            current_name = chosen_mic.name
            print(f"starting with: {current_name}")
            print(f"new mic name: {new_mic}")
            while current_name == new_mic:
                # the actual number of frames in each chunk is the block size
                # higher blocksize = easier on the system
                # higher blocksizes inherently have latency because they have to 
                # record the data before sending it
                # but smaller block sizes eventually have infinite latency because
                # the system cannot process the audio fast enough
                # TODO: write script to auto adjust the blocksize
                # TODO: section in Vue "options" for the user to change the blocksize
                data = np.abs(mic.record(numframes=None))
                avg = np.average(np.abs(data))
                peak = np.max(np.abs(data))

                # TODO: experiment with sending raw data
                # if you do, just add a new key called "data" with the raw np array
                #print(data)

                payload = {
                    "avg": float(avg),
                    "peak": float(peak),
                    "data": data.tolist(),
                    "source": current_name
                }
                response = requests.post(DOCKER_IP + "audio_in", json=payload).json()
                #print(response)
                if "source" in response:
                    # oh no we have to change audio devices
                    new_mic = response["source"]
                    print("switching mics")
                #bars = "#" * int(50 * avg)
                #mbars = "-" * int((50 * peak) - (50 * avg))
                #print("local audio: " + bars + mbars)
                # latency only works on linux
                print(f"latency: {mic.latency:4.3f} mic: {current_name[:6]} {response['bars']}")
        
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
