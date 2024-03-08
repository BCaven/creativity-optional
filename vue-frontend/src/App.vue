<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";
import basic_3d_scene from "./components/basic_3d_scene.vue";


// use multicast or something to find this server route
// eventually this page will be the UI for the server in the docker container - so we can just do localhost:container_port
// and never have to worry about it again
// for testing, I am running this outside of the docker container
// look into service workers as a way to automate the process of receiving data from the server
const server_route = "0.0.0.0:8000";
let sound_bar = ref("");
let sound_volume = ref(0);
let sound_options = ref([]);
let selected_input = ref("");
const timer = ref();

async function getSoundOptions() {
  // get all input options from local controller
  console.log("getting sound options from server");
  const response = await fetch("http://" + server_route + "/audio_sources");
  let r = await response.json();
  // update the list of mics and selected mic from the server
  sound_options.value = r['mics'];
  selected_input.value = r['source'];
}

async function updateSoundData() {
  // get the new sound data
  // the sound "bar" is just for testing visualization
  const response = await fetch("http://" + server_route + "/audio_in");
  //console.log(response.json());
  let r = await response.json();
  sound_bar.value = r.bars;
  sound_volume.value = r.bars.length;
  console.log(sound_bar.value);
}

function countDownFunc () {
  //console.log("updating sound data");
  // NOTE: when testing without audio data, comment out this function call
  updateSoundData();
}

// Instantiate
onMounted(() => {
  // could probably make this refresh faster given a better computer - I am testing this on my garbage laptop
  timer.value = setInterval(() => {
    countDownFunc();
  }, 100); // 10 times every second
});

// Clean up
onBeforeUnmount(() => {
  timer.value = null;
});

</script>

<template>
  <main>
    <v-btn @click="getSoundOptions">Get Sound Options</v-btn>
    <p>Audio Device: {{ selected_input }}</p>
    <p> Current Audio: {{ sound_bar }}</p>
    <v-combobox
      label="audio input"
      :items="sound_options"
      ></v-combobox>
    <v-slider v-model="sound_volume"></v-slider>
    <basic_3d_scene :volume="sound_volume"/>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
