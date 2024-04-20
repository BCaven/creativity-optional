<script setup>
/*
Source for the front-end served by the flask server

Tasks:
[DONE] websocket connection
[TODO] import initial node graph
[TODO] support for general keys
[TODO] rearrange the threejs scene
[TODO] import models into the threejs scene
[TODO] typescript so future developers do not hate us
*/


import { onMounted, onBeforeUnmount, ref } from "vue";
import { io }  from "socket.io-client";

import light_example_scene from "./components/light_example_scene.vue";


console.log(location);

// do not need to specify the location because this page is getting served by the websocket server
const socket = io();

let server_data = ref(new Map());

// socket listeners
// we mostly just need to listen for new data - not partictularly concerned with sending information back at the moment
function handleIncomingData(event) {
  console.log("message from server: ", event);
}
socket.on("incoming data", handleIncomingData);
socket.on("message", handleIncomingData);
socket.on("connect", () => console.log("websocket connected!"));
socket.on("disconnect", () => console.log("websocket disconnected"));

/**
 * getKey
 * @param {String} key 
 * 
 * get data for a specific key from the server and update it's value
 */
async function getKey(key) {
  // get data for a specific key
  const response = await fetch("https://" + server_route + "/general_keys/" + key);
  let r = await response.json();
  // make sure we got a valid response
  // update that key's data
  server_data.value.set(key, r[key]);
}
/**
 * getAllKeys
 * 
 * fill in every known key with an empty value
 */
async function getAllKeys() {
  const response = await fetch("https://" + server_route + "/general_keys");
  let r = await response.json();
  r.keys().forEach(key => server_data.value.set(key, ''));
}


</script>

<template>
  <main>


  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
