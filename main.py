import os
import argparse
from plyfile import PlyData, PlyElement

cloud_file = "default_cloud.ply"

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

c_x = (x_min + x_max)/2
c_y = (y_min + y_max)/2
c_z = z_min - (z_max - z_min + max(x_max-x_min, y_max-y_min))

l_x = (x_min + x_max)/2
l_y = (y_min + y_max)/2
l_z = z_min

with open("config.json", "w") as cf:
    configSettings = '{"filename": "'+cloud_file[:-4]+'", "camera_position": ['+str(c_x)+', '+str(c_y)+', '+str(c_z)+'], "look_at": ['+str(l_x)+', '+str(l_y)+', '+str(l_z)+'], "point_size": 0.01, "point_opacity": 1}'
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
        #screenshot {
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
    </style>
</head>

<body>
    <!-- <button id="screenshot"> SCREENSHOT </button>  -->     
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
            // drawLines(scene, config.lines, config.line_color_list)
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
            $("#screenshot").click(function() {
                window.open( renderer.domElement.toDataURL("image/png"), "Final");
                return false;
            });            
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