"""
The idea is that we have a list of tasks which get started by the flask server

Most of these are related to image processing
but there will also be some for interfacing with local audio applications


"""
from celery.signals import worker_ready
from celery import shared_task
import socket
import numpy as np
import sys

# UDP globals
SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 4242
# might want to split this array into multiple parts
BUF_SIZE = 8192

@worker_ready.connect(ignore_result=False)
def start_udp_server():
    """
    Start UDP server on startup
    
    
    This server should automatically update the audio buffer when a new packet is recieved
    I guess that goes in the metadata of the process?
    Not super sure, will have to look

    TODO: send settings to Flask Server
    TODO: recieve settinsg update from flask server and send the new settings back to the client
    TODO: audio buffer
    """
    global SERVER_ADDR, SERVER_PORT, BUF_SIZE

    sock = socket.socket() # UDP
    sock.bind((SERVER_ADDR, SERVER_PORT))
    sock.listen(1)
    con = None
    con, addr = sock.accept()
    return sock, con, addr

@shared_task(ignore_result=False)
def get_udp_settings(sock, con, addr):
    """
    Once the client has made a udp connection, we need to get the settings
    """
    global BUF_SIZE
    print("client connected from", addr)
    # mic list
    num_mics = con.recv(BUF_SIZE)
    print("raw num mics:", num_mics)
    try:
        num_mics = int.from_bytes(num_mics)
    except ValueError as error:
        print(error)
        sock.close()
        # reraise the error
        raise ValueError(error)
        #sys.exit(1)

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
    assert settings['buf_size'] == BUF_SIZE, f"bufsize failed to match: {settings['buf_size']} != {BUF_SIZE}"
    return all_microphones, settings

@shared_task(ignore_result=False)
def get_audio_chunk(sock, connection, settings):
    """
    Get the next audio chunk from the server
    
    """
    global BUF_SIZE
    try:
        raw_data = connection.recv(BUF_SIZE) 
        cleaned = np.frombuffer(raw_data, dtype=settings['dtype'])
        cleaned.shape = settings['shape']
        # append the cleaned shape to the audio buffer
        return cleaned
        
    except ValueError as error:
        print("whoops, bad packet")
        sock.close()
        # reraise the error
        raise ValueError(error)
        