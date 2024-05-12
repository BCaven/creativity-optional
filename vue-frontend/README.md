# creativity-optional-vue-frontend

## the goal:

the front end should have two main parts:
1) node editor to control the scene (path: `/`)
2) the actual output (path: '/output')

## the node editor:

look for things we can use as a drop in so I do not need to make a node editor from scratch
it would be nice to have the option to display the scene behind the node editor and have it update in real(ish) time.

## the actual output:

should only really be accessed by end applications (wallpaper engine, etc) or by the server for Server-side rendering

## storing and changing the dynamic scene:

easy way: make it a json (or equivalent) and use some polymorphism so the scene can decode any node

## Running the front end without a backend

This is useful if for some reason you do not want to test with the backend.
```sh
# from the `vue-frontend` folder...
# install dependencies
npm install
# run development server
npm run dev
```