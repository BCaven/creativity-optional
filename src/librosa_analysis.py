import librosa
import numpy as np

class Analyzer:
    def __init__(self, numChannels=1):
        self.audioChunks = np.zeros((0, numChannels))
        self.lengths = [] #contains lengths of last eight blocks
    
    def readData(self, chunk, samplerate):
        # print("##############################\nLIBROSA\n##################################")
        #append data to the collected chunks
        self.audioChunks = np.append(self.audioChunks, chunk)
        self.lengths.append(chunk.shape[0])

        #remove oldest audio chunk data. We keep only eight newest chunks
        if (len(self.lengths) > 8):
            self.audioChunks = self.audioChunks[self.lengths.pop(0):]
        
        #feed data into librosa and get only the data pertaining to new portion
        # print(self.lengths[-1])
        pulses = librosa.beat.plp(y=self.audioChunks, sr=samplerate, win_length=self.lengths[-1])
        # print(pulses)
        # print(pulses.shape[0])
        pulses_avg = np.average(pulses)
        pulse_bar = "=" * int(50 * pulses_avg)
        return {"pulse": pulses_avg, "pulse_bar": pulse_bar}