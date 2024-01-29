from tkinter import N
import numpy as np
import pyaudio
import time
import librosa
from librosa import feature

#many thanks to https://stackoverflow.com/questions/59056786/python-librosa-with-microphone-input
class RealTimeAudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.stream = None

    def start(self):
        self.p = pyaudio.PyAudio()
        # for reading from mic
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  stream_callback=self.callback,
                                  frames_per_buffer=self.CHUNK)
        # self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
        #             frames_per_buffer=self.CHUNK)


    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        print(frame_count, time_info, flag)
        librosa.feature.mfcc(y=numpy_array)
        tempo, beats = librosa.beat.beat_track(y=numpy_array)
        print(tempo, beats)
        return None, pyaudio.paContinue

    def mainloop(self):
        while (self.stream.is_active()): # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            time.sleep(2.0)


audio = RealTimeAudioHandler()
audio.start()     # open the the stream
audio.mainloop()  # main operations with librosa
audio.stop()