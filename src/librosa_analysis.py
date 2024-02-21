import librosa
import numpy as np

def getData(chunk, samplerate):
    pulses = librosa.beat.plp(y=chunk, sr=samplerate)
    pulses_avg = np.average(pulses)
    pulse_bar = "=" * int(50 * pulses_avg)
    return {"pulse": pulses_avg, "pulse_bar": pulse_bar}