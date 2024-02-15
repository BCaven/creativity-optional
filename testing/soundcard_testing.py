import soundcard as sc
import numpy as np
import sys
import requests

DOCKER_IP="http://192.168.86.34:8000/audio_in"

RECORD = True

speakers = sc.all_speakers()
mics = sc.all_microphones(include_loopback=True)

print("all devices:")
print(speakers)
print(mics)

default_mic = sc.default_microphone()
default_speaker = sc.default_speaker()

print(f"defaults:\nmic: {default_mic}\nspeaker: {default_speaker}")

# look at this:
# https://soundcard.readthedocs.io/en/latest/#latency
# with default settings latency is ~2 seconds
# following the recomendations in the documentation, latency got down to ~0.2 seconds

if not RECORD:
    sys.exit(0)

with default_mic.recorder(samplerate=48000, blocksize=256) as mic:
    while True:
        try:
            # numframes is how many samples are part of each chunk
            # higher values mean larger (less sensitive) chunks
            # however, higher frames are also easier on us because it means
            # fewer post requests
            # setting it to None returns the audio as soon as we get it
            # the actual number of frames in each chunk is the block size
            data = np.abs(mic.record(numframes=None))
            avg = np.average(np.abs(data))
            peak = np.max(np.abs(data))

            #bars = "#" * int(avg * 50)
            #max_bars = "-" * int((50 * peak) - (50 * avg))
            #print(data)
            print(f"{len(data)} {bars + max_bars}")
            payload = {
                "avg": avg,
                "peak": peak
            }
            response = requests.post(DOCKER_IP, data=payload).json()
            rpeak = float(response['peak'])
            ravg = float(response['avg'])
            bars = "#" * int(ravg * 50)
            max_bars = "-" * int((50 * rpeak) - (50 * ravg))
        except KeyboardInterrupt:
            break
        # only works on linux
        #print(f"latency: {mic.latency}")