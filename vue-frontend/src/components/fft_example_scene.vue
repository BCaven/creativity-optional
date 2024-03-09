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
        fft: Array,
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
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        this.cubes = [];
        for (let i = 0; i < 8; i++) {
            this.cubes.push(new THREE.Mesh(geometry, material));
            this.cubes[i].position.x = i - 4;
            this.scene.add(this.cubes[i]);
        }
  
        this.camera.position.z = 5;
  
        const animate = function() {}
      },
      animate: function() {
        requestAnimationFrame(this.animate);
        let max_height = 10;
        for (let index = 0; index < this.fft.length; index ++) {
            let cube = this.cubes[index];
            let fft_cube = this.fft[index];

            let old_x = cube.position.x;
            if (distance(this.volume - 4 + index, old_x) > 0.5) {
                if (this.volume > old_x) {
                    cube.position.x += 0.1;
                } else if (this.volume < old_x) {
                    cube.position.x -= 0.1;
                }
            }
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
            let old_y = cube.position.y;
            if (distance(fft_cube * max_height, old_y) > 0.5) {
                if (fft_cube * max_height > old_y) {
                    cube.position.y += 0.1;
                } else {
                    cube.position.y -= 0.1;
                }
            }
        }
  
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