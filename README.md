# creativity-optional

Light organization program for all your gamer-cave needs

# What is this project?

This project is a script that generates a stream of images based on song selection/system audio and sends the stream to an output of your choice.

## Available outputs:

- [ ] Computer monitor
- [ ] keyboard / peripheral devices
- [ ] room lights

## Sound input methods:

- [ ] system audio / audio from a specific application
- [ ] spotify [API](https://developer.spotify.com/documentation/web-api)
- [ ] amazon music [API](https://developer.amazon.com/docs/music/API_web_overview.html)
- [ ] apple music [API](https://developer.apple.com/documentation/applemusicapi/)

# Goals:

- [ ] uv mapping for outputs
- [ ] real-time light reactions
- [ ] plug-and-play connection to third party apis

# Contributing to this project:

Both `main` and `develop` branches are protected. 
To contribute first find or make an issue in the [issues](https://github.com/BCaven/creativity-optional/issues) tab.
Then, branch off of `develop` for the issue/feature you are working on. Branch names should be the same as the name of the issue.

Once your contribution is complete, make a [pull request](https://github.com/BCaven/creativity-optional/pulls) to the `develop` branch and request someone to review your pull request.

If your change gets accepted to the `develop` branch, a pull request will be opened to merge it into main.


# TODO List:

- [ x ] organize Directory
- [ x ] set up rules for development on github

# Development:

## Directory organization:

`src/` contains source files for the application
`testing/` contains miscellaneous scripts used to test specific sub features

## venv activation

[in-depth tutorial](https://docs.python.org/3/tutorial/venv.html)

TLDR:
For windows:
`.venv\Scripts\activate`

For linux/macos:
`source .venv/bin/activate`

To run scripts, first activate the virtual environment then run the script.

Python scripts were designed to be run from the root directory of the project.

For example, `python3 testing/sound_input.py`
