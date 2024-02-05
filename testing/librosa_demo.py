#!/usr/bin/env python3
"""
Using librosa on pyaudio stream.

Librosa functions require the audio data (numpy array)
and the sampling rate of that audio data

This will be helpful: https://librosa.org/doc/latest/tutorial.html#quickstart

NOTE: https://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time
"""

import pyaudio
import numpy as np
import librosa

CHUNK = 2**11
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                # default audio out
                frames_per_buffer=CHUNK)


# only go for a few seconds
for i in range(int(20*44100/1024)):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    peak = np.average(np.abs(data)) * 2
    bars = "#" * int(50 * peak / 2 ** 16)
    max_val = np.max(data)
    mbars = "-" * int((50 * max_val / 2 ** 16) - (50 * peak / 2 ** 16))
    print("%04d %05d %s" % (i, peak, bars + mbars))
    # tempo, beat_frames = librosa.beat.beat_track(y=data, sr=RATE)
    # print(f"tempo: {tempo}\nbeat_frames: {beat_frames}")


stream.stop_stream()
stream.close()
p.terminate()
