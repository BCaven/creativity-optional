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
import basic_3d_scene from "./components/basic_3d_scene.vue";


console.log(location);

// do not need to specify the location because this page is getting served by the websocket server
const socket = io();

let server_data = ref(new Map());
// audio data being its own thing is just to have backwards compatability with old scenes
// eventually it will be removed (as will hardcoded custom scenes) but for now, it is kept in
let audio_max = ref(0);
// socket listeners
// we mostly just need to listen for new data - not partictularly concerned with sending information back at the moment
function handleIncomingData(data) {
  //console.log("message from server: ", data);
  for (const prop in data) {
    if (prop != 'type') {
      server_data.value.set(prop, data[prop]);
      //console.log("server_data: ", server_data.value);
    }
  }
}
function handleAudioData(data) {
  //console.log("audio data: ", data);
  audio_max.value = Number(data['peak']);
  server_data.value.set('audio_max', data['peak']);
}
socket.on("incoming_data", handleIncomingData);
socket.on("audio_data", handleAudioData);
socket.on("message", handleIncomingData);
socket.on("connect", () => console.log("websocket connected!"));
socket.on("disconnect", () => console.log("websocket disconnected"));

</script>

<template>
  <!--
    Start page: node editor with threejs scene in the background
  -->
  <main>
    <h1>Incoming data:</h1>
    <v-list lines="one">
      <v-list-item
        v-for="item in server_data"
        :key="item[0]"
        :title="'Item ' + item[0] + ':'"
      >
        {{ item[1] }}
      </v-list-item>
      
    </v-list>
    <!--<light_example_scene volume:audio_max></light_example_scene>
    -->
    <basic_3d_scene :volume="audio_max" :general_inputs="server_data"/>

  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
