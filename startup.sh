#!/bin/sh
echo "for chad's eyes only"
python3 src/local_audio_client.py > local_audio_client.log &
npm run dev --prefix ./vue-frontend

# kill the local audio client if it exists
# TODO: make sure this actually works
# of course, the local client will end if it does not get a response from the server
ps aux | grep -v grep | grep "python3 src/local_audio_client.py" | awk '{ print $2 }' | kill