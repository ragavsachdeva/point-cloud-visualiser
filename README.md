# Point Cloud Visualiser

A package that visualises 3D point clouds (a .ply file) using three.js.

## Getting Started

* Clone/Download this repository and cd into the directory.
* Install all the requirements using $```pip install -r requirements.txt```
* Add your PLY file in the directory.
* Run $```python3 main.py -f your-point-cloud-file.ply```.
This will also automatically run a local server. 
* Go to the port being served in your browser.

### Functionality

* Rotate the visualisation with swipe motion using your mouse/trackpad.
* Zoom in/out.
* Control the camera view (or "move" the visualisation) using arrow keys.
* Alter the size and opacity of the points.

### Prerequisites

* Python3

## Author

* **Ragav Sachdeva**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

Thanks to David de la Iglesia Castro for publishing his [pyntcloud](https://github.com/daavoo/pyntcloud) library. The visualiser is based on his work.
