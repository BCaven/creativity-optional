"""
Server that runs in the docker container

This server should call the blackbox processes and receive requests from the audio client
NOTE: technically, the "client" "serves" raw audio to this application


Technical:
audio is posted to ip/audio_in
video should be available at ip/video/id
the app should be avaliable at ip/

might want to open a second port for the audio if we are *slow* because of the constant audio requests


TODO: find good request handler
    For now just going to use the built in python https server
"""

import http.server
import socketserver



