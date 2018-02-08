import random

with open("cloud.ply", "w") as myfile:
	myfile.write("")

vertex_count = 100000

with open("cloud.ply", "a") as myfile:
	myfile.write("ply\nformat ascii 1.0\nelement vertex "+str(vertex_count)+"\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
	
	for x in range(vertex_count):
		x = random.uniform(-0.5, 0.5)
		y = random.uniform(-0.5, 0.5)
		z = random.uniform(-0.5, 0.5)
		r = random.randint(0,255)
		g = random.randint(0,255)
		b = random.randint(0,255)

		text = "{} {} {} {} {} {}\r\n".format(x, y, z, r, g, b)

		myfile.write(text)