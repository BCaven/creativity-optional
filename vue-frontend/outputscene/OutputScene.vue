<script setup>
// TODO: fix formatting bug where threejs canvas does not take up the entire screen

import { onMounted, onBeforeUnmount, ref } from "vue";
import { io }  from "socket.io-client";

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
  <main>
    <basic_3d_scene :volume="sound_volume"/>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
