<!--
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
        volume: Number,
        fft: Array
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

        this.bgGeo = new THREE.PlaneGeometry(window.innerWidth, window.innerHeight);
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

        this.hueShift = new THREE.DirectionalLight(0xffffff, 0);
        this.hueShift.position.set(0, 0, 1);
        this.scene.add(this.hueShift);
      
        this.hueColor = new THREE.Color(0xff0000);

        // Divide frequencies into three ranges
        this.trebleLight = new THREE.SpotLight(0xffffff, 1.0, 0, Math.PI / 2.0);
        this.altoLight = new THREE.SpotLight(0xffffff, 1.0, 0, Math.PI / 2.0);
        this.bassLight = new THREE.SpotLight(0xffffff, 1.0, 0, Math.PI / 2.0);

        this.trebleLight.position.set(-window.innerWidth / 4.0, 0, window.innerWidth / 4.0);
        this.altoLight.position.set(0, 0, window.innerWidth / 4.0);
        this.bassLight.position.set(window.innerWidth / 4.0, 0, window.innerWidth / 4.0);

        this.trebleLight.target.position.set(-window.innerWidth / 4.0, 0, 0);
        this.bassLight.target.position.set(window.innerWidth / 4.0, 0, 0);

        this.scene.add(this.trebleLight.target)
        this.scene.add(this.bassLight.target)

        // this.trebleLight.position.set(0, 0, 1);
        // this.altoLight.position.set(0, 0, 1);
        // this.bassLight.position.set(0, 0, 1);

        this.scene.add(this.trebleLight);
        this.scene.add(this.altoLight);
        this.scene.add(this.bassLight);

        this.trebleColor = new THREE.Color(0xff0000);
        this.altoColor = new THREE.Color(0x00ff00);
        this.bassColor = new THREE.Color(0x0000ff);


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
        // set overall color
        this.hueShift.color.set(this.hueColor);
        // this.hueColor.offsetHSL(0, 0, -0.01);

        // set pitch based color
        this.trebleLight.color.set(this.trebleColor);
        this.altoLight.color.set(this.altoColor);
        this.bassLight.color.set(this.bassColor);

        this.trebleColor.offsetHSL(0.01, 0, 0);
        this.altoColor.offsetHSL(0.02, 0, 0);
        this.bassColor.offsetHSL(0.03, 0, 0);

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