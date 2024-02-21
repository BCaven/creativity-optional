from elgato_light_strip import Room
import requests
from time import sleep
DOCKER_IP="http://192.168.86.34:8000/audio_in"

room = Room()
room.setup()
print(room.lights)

while True:
    try:
        response = requests.get(DOCKER_IP).text
        #print(response)
        # on, hue, saturation, brightness
        room.room_color(1, 240, 100, min(100, len(response) * 2))
        sleep(0.005)
    except KeyboardInterrupt:
        break