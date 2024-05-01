"""
Creativity Optional
local audio client based on soundcard

tested on windows and linux, unreliable on mac

please submit bugs to https://github.com/BCaven/creativity-optional/issues

this is supposed to be a background task started with cron/equivalent
settings should be changed either through the command line arguments or through
the creativity-optional frontend

Tasks:
[DONE]: finish transition to functions
[DONE]: look into async httpx
[DONE]: command line arguments
[TODO]: write usage function
[TODO]: write an equivalent using pyaudio and pyaudio(WASPI patch)
"""
import soundcard as sc
import numpy as np
import sys
import requests
import logging
logging.basicConfig(format='[%(levelname)s] %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
session = requests.Session()



def usage(return_val: int):
    print("""
please write this...

""")
    sys.exit(return_val)


def send_settings(ip: str, settings: dict) -> bool:
    """
    Send all settings
    Runs when the application starts and if it is requested by the server

    Returns if the function ran successfully
    """
    # send the settings dict
    # for now we do not care about the response
    try:
        logging.info(f"sending settings: {settings}")
        _ = session.post(ip + "audio_settings", json=settings)
    except requests.exceptions.ConnectionError:
        logging.warning("The server did not respond, is it running?")
        return False
    return True

def update_settings(ip: str, settings: dict) -> bool:
    """
    ask the server for new settings
    """
    try:
        response = session.get(ip + "audio_settings")
        jresponse = response.json()
        assert 'settings' in jresponse, f"malformed response from server - no 'settings' key"
        for token in jresponse['settings']:
            settings[token] = jresponse['settings'][token]
        logging.info(f"settings got updated: {settings}")
    except requests.exceptions.ConnectionError:
        logging.warning("The server did not respond, is it running?")
        return False
    return True



def send_audio(chosen_mic, ip: str, settings: dict) -> bool:
    """
    Continuously send audio from the current settings until the server responds with new settings
    the actual number of frames in each chunk is the block size
    higher blocksize = easier on the system
    higher blocksizes inherently have latency because they have to 
    record the data before sending it
    but smaller block sizes eventually have infinite latency because
    the system cannot process the audio fast enough

    this function should block until the server turns off or sends new settings
    """
    logging.info(f"listening to {chosen_mic.id} : {chosen_mic.name}")
    with chosen_mic.recorder(samplerate=settings['samplerate'], blocksize=settings['blocksize']) as mic:
            while True:
                data = np.abs(mic.record(numframes=None))
                avg = np.average(np.abs(data))
                peak = np.max(np.abs(data))

                payload = {
                    "avg": float(avg),
                    "peak": float(peak),
                    "data": data.tolist(),
                }
                try:
                    response = session.post(ip + "audio_in", json=payload)
                except requests.exceptions.ConnectionError:
                    logging.error("server did not respond, exiting...")
                    return False
                
                if "change_settings" in response:
                    logging.info("stopping because new settings are available")
                    return True

def main():
    """
    main function, wrangles send_audio and send_settings
    """
    # BUG: fuzzy search grabs loopback devices when given the name of the actual device (non-loopback)
    DOCKER_IP="http://127.0.0.1:8000/"
    # default is to not include loopback
    loopback = False

    settings = {
        'loopback': loopback,
        'blocksize': 2048,
        'samplerate': 48000,
        'mics': {m.id: m.name for m in sc.all_microphones(include_loopback=loopback)},
        'source': sc.default_microphone().id
    }
    args = sys.argv[1:]
    while args:
        next = args.pop(0)
        if next == '-ip':
            try:
                DOCKER_IP = args.pop(0)
            except:
                logging.error("failed to parse command line arguments -ip used but no ip given")
                usage(1)
        elif next == '--loopback':
            settings['loopback'] = True
        elif next == '-b' or next == '--blocksize':
            try:
                settings['blocksize'] = int(args.pop(0))
            except:
                logging.error("failed to parse command line arguments - bad blocksize")
                usage(1)
        elif next == '--samplerate':
            try:
                settings['samplerate'] = int(args.pop(0))
            except:
                logging.error("failed to parse command line arguments - bad samplerate")
                usage(1)
        elif next == '-s' or next == '--source':
            try:
                settings['source'] = args.pop(0)
            except:
                logging.error("failed to parse command line arguments - no source given")
                usage(1)
        else:
            usage(1)
    
    if not send_settings(DOCKER_IP, settings):
        return
        
    while True:
        chosen_mic = sc.get_microphone(settings['source'], include_loopback=settings['loopback'])
        # send_audio should block
        if not send_audio(chosen_mic, DOCKER_IP, settings):
            return
        
        # if send_audio stopped and returned true then the settings need to be
        # updated
        if not update_settings(DOCKER_IP, settings):
            return


if __name__ == "__main__":
    main()