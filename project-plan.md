    NOTE: This is the original pitch for the project
    
    Look at the README for an updated vision of the project

# pitch

room management: a light/appliance library that doesn't suck

smart color management (song mapping): trying to expand upon the ideas present in Hue Light Sync

easily customizable layouts (UV mapping)

potential to do some networking shenanigans iff you have a permanent controller (e.g. rp pico)

idea is that you merge separate APIs (Hue, Corsair, Asus, Alienware, etc) into one cohesive package -> desktop background, system lights, room lights all flowing as one cohesive unit

# project PLAN

1. getting the music into a usable form
2. making parameters out of music
3. (Generative ai) music -> image/image sequence
4. displaying image sequence on website
5. checking for compatable APIs (lights: hue, elgato (kms), dumb lights (assuming custom controller))
6. connect APIs to image sequence to display the fun colors

# APIs:

## changing the parameters (change what the image looks like):

1. Apple music API
2. Spotify
3. apple watch/health
4. oura (but requires input from user)

## display the image somewhere else:

1. wallpaper engine equivalent
2. Hue
3. elgato
4. icue
5. AuraSync
6. misc computer parts bc cool (mice/keyboards/etc)

# output:

- make an API/library for our own software so 3rd party can use it (example: custom light controllers for "dumb" lights)

# building the application

- framework: svelte, vue
- look up process/requirements for Windows app (zoom can do it so it cant be that hard)
- macOS app: apple developer?
- Linux its literally just an executable

# hosting the website/application:

- desktop app
- background application
- website

# generating the parameters from the music:

- dude its literally whatever the AI thinks is interesting unless we want to hard code it

# generating the image:

- ask anar
- image is created from the parameters

# UV unwrapping:

- principle: map portions of the generated image to specific things (computer monitor, lights ,etc)
- will need a GUI for this
- "easy" way to make everything look uniform with minimal effort on our side
- only useful if we have multiple display methods (lights that arent the computer screen)

















