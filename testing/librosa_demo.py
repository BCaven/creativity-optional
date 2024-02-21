#!/usr/bin/env python3
"""
Using librosa on pyaudio stream.

Librosa functions require the audio data (numpy array)
and the sampling rate of that audio data

This will be helpful: https://librosa.org/doc/latest/tutorial.html#quickstart

NOTE: https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time

TODO: turn this into a generator

TODO: get loopback devices

TODO: make a pub sub server out of this
"""

import pyaudio
import numpy as np
import librosa
import dynamic2

CHUNK = 2**11
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


# go until keyboard interupt is received
while True:
    try:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        bars = "#" * int(100 * peak / 2 ** 16)
        max_val = np.max(data)
        mbars = "-" * int((50 * max_val / 2 ** 16) - (50 * peak / 2 ** 16))
        dynamic2.imageLoop(peak)
        print("%05d %s" % (peak, bars + mbars))
        # tempo, beat_frames = librosa.beat.beat_track(y=data, sr=RATE)
        # print(f"tempo: {tempo}\nbeat_frames: {beat_frames}")
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
