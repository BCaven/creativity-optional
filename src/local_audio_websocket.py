import soundcard as sc
import numpy as np
import sys
from websockets.sync.client import connect
import asyncio

# TODO: wss
# TODO: multicast discovery of server
DOCKER_WEB_SOCKET = "ws://0.0.0.0:8000/"
loopback = False

blocksize = 1024
samplerate = 48000

# TODO: search for mic by id instead of name
# still want the user to pick from human readable names tho
mics = sc.all_microphones(include_loopback=loopback)
current_mic = sc.default_microphone()
new_mic = current_mic.id


async def get_audio(mic):
    """
    Get audio chunk

    TODO: make sure this actually works lol
    """
    return mic.record(numframes=None)

async def producer_handler(websocket):
    """
    Send audio chunks

    TODO: restart producer when the settings change
    """
    with current_mic.recorder(samplerate=samplerate, blocksize=blocksize) as mic:
        while current_mic.id == new_mic:
            data = await get_audio(mic)
            # TODO: add other stuff to this payload
            payload = {
                "data": data
            }
            await websocket.send(payload)
    current_mic = sc.get_microphone(new_mic, include_loopback=loopback)


async def consumer(message):
    """
    Process the websocket message
    """
    return

async def receive_handler(websocket):
    """
    Recieve stuff from the server via websocket, modifies global variables
    """
    async for message in websocket:
        await consumer(message)

async def handler(websocket):
    """
    Start consumer and producer tasks
    """
    consumer_task = asyncio.create_task(receive_handler(websocket))
    producer_task = asyncio.create_task(producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

async def main():
    """
    Connect and run
    """
    async with connect(DOCKER_WEB_SOCKET) as websocket:
        await handler(websocket)


if __name__ == "__main__":
    asyncio.run(main())