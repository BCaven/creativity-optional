import soundcard as sc
import numpy as np
import sys
import socket

# BUG: fuzzy search grabs loopback devices when given the name of the actual device (non-loopback)

# UDP globals
SERVER_ADDR = "0.0.0.0"
SERVER_PORT = 4242
# might want to split this array into multiple parts
BUF_SIZE = 8192

# connect to udp socket
sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

LOOPBACK = False

blocksize = 1024
samplerate = 48000

mics = sc.all_microphones(include_loopback=LOOPBACK)
new_mic = sc.default_microphone().name

audio_devices = "|".join([m.name for m in mics]) + "," + "|".join([m.id for m in mics]) + "," + new_mic
sock.send(audio_devices)
# send the list
# for now we do not care about the response
#_ = requests.post(DOCKER_IP + "audio_source", data=audio_devices)

# going to want a consumer and producer thread... or maybe not
while True:
    try:
        chosen_mic = sc.get_microphone(new_mic, include_loopback=LOOPBACK)
        new_mic = chosen_mic.name
        with chosen_mic.recorder(samplerate=samplerate, blocksize=blocksize) as mic:
            current_name = chosen_mic.name
            settings = ""
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
                # sending as bytes - to convert back will need the data type and the original shape of the array
                #print("original")
                #print(data)
                #print(data.shape)
                #t = data.dtype
                #shape = data.shape
                #print("bytes")
                b = data.tobytes()
                #print(b)
                #print("converted back")
                #con = np.frombuffer(b, dtype=t)
                #con.shape = shape
                #print(con)

                sock.send(b)

        
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
