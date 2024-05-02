<template>
    <div id="container"></div>
  </template>
  <script>
  import * as THREE from 'three'
  function distance(a, b) {
    return Math.sqrt((a - b) * (a - b))
  }
  export default {
    name: 'ThreeTest',
    data() {
      return {
      }
    },
    props: {
        volume: Number
    },
    methods: {
      init: function() {
        this.scene = new THREE.Scene()
        this.camera = new THREE.PerspectiveCamera(
          75,
          window.innerWidth / window.innerHeight,
          0.1,
          1000
        );
  
        this.renderer = new THREE.WebGLRenderer();
        // TODO: find the real solution for this work around later (removing scroll bar)
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);
  
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        this.activeMat = new THREE.MeshBasicMaterial({color: 0xff00ff});
        this.inactiveMat = new THREE.MeshBasicMaterial({color: 0x101040});
        this.cubes = [];
        for (let i = -5; i < 5; i++) {
          this.cubes.push(new THREE.Mesh(geometry, this.inactiveMat));
          this.cubes[i + 5].position.x = i * 1.1;
          this.scene.add(this.cubes[i + 5]);
        }
        this.currentCube = 0;
        
        this.camera.position.z = 5;
  
        const animate = function() {}
      },
      animate: function() {
        requestAnimationFrame(this.animate);
        for (let i = 0; i < 10; i++) {
          this.cubes[i].rotation.x += 0.01;
          if (i == this.currentCube) {
            this.cubes[i].material = this.activeMat;
          } else {
            this.cubes[i].material = this.inactiveMat;
          }
        }
        let old_y = this.cubes[this.currentCube].position.y;
        let desired_y = this.volume * 10;
        //console.log("volume: ", this.volume);
        //console.log("desired y: ", desired_y);
        if (distance(desired_y, old_y) > 0.02) {
          if (desired_y > old_y) {
            this.cubes[this.currentCube].position.y += distance(desired_y, old_y) / 10;
          } else {
            this.cubes[this.currentCube].position.y -= distance(desired_y, old_y) / 10;
          }
        }
        
        
        //console.log("current cube: ", this.currentCube);
        this.renderer.render(this.scene, this.camera);
        //console.log("animating...");
      }
    },
    mounted() {
      this.init();
      this.timer = setInterval(() => {
        this.currentCube += 1;
        if (this.currentCube > this.cubes.length - 1) {
          this.currentCube = 0;
        } 
      }, 1000);
      
      this.animate();
      
    }
  }
</script>

<style>
canvas {
    width: 100%;
    height: 100%;
    display: block;
}
</style>