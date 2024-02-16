import soundcard as sc
import numpy as np
import sys
import requests
from time import time_ns, time

DOCKER_IP="http://192.168.86.34:8000/audio_in"

RECORD = True

speakers = sc.all_speakers()
mics = sc.all_microphones(include_loopback=True)

print("all devices:")
print("\n".join(f"{i.id} {i.name}" for i in speakers))
print("\n".join(f"{i.id} {i.name}" for i in mics))

default_mic = sc.default_microphone()
default_speaker = sc.default_speaker()
chosen_mic = sc.get_microphone("alsa_output.usb-Corsair_CORSAIR_VIRTUOSO_XT_Wireless_Gaming_Receiver_16cad14300030215-00.pro-output-0.monitor", include_loopback=True)

print(f"defaults:\nmic: {default_mic}\nspeaker: {default_speaker}")
print(f"chosen mic: {chosen_mic}")

# look at this:
# https://soundcard.readthedocs.io/en/latest/#latency
# with default settings latency is ~2 seconds
# following the recomendations in the documentation, latency got down to ~0.2 seconds on one laptop
# laptop with different audio setup started with low latency and the latency quickly climbed
# changing the blocksize to 512 instead of 256 reduced the latency to a consistent 0.011 seconds

if not RECORD:
    sys.exit(0)

with chosen_mic.recorder(samplerate=48000, blocksize=512) as mic:
    while True:
        try:
            # numframes is how many samples are part of each chunk
            # higher values mean larger (less sensitive) chunks
            # however, higher frames are also easier on us because it means
            # fewer post requests
            # setting it to None returns the audio as soon as we get it
            # the actual number of frames in each chunk is the block size
            record_time = time()
            data = np.abs(mic.record(numframes=None))
            avg = np.average(np.abs(data))
            peak = np.max(np.abs(data))

            #bars = "#" * int(avg * 50)
            #max_bars = "-" * int((50 * peak) - (50 * avg))
            #print(data)
            #print(f"{len(data)} {bars + max_bars}")
            payload = {
                "avg": avg,
                "peak": peak,
                "post time": time_ns()
            }
            send_time =  time() - record_time
            response = requests.post(DOCKER_IP, data=payload).text
            receive_time = time() - record_time
            #print(f"{receive_time:4.3f} {send_time:4.3f} {response}")
            #rpeak = float(response['peak'])
            #ravg = float(response['avg'])
            #bars = "#" * int(ravg * 50)
            #max_bars = "-" * int((50 * rpeak) - (50 * ravg))
            print(f"latency: {mic.latency:4.3f} {response}")
        except KeyboardInterrupt:
            break
        # only works on linux
        