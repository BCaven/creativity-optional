#!/usr/bin/env python
import os
import struct
import numpy as np
import sys
import requests

def main():

    DOCKER_IP="http://0.0.0.0:8000/"

    # Open the named pipe for reading
    with sys.stdin.buffer.read() as pipe:
        # Number of bytes per sample (32-bit signed integer PCM)
        bytes_per_sample = 4

        # Convert raw audio data to floating-point values
        float_audio_data = []
        
        # Read raw audio data from the named pipe
        while True:
            # Read a chunk of raw audio data from the named pipe
            raw_audio_data = pipe.read(1024)  # Adjust buffer size as needed

            # Check if end of file is reached
            if not raw_audio_data:
                break

            # Iterate over raw audio data, convert each sample to a float
            for i in range(0, len(raw_audio_data), bytes_per_sample):
                # Extract sample as little-endian signed 32-bit integer
                sample_bytes = raw_audio_data[i:i+bytes_per_sample]
                sample = struct.unpack('<i', sample_bytes)[0]

                # Convert sample to floating-point value
                float_sample = sample / (2 ** 31)  # Normalize to range [-1.0, 1.0]
                
                # Append abs of float sample to float audio data
                float_audio_data.append(np.abs(float_sample))

            # Gather audio data in real time
            data = np.abs(float_audio_data[-20:])
            avg = np.average(float_audio_data[-20:])
            peak = np.max(float_audio_data[-20:])
            
            # Display audio graph
            #bars = "#" * int(50 * avg)
            #mbars = "-" * int((50 * peak) - (50 * avg))
            #print("local audio: " + bars + mbars)
            #print(f"[data: {data:.2f} avg: {avg:.2f} peak: {peak:.2f}]{'#' * int(peak * 100)}{'-' * int((peak - data) * 100)}")
            payload = {
                "avg": float(avg),
                "peak": float(peak),
                "data": data.tolist(),
                "source": "MacOS Device" #Currently hardcoded TODO: Fix
            }
            response = requests.post(DOCKER_IP + "audio_in", json=payload).json()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
