"use strict"

import * as THREE from 'three';
// post processing libraries
import { WebGLRenderer } from "three";
import { EffectComposer, EffectPass, RenderPass, HueSaturationEffect } from "postprocessing";


// ---------------------------  SETUP SCENE ----------------------------------------

const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera( window.innerWidth / -2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / -2, 0.1, 1000);
// const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.01, 10000);
camera.position.z = 1000;
const renderer = new WebGLRenderer({
	powerPreference: "high-performance",
	antialias: false,
	stencil: false,
	depth: false
});
// renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

// ---------------------------  ADD IMAGE ----------------------------------------

// load a texture, set wrap mode to repeat
const picTexture = new THREE.TextureLoader().load( "images/test_photo.jpg" );
const pictureMat = new THREE.MeshBasicMaterial({
	map:picTexture,
	onBeforeCompile: shader => {
		shader.uniforms.time = gu.time;
		shader.fragmentShader = `
			uniform float time;
			// All components are in the range [0…1], including hue.
			vec3 rgb2hsv(vec3 c)
			{
				vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
				vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
				vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
			
				float d = q.x - min(q.w, q.y);
				float e = 1.0e-10;
				return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
			}

			// All components are in the range [0…1], including hue.
			vec3 hsv2rgb(vec3 c)
			{
				vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
				vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
				return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
			}


		`
	}
});

const boxGeo = new THREE.BoxGeometry( window.innerWidth, window.innerHeight, 100 );

const cube = new THREE.Mesh( boxGeo, pictureMat);
scene.add( cube );

// ------------------------------ POST-PROCESSING ----------------------------


const composer = new EffectComposer(renderer);
// Rendered  scene as input for next post-processing
const renderPass = new RenderPass( scene, camera );
composer.addPass( renderPass );


// const hueSatPass = new HueSaturationEffect({
// 	blendFunction: null,
// 	saturation: 0.9,
// 	hue: 0.0});
// composer.addPass(hueSatPass);






// const effectPass = new EffectPass();
// composer.addPass(effectPass);
// // final sRGB color space conversion & optional tone mapping
// const outputPass = new OutputPass();
// composer.addPass( outputPass );








// ------------------------------  ANIMATE ---------------------------------
function animate() {
	requestAnimationFrame( animate );

	// cube.rotateY(.01);
	composer.render();
}

animate();