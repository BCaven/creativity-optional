"""
The protocol:
The client's first item is going to be the list of microphone names, ids, and which mic is currently being used
    csv:
        mic_name|mic_name|mic_name,mic_id|mic_id|mic_id,current_mic_name
The second is the settings:
    buf_size
    blocksize
    samplerate
    dtype
    shape
    etc
    formatted as a csv like the following:
        buf_size,blocksize,samplerate,dtype,shape

everything recieved after that is a np array of the raw audio stream
    these are sent as byte arrays which get converted to np arrays and readjusted to the correct shape

"""

import socket
import numpy as np

# UDP globals
SERVER_ADDR = "0.0.0.0"
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
mic_input = con.recv(BUF_SIZE)
print(mic_input)
# settings
raw_settings = con.recv(BUF_SIZE)
settings = {
    'dtype': np.float32,
    'shape': (1024, 2)
}
print(raw_settings)

while True:
    raw_data = con.recv(BUF_SIZE) 
    cleaned = np.array(raw_data, dtype=settings['dtype'])
    cleaned.shape = settings['shape']