"""
Local client:
establishes a UDP connection to the server.
Sends list of microphones, audio/connection settings, then
continuously sends audio chunks


TODO: listen for server responses (mic changes, setting changes)
TODO: make this work as an executable
TODO: include soundcard, numpy libraries in final executable so no installs are required
TODO: *maybe* multicast to find the server
"""
import soundcard as sc
import numpy as np
import sys
import socket

# BUG: fuzzy search grabs loopback devices when given the name of the actual device (non-loopback)
# current solution: local client only uses ids, frontend is given id:name pairs and presents names
# to the user instead of ids

# UDP globals
SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 4242
# might want to split this array into multiple parts
BUF_SIZE = 8192

# connect to udp socket
sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

LOOPBACK = True
MAC = False

blocksize = 1024
samplerate = 48000

mics = sc.all_microphones(include_loopback=LOOPBACK)
new_mic = sc.default_microphone().id


print(f"number of mics: {len(mics)}")
sock.send(len(mics).to_bytes(len(mics)//255 + 1))
for mic in mics:
    message = mic.id
    if not MAC:
        message += "," + mic.name
    byte_message = bytearray(message, encoding='utf-8')
    print(f"sending: {byte_message.decode()}")
    sock.send(byte_message)

# going to want a consumer and producer thread... or maybe not
while True:
    try:
        chosen_mic = sc.get_microphone(new_mic, include_loopback=LOOPBACK)
        new_mic = chosen_mic.id
        with chosen_mic.recorder(samplerate=samplerate, blocksize=blocksize) as mic:
            current_id = chosen_mic.id
            # the first chunk will just be disgarded because we need the settings
            # not too worried about disgaring it because we dont have to worry about
            # playing audio and dropping one packet isnt the end of the world
            raw_chunk = np.abs(mic.record(numframes=None))
            settings = str(BUF_SIZE) + "," + str(blocksize) + "," + str(samplerate) + "," + str(raw_chunk.dtype) + "," + "|".join(str(val) for val in raw_chunk.shape)
            print(settings)
            byte_message = bytearray(settings, encoding='utf-8')
            sock.send(byte_message)
            while current_id == new_mic:
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

                # sending as bytes - to convert back will need the data type and the original shape of the array
                b = data.tobytes()
                sock.send(b)
                print(f'latency: {mic.latency}')

        
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
