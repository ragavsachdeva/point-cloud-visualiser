import random

with open("cloud.ply", "w") as myfile:
	myfile.write("")

vertex_count = 100000

with open("cloud.ply", "a") as myfile:
	myfile.write("ply\nformat ascii 1.0\nelement vertex "+str(vertex_count)+"\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
	
	for x in range(vertex_count):
		myfile.write(str(random.uniform(-0.5, 0.5)) + " " + str(random.uniform(-0.5, 0.5)) + " " + str(random.uniform(-0.5, 0.5)) + " " + str(random.randint(0,255)) + " " + str(random.randint(0,255)) + " " + str(random.randint(0,255)) + "\n")