import soundcard as sc
import numpy as np
import sys
import socketio
import asyncio
import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)

# TODO: wss
# TODO: multicast discovery of server
DOCKER_WEB_SOCKET = "http://0.0.0.0:5000/"
RUNNING = True
loopback = False

blocksize = 1024
samplerate = 48000

# TODO: search for mic by id instead of name
# still want the user to pick from human readable names tho
mics = sc.all_microphones(include_loopback=loopback)
current_mic = sc.default_microphone()
new_mic = current_mic.id
sio = socketio.AsyncClient()


async def get_audio(mic):
    """
    Get audio chunk

    TODO: make sure this actually works lol
    """
    return mic.record(numframes=None).tolist()

async def send_audio():
    """
    Send audio chunks

    TODO: restart producer when the settings change
    """
    global current_mic, samplerate, blocksize, RUNNING, sio
    if sio is None:
        print("sio undefined")
        return
    with current_mic.recorder(samplerate=samplerate, blocksize=blocksize) as mic:
        print(f"Mic: {current_mic.name}")
        while current_mic.id == new_mic and RUNNING:
            try:
                data = await get_audio(mic)
                # TODO: add other stuff to this payload
                #print(f"sending data: {data}")
                payload = {
                    "data": data
                }
                print("sending data...")
                await sio.emit('audio_in', payload)
            except KeyboardInterrupt:
                RUNNING = False
                return
    current_mic = sc.get_microphone(new_mic, include_loopback=loopback)


@sio.event
async def message(data):
    """
    Handle messages from the server
    """
    print(f"recieved message: {data}")

@sio.event
async def connect():
    print("Connected")

@sio.event
async def connect_error(data):
    global RUNNING
    print(f"failed to connect: {data}")
    RUNNING = False

@sio.event
async def disconnect():
    global RUNNING
    print("disconnected from the server")
    RUNNING = False

async def main():
    """
    Connect and run
    """
    global RUNNING
    await sio.connect(DOCKER_WEB_SOCKET)
    #await send_audio()
    await sio.wait()
    await sio.disconnect()
        

if __name__ == "__main__":
    asyncio.run(main())