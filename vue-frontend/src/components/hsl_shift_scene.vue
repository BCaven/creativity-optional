<!--
  Background is a sprite (800 x 800 x 1)
  Camera is at (0, 0, 500) pointed towards -z
  cube is (100 x 100 x 100) at (0, 0, 100)
 -->

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
        this.camera = new THREE.OrthographicCamera(
            window.innerWidth / -2,
            window.innerWidth / 2,
            window.innerHeight / 2,
            window.innerHeight / -2,
            0.1,
            1000
        );
  
        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);
  

        // load image
        this.map = new THREE.TextureLoader().load('/src/assets/HSV_test.png')
        this.imgMap = new THREE.MeshPhongMaterial({map: this.map, color: 0xffffff});

        this.bgGeo = new THREE.PlaneGeometry(800, 800);
        this.bg = new THREE.Mesh(this.bgGeo, this.imgMap);

        this.boxGeo = new THREE.BoxGeometry(100, 100, 100);
        this.boxMat = new THREE.MeshPhongMaterial( { color: 0xff00ff} );

        this.cube = new THREE.Mesh(this.boxGeo, this.boxMat);
        this.scene.add(this.bg);
        this.scene.add(this.cube);
        // this.SpriteMaterial.color.offsetHSL(0.5, 0.5, 1);
        // this.SpriteMaterial.color.setHex(0xff0000);

        this.cube.position.z = 100;

        this.camera.position.z = 500;
  



        // everything above this is default
        this.defaultLight = new THREE.AmbientLight(0xffffff, 1.0);
        this.scene.add(this.defaultLight);

        this.hueShift = new THREE.DirectionalLight(0xffffff, 1.5);
        this.hueShift.position.set(0, 0, 800);
        this.scene.add(this.hueShift);
      
        this.hueColor = new THREE.Color(0xff00);






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
        // this.light.color.setHSL(1, 1, this.brightness); 
        this.renderer.render(this.scene, this.camera);
        //console.log("animating...");



        // everything above this is Blake's stuff
        this.hueShift.color.set(this.hueColor);
        this.hueColor.offsetHSL(0.01, 0, 0);



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