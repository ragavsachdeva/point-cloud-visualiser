import os
import argparse
import math
from plyfile import PlyData, PlyElement

cloud_file = "skull.ply"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Please provide the name of the point cloud file.")
args = parser.parse_args()
if args.filename:
    cloud_file = args.filename

plydata = PlyData.read(cloud_file)
x_min = min(plydata.elements[0].data['x'])
x_max = max(plydata.elements[0].data['x'])
y_min = min(plydata.elements[0].data['y'])
y_max = max(plydata.elements[0].data['y'])
z_min = min(plydata.elements[0].data['z'])
z_max = max(plydata.elements[0].data['z'])

#Tweak these parameters to adjust the initial camera position

c_x = (x_min + x_max)/2
c_z = (y_min + y_max)/2
c_y = (z_min - (z_max - z_min + max(x_max-x_min, y_max-y_min)))

l_x = (x_min + x_max)/2
l_z = (y_min + y_max)/2
l_y = z_min

with open("config.json", "w") as cf:
    configSettings = '{"filename": "'+cloud_file[:-4]+'", "camera_position": ['+str(c_x)+', '+str(c_y)+', '+str(c_z)+'], "look_at": ['+str(l_x)+', '+str(l_y)+', '+str(l_z)+'], "point_size": 0.2, "point_opacity": 1}'
    cf.write(str(configSettings))

file = open('index.html','w')

message = """
<!DOCTYPE html>

<head>
    <title>Point Cloud Visualiser</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <style>
        body {
            color: #cccccc;
            font-family: Monospace;
            font-size: 13px;
            text-align: center;
            background-color: #050505;
            margin: 0px;
            overflow: hidden;
        }

        #logo_container {
            position: absolute;
            top: 0px;
            width: 100%;
        }

        #Logo {
            height: 100px;
        }
        #myBtn {
            position: absolute;            
            background-color: rgb(245, 139, 69);
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 12px;
            top: 0px;            
            left: 0px;            
        }

                /* The Modal (background) */
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            padding-top: 100px; /* Location of the box */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgb(0,0,0); /* Fallback color */
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
        }

        /* Modal Content */
        .modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
        }

        /* The Close Button */
        .close {
            color: #aaaaaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .close:hover,
        .close:focus {
            color: #000;
            text-decoration: none;
            cursor: pointer;
        }     

        textarea {
            overflow-y: scroll;
            height: 100px;
            resize: none; /* Remove this if you want the user to resize the textarea */
        }   
    </style>
</head>

<body>
    <button id="myBtn"> SCREENSHOT </button>
        <!-- The Modal -->
    <div id="myModal" class="modal">

      <!-- Modal content -->
      <div class="modal-content">
        <span class="close">&times;</span>
        <div id="durl">Some text in the Modal..</div>
      </div>

    </div>  
    <div>
        <img id="Logo" src="">      
    </div>

    <div id="container">
    </div>
    
    <script src="assets/three.min.js"></script>
    <script src="assets/Detector.js"></script>
    <script src="assets/OrbitControls.js"></script>
    <script src="assets/stats.min.js"></script>
    <script src="assets/jquery.min.js"></script>
    <script src="assets/PLYLoader.js"></script>
    <script src="assets/dat.gui.min.js"></script> 
    <script src="assets/CanvasRenderer.js"></script>    

    <script>
        if (!Detector.webgl) Detector.addGetWebGLMessage();

        var container;
        var camera, scene, renderer, controls;
        var points;
        var loader;

        //
        // Config File Loader
        //
        
        let fileLoader = new THREE.FileLoader();
        fileLoader.load("config.json", result => {
          let config = JSON.parse(result);

          init(config);
          animate(config);
        })


        //========================= INIT ==============================================//

        function init(config) {
            let camera_position = config.camera_position;
            let look_at = config.look_at;

            var textureLoader = new THREE.TextureLoader();
            var sprite = textureLoader.load( "assets/ball.png" );
            //
            // SCENE
            //
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0xffffff)
            //
            // Lines
            //
            //drawLines(scene, config.lines, config.line_color_list)
            //
            // CAMERA
            //
            camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.x = camera_position[0];
            camera.position.y = camera_position[1];
            camera.position.z = camera_position[2];
            camera.up = new THREE.Vector3(0, 0, 1);
            //
            // GUI
            //
            var parameters = 
            {
                size: config.point_size,
                opacity: config.point_opacity,
                wireframe: true,
            };
            const gui = new dat.GUI();            

            //
            // LOADER
            //
            var material;
            var figure;
            loader = new THREE.PLYLoader();
            loader.load('""" + cloud_file+ """', (geometry) => {
                console.log(geometry);

                material = new THREE.PointsMaterial({
                    size: config.point_size,
                    vertexColors: THREE.VertexColors,
                    transparent: true,
                    opacity: config.point_opacity,
                    map: sprite
                });
                figure = new THREE.Points(geometry, material);

                var figureSize = gui.add(parameters, 'size').min(0.001).max(1).step(0.001).name("Point Size").listen();
                figureSize.onChange((value) => {
                    figure.material.size = value;
                }); 


                var figureOpacity = gui.add(parameters, 'opacity').min(0.1).max(1).step(0.1).name('Opacity').listen();
                figureOpacity.onChange((value) => {
                    figure.material.opacity = value;   
                });      


                scene.add(figure);
            });
            var light = new THREE.AmbientLight( 0xFFFFFF, 1 ); // soft white light
            scene.add( light );
            //            
            // RENDERER
            //
            renderer = new THREE.WebGLRenderer({
                antialias: false,
                preserveDrawingBuffer: true                
            });
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            //
            // SCREENSHOT
            //

            // Get the modal
            var modal = document.getElementById('myModal');

            // Get the button that opens the modal
            var btn = document.getElementById("myBtn");

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName("close")[0];

            // When the user clicks the button, open the modal 
            btn.onclick = function() {

                var url = renderer.domElement.toDataURL("image/png");
                var iH = "Following is the dataURL of your image. Please go <a href='https://codebeautify.org/base64-to-image-converter' target='_blank'>here</a> to convert it into an image.<br><br>";
                var text = document.createElement("textarea");
                text.value = url;

                var durl = document.getElementById('durl');
                durl.innerHTML = iH;
                durl.append(text);


                modal.style.display = "block";
            }

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }



            //
            // ORBIT CONTROLS
            //
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.target.copy(new THREE.Vector3(look_at[0], look_at[1], look_at[2]));
            camera.lookAt(new THREE.Vector3(look_at[0], look_at[1], look_at[2]));
            //
            // ADD CONTAINER TO DOM
            //
            container = document.getElementById('container');
            container.appendChild(renderer.domElement);
            //
            // RESIZE LISTENER
            //
            window.addEventListener('resize', onWindowResize, false);
        }

        //========================= RESIZE ==============================================//

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
        
        //========================= ANIMATE ==============================================//

        function animate(config) {
            requestAnimationFrame(animate);
            render();
        }

        //========================= RENDER ==============================================//

        function render() {
            renderer.render(scene, camera);
        }

        //======================== Line Drawing Utils ===================================//

        function zip() {
          var args = [].slice.call(arguments);
          var shortest = args.length==0 ? [] : args.reduce(function(a,b){
              return a.length<b.length ? a : b
          });

          return shortest.map(function(_,i){
              return args.map(function(array){return array[i]})
          });
        }

        function makeThreeLine(linePoints, lineColor) {
          let material = new THREE.LineBasicMaterial({ color: parseInt(lineColor, 16) });
          let geometry = new THREE.Geometry();
          linePoints.forEach(x => {
            // ... is "spread syntax", same as a "splat" in Python.
            geometry.vertices.push(new THREE.Vector3(...x));
          })
          return new THREE.Line(geometry, material);
        } 

        function drawLines(scene, lines, colors) {
          if (lines.length !== colors.length) {
            throw Error("lines and colors must be the same length");
          }
          zip(lines, colors).forEach(lc => scene.add(makeThreeLine(lc[0], lc[1])))
        }

    </script>
</body>

</html>

"""

file.write(message)
file.close()

os.system("python3 -m http.server")