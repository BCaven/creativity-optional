<template>
    <div id="container"></div>
</template>
<script setup>
/*
The current idea: make the node editor secretly be a three.js scene

Tasks:
[TODO] make the basic graph ui
[TODO] grab the default settings from the server
[TODO] track changes made by the user
[TODO] save those changes by sending them back to the server (when requested - might also add an auto-update feature)
[TODO] "make it pretty"
[TODO] look into three.js divs with "transparent" backgrounds (it would be really cool to have the live-updating scene in the background)

*/
</script>

<style>
#container {
    width: 100%;
    height: 100%;
}
</style>