<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";
import light_example_scene from "./components/light_example_scene.vue";


// use multicast or something to find this server route
// eventually this page will be the UI for the server in the docker container - so we can just do localhost:container_port
// and never have to worry about it again
// for testing, I am running this outside of the docker container
// look into service workers as a way to automate the process of receiving data from the server
const server_route = "0.0.0.0:8000";
let sound_bar = ref("");
let sound_volume = ref(0);
let fft = ref([]);
let selected_item = ref({"id": "", "name": ""});
let sound_options = ref([]);
let selected_input = ref("");
const timer = ref();

async function getSoundOptions() {
  // get all input options from local controller
  console.log("getting sound options from server");
  const response = await fetch("http://" + server_route + "/audio_source");
  let r = await response.json();
  // update the list of mics and selected mic from the server
  console.log(r.mics)
  sound_options.value = r.mics;
  selected_input.value = r.source;
}
async function updateSoundOptions() {
  selected_input.value = selected_item.value.name;
  console.log("sending new sound source to server");
  const response = await fetch(
    "http://" + server_route + "/audio_source",
    {
      method: "POST",
      body: JSON.stringify(selected_input)
    }
  );
  let r = await response.json();
}

async function updateSoundData() {
  // get the new sound data
  // the sound "bar" is just for testing visualization
  const response = await fetch("http://" + server_route + "/audio_in");
  //console.log(response.json());
  let r = await response.json();
  sound_bar.value = r.bars;
  sound_volume.value = r.peak;
  //console.log(sound_bar.value);
}
async function updateFFTData() {
  const response = await fetch("http://" + server_route + "/fft_audio");
  let r = await response.json();
  fft.value = r['frequencies'];
}

function countDownFunc () {
  //console.log("updating sound data");
  // NOTE: when testing without audio data, comment out this function call
  updateSoundData();
  updateFFTData();
}

// Instantiate
onMounted(() => {
  // could probably make this refresh faster given a better computer - I am testing this on my garbage laptop
  timer.value = setInterval(() => {
    countDownFunc();
  }, 60); // ~15 times every second
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
    <p> Current Volume: {{ sound_volume }}</p>
    <!--<v-combobox
      label="audio input"
      :items="sound_options"
      v-model="selected_item"
      item-text="name"
      single-line
      return-object
      ></v-combobox>-->
    <v-progress-linear max=1 model-value=0 v-model="sound_volume" :height="12"></v-progress-linear>

    <light_example_scene :volume="sound_volume"/>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
