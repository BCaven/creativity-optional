### Setup on MacOS
The MacOS version of CO usees PyAudio (because SoundCard only works on Linux and Windows RIP) The dowside of this is that PyAudio doesn't natively support loopback, so we have to get it ourselves. Our current solution is to use BlackHole, a popular loopback driver

## Installing BlackHole
install the desired BlackHole driver by running:
`./brew-installer.sh`

this will automatically install the desired 2 driver version of BlackHole

## Creativing the Loopback system
Follow this tutorial from the BlackHole GitHub to set up the Loopback with a Multi-Output Device[https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device]

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

In the current build, the Vue server and the local client also need to be run seperately as well. In a seperate window, run the following:

`python3 src/macOS_pyaudio.py`

This will run the local client, and you should be able to see the raw data in the docer image.

To see a demo of the output from the `vue-frontend` directoy, run the command:

`npm run dev` 

and go to the localhost link on your browser!
NOTE: Some browsers will not allow the `vue-frontend` to make the GET requests, meaning that it will not recieve any of the audio data.

# Tested Browsers that don't work without changing settings:
Safari, Brave

# Tested Browsers that work:
Chrome, Firefox