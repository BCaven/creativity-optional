#!/bin/sh

SOURCE="BlackHole 2ch" # use -d for default mic
RATE='48k' # sampling rate (Hz)
usage() {
    cat <<EOF
Usage: macOS_shell_client.sh [-m] [-s SOURCE] [-r RATE]

    -m  use the default microphone as input

    -s SOURCE specify a specific source

    -r RATE specify the sampling rate in Hz

default values are the BlackHole mic, and 48k Hz

EOF
exit $1
}

while [ $# -gt 0 ]; do
    case $1 in
        -m)
            SOURCE="-d"
            ;;
        -s)
            shift
            SOURCE="$1"
            ;;
        -r) 
            shift
            RATE="$1"
            ;;
        
        -h)
            usage 0
            ;;
        *) 
            usage 1
            ;;
    esac
    shift
done

sox -r $RATE -c 2 -b 32 -e signed-integer -t coreaudio "$SOURCE" -t raw - | python3 src/macOS_sound_processor.py
