import soundcard as sc
import numpy as np
import sys
from websockets.sync.client import connect
import asyncio

# TODO: wss
# TODO: multicast discovery of server
DOCKER_WEB_SOCKET = "ws://0.0.0.0:800/"
LOOPBACK = False

blocksize = 1024
samplerate = 48000

# TODO: search for mic by id instead of name
# still want the user to pick from human readable names tho
mics = sc.all_microphones(include_loopback=LOOPBACK)
new_mic = sc.default_microphone().name


async def send_audio():
    """
    Continuously send audio data to the server via websocket.

    Need to restart the recorder with a different mic if a new mic is selected.
    TODO: restart if settings change
    TODO: search based on id instead of name
    """
    async with connect(DOCKER_WEB_SOCKET) as websocket:
        while True:
            # TODO: send list of microphones + current source + settings to server
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
                        payload = {
                            "avg": avg,
                            "peak": peak,
                            "data": data,
                            "source": current_name
                        }
                        await websocket.send(payload)
                        
                
            except KeyboardInterrupt:
                print("exiting...")
                sys.exit(0)

async def receive_settings():
    """
    Recieve stuff from the server via websocket, modifies global variables
    """
    async with connect(DOCKER_WEB_SOCKET) as websocket:
        while True:
            response = await websocket.recv()
            # do stuff with the response
            print(response)