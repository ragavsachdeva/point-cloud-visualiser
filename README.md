# Point Cloud Visualiser

A package that visualises 3D point clouds (a .ply file) using three.js.

![alt text](/extra/screenshots.png)

### Prerequisites

* Python3

## Getting Started

* Clone/Download this repository and cd into the directory.
* Install all the requirements using $```pip install -r requirements.txt```
* Add your PLY file in the directory.
* Run $```python3 main.py -f your-point-cloud-file.ply```.
This will also automatically run a local server. 
* Go to the port being served in your browser.

You may need to tune the values of ```c_x, c_y, c_z, l_x, l_y, l_z``` in the ```main.py``` file. 
```c``` = intial position of the camera. ```l``` = the point (direction) being looked at.

### Functionality

* Rotate the visualisation with swipe motion using your mouse/trackpad.
* Zoom in/out.
* Control the camera view (or "move" the visualisation) using arrow keys.
* Alter the size and opacity of the points.

#### Note:

* The .ply file should have the following structure

```
ply
format ascii 1.0
element vertex [number-of-points]
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
[x] [y] [z] [r] [g] [b]
.
.
.
```

* 360° rotation is only possible horizontally. Vertical rotation is restricted to 180°. It is a limitation of the three.js.

* Furthermore, "horizontal" rotation is always about z-axis. Modify your .ply file accordingly.

## Author

* **Ragav Sachdeva**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

Thanks to David de la Iglesia Castro for publishing his [pyntcloud](https://github.com/daavoo/pyntcloud) library. The visualiser is based on his work.
