from plyfile import PlyData, PlyElement

plydata = PlyData.read('pyntcloud_plot.ply')

print((plydata.elements[0].data[0]))

