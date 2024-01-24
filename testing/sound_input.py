#!/usr/bin/env python3.11
"""
Continuously read input stream.

Original code from here: https://stackoverflow.com/questions/48653745/continuesly-streaming-audio-signal-real-time-infinitely-python
"""

import pyaudio
import numpy as np
import sys
import matplotlib.pyplot as plt

RATE = 44100
CHUNK = int(RATE/20)  # RATE / number of updates per second


def soundplot(stream):
    """Plot stream."""
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    return data


if __name__ == "__main__":
    plt.ion()
    fig = plt.figure()
    x = np.linspace(0, RATE, CHUNK)
    y = np.linspace(0, RATE, CHUNK)
    ax = fig.add_subplot(111)
    line1, = ax.plot(x, y, 'r-')  # Returns a tuple of line objects, thus the comma

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    for i in range(sys.maxsize**10):
        data = soundplot(stream)
        line1.set_ydata(data)
        fig.canvas.draw()
        fig.canvas.flush_events()
    stream.stop_stream()
    stream.close()
    p.terminate()
