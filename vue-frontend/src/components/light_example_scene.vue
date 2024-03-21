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
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);
  
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshStandardMaterial( { color: 0xffffff, roughness: 0, metalness: 0 } );
        this.cube = new THREE.Mesh(geometry, material);
        this.scene.add(this.cube);

        // lights
        this.ambientLight = new THREE.AmbientLight(0x0000ff, 0.5)
        this.scene.add(this.ambientLight)
        this.light = new THREE.RectAreaLight( 0xff0000, 5, 4, 10 );
        this.light.position.set(0, 0, 3)
        this.brightness = 0.5;
        
        this.scene.add(this.light)
        
        
        this.camera.position.z = 5;
  
        const animate = function() {}
      },
      animate: function() {
        requestAnimationFrame(this.animate);
        let old_y = this.cube.position.y;
        let desired_y = this.volume * 5;
        if (distance(desired_y, old_y) > 0.02) {
          if (desired_y > old_y) {
            this.cube.position.y += distance(desired_y, old_y) / 10;
          } else {
            this.cube.position.y -= distance(desired_y, old_y) / 10;
          }
        }
        this.cube.rotation.x += 0.01;
        this.cube.rotation.y += 0.01;
        let desired_brightness = this.volume;
        if (distance(desired_brightness, this.brightness) < 0.02) {
            this.brightness = desired_brightness;
        } else {
            if (desired_brightness > this.brightness) {
                this.brightness += distance(desired_brightness, this.brightness);
            } else {
                this.brightness -= distance(desired_brightness, this.brightness);
            }
        }
        if (this.brightness > 1) {
            this.brightness = 1;
        } else if (this.brightness < 0) {
            this.brightness = 0;
        }
        this.light.color.setHSL(1, 1, this.brightness); 
        this.renderer.render(this.scene, this.camera);
        //console.log("animating...");
      }
    },
    mounted() {
      this.init();
      this.animate();
    }
  }
</script>

<style>
#container {
    width: 100%;
    height: 100%;
}
</style>