# ThreeJS Scene

Needs to import models from Blender Scene 

# TODO

- [ ] import models
- [ ] access/modify blendshapes (morphshapes)
- [ ] make helper scripts to better harvest data or format it in a way that better suits our needs

# APIs and helper scripts

I think it will be easiest to have these return JSON objects with their data so the server can just send the JSON over to the frontend instead of needing to parse the responses from the helper scripts

- [ ] Apple Music API
    - [ ] register as apple developer and get key
    - [ ] helper script to achieve the "currently playing" feature
- [ ] battery status
    - [ ] charging, percentage, etc
- [ ] graphics mode/laptop power profile
    - maybe lump this in with the battery state helper
- [ ] github / git helper
    - it would be cool to have current working directory git status but that one might be tricky because the app would have to have some knowledge of the current working directory
    - alternatively this could be set using environment variables but I don't think the application would have the permissions to see them.
        -  [ ] check how to do this, might be able to sneak around it with `set` or `export`
    - [ ] using webhooks for github integration - look at github API docs
- [ ] "random animations" helper script
    - script to orchestrate the "random" ambient events and animations that happen in the scene (rain, people moving, flickering signs, etc)