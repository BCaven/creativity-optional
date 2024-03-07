"""
The protocol:
The client's first item is going to be the list of microphone names, ids, and which mic is currently being used
Unfortunately, these cannot be guarenteed to be smaller than buf_size so they
are going to be sent in separate messages

The second is the settings:
    buf_size
    blocksize
    samplerate
    dtype
    shape
    etc
    formatted as a csv like the following:
        buf_size,blocksize,samplerate,dtype,shape|shape|shape

everything recieved after that is a np array of the raw audio stream
    these are sent as byte arrays which get converted to np arrays and readjusted to the correct shape

TODO: support for multiple clients


Celery
TODO: celery support
"""

import socket
import numpy as np
import sys

def udp_server():
    # UDP globals
    SERVER_ADDR = "127.0.0.1"
    SERVER_PORT = 4242
    # might want to split this array into multiple parts
    BUF_SIZE = 8192

    sock = socket.socket() # UDP
    sock.bind((SERVER_ADDR, SERVER_PORT))
    sock.listen(1)
    con = None
    con, addr = sock.accept()
    print("client connected from", addr)
    # mic list
    num_mics = con.recv(BUF_SIZE)
    print("raw num mics:", num_mics)
    try:
        num_mics = int.from_bytes(num_mics)
    except ValueError as error:
        print(error)
        sock.close()
        sys.exit(1)

    all_microphones = {}
    for i in range(num_mics):
        raw_in = con.recv(BUF_SIZE).decode().split(",")
        if len(raw_in) == 1:
            # mac gang
            # to keep the rest of the program the same, we are going to
            # pretend that mac ids and names are the same thing
            all_microphones[raw_in[0]] = raw_in[0]
        elif len(raw_in) == 2:
            # id: name
            all_microphones[raw_in[0]] = raw_in[1]
        else:
            sock.close()
            raise ValueError(f"failed to parse incoming mic id,name pairs.\nWas expecting either 1 or 2 values, got {len(raw_in)}")
    print(all_microphones)   

    # settings
    raw_settings = con.recv(BUF_SIZE).decode().split(",")
    assert len(raw_settings) == 5, f"recieved the wrong number of settings, expected 5, got {len(raw_settings)}"
    # this order is always the same, so the spots will be hardcoded
    settings = {
        'buf_size': int(raw_settings[0]),
        'blocksize': int(raw_settings[1]),
        'samplerate': int(raw_settings[2]),
        'dtype': raw_settings[3],
        'shape': tuple(int(i) for i in raw_settings[4].split("|"))
    }
    print(settings)
    assert settings['buf_size'] == BUF_SIZE, f"bufsize failed to match: {settings['buf_size']} != {BUF_SIZE}"

    while True:
        try:
            raw_data = con.recv(BUF_SIZE) 
            cleaned = np.frombuffer(raw_data, dtype=settings['dtype'])
            cleaned.shape = settings['shape']
            avg = np.average(np.abs(cleaned))
            peak = np.max(np.abs(cleaned))
            print(f"avg: {avg:6.4f} peak: {int(peak * 100) * '#'}")
        except ValueError:
            print("whoops, bad packet")
            print(raw_data)
            return False
            