<template>
    <div id="container"></div>
</template>

<script>
import * as THREE from 'three';

export default {
    name: 'ThreeTest',
    data() {
        return {
            xMouse: 0,
            yMouse: 0
        };
    },
    props: {
        fft: Array,
        volume: Number
    },
    methods: {
        init: function() {
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(
                75,
                window.innerWidth / window.innerHeight,
                0.1,
                1000
            );
            this.renderer = new THREE.WebGLRenderer();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            document.getElementById('container').appendChild(this.renderer.domElement);

            const geometry = new THREE.SphereGeometry(0.5, 32, 32);
            this.spheres = [];
            for (let i = 0; i < 8; i++) {
                const material = new THREE.MeshPhongMaterial({ color: this.getColor(i) });
                const sphere = new THREE.Mesh(geometry, material);
                sphere.position.x = i - 4;
                this.scene.add(sphere);
                this.spheres.push(sphere);
            }

            const light = new THREE.PointLight(0xffffff, 1, 100);
            light.position.set(0, 0, 10);
            this.scene.add(light);
            this.camera.position.z = 10;
            this.animate();
        },
        animate: function() {
            requestAnimationFrame(this.animate);
            this.camera.rotation.y += 0.01;

            for (let index = 0; index < this.fft.length; index++) {
                const sphere = this.spheres[index];
                const fftValue = this.fft[index];

                const xTarget = this.volume - 4 + index;
                const yTarget = fftValue * 10;

                sphere.position.x += (xTarget - sphere.position.x) * 0.1;
                sphere.position.y += (yTarget - sphere.position.y) * 0.1;
                let hue = (sphere.position.x + 4) / 8;
                sphere.material.color.setHSL(hue, 1, 0.5);
            }
            this.renderer.render(this.scene, this.camera);
        },
        onmousemove: function(event) {
            this.xMouse = (event.xClient / window.innerWidth) * 2 - 1;
            this.yMouse = -(event.yClient / window.innerHeight) * 2 - 1;

            const movement = 10;
            this.camera.position.x += (this.xMouse - this.camera.position.x) / movement;
            this.camera.position.y += (this.yMouse - this.camera.position.y) / movement;
        }
    },
    mounted() {
        this,init();
        document.addEventListener('mousemove', this.onmousemove, false);
    },
    beforeDestroy() {
        document.removeEventListener('mousemove', this.onmousemove, false);
    }
};
</script>

<style>
#container {
    width: 100%;
    height: 100%;
};
</style>