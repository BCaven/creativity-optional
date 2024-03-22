from genericpath import exists
import os
import sys
import struct
import numpy as np
import time
import requests

def translator():
    DOCKER_IP="http://0.0.0.0:8000/"
    # Open the named pipe for reading
    with open('runtime/audio_pipe', 'rb') as pipe:
        # Number of bytes per sample (32-bit signed integer PCM)
        bytes_per_sample = 4

        # Convert raw audio data to floating-point values
        float_audio_data = []
        
        try:
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
                # print(data)
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
                print("Sending to " + DOCKER_IP + "audio_in")
                response = requests.post(DOCKER_IP + "audio_in", json=payload).json()
                print("return:", response)
            
        except KeyboardInterrupt:
            time.sleep(0.05)
            print("exiting...")
            # os.system("rm runtime/audio_pipe")
            sys.exit(0)


def main():
    mic = "BlackHole 2ch" # Input mic (BlackHole is for loopback, -d is default device microphone)
    mic = "-d"
    rate = 48000 # sampling rate (Hz)


    # Make sure the fifo file exists
    if not exists("runtime/audio_pipe"):
        os.system("mkfifo runtime/audio_pipe")
    
    #translator()

    pid = os.fork() #TODO: verify that this checks for errors correctly
    if pid == -1:
        print("error: falied to fork processes")
        
    if pid == 0:
        print("running translator...")
        translator()
    else:
        print("collecting audio...")
        os.system(f"""sox -r {rate} -c 2 -b 32 -e signed-integer -t coreaudio "{mic}" -t raw runtime/audio_pipe""")

if __name__ == "__main__":
    main()
