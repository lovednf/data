import os
import re
import numpy as np
import matplotlib.pyplot as plt

path = os.getcwd()
subdir = [dirnames for root,dirnames,filenames in os.walk(path)]
subdir = sorted(subdir[0], key = lambda x:int(re.match(r'(\d+)', x).group()))
print(subdir, "\n")


data = []
for i in range(26):
	with open(path + "/" + subdir[i] + "/temp.txt", "r") as txtfile:
		data.append(txtfile.readlines())
print(data, "\n")


def rotaMat(coordX, coordY, theta, distance): 
	#coordX and coordY represent the current coordinate X and Y, respectively
	M = np.mat([[np.cos(theta*np.pi/180), -1*np.sin(theta*np.pi/180)], \
		[np.sin(theta*np.pi/180), np.cos(theta*np.pi/180)]])
	coord = np.array([0, -1]) #define the initial positive direction
	return np.array(np.dot(M, coord)*distance + np.array([coordX, coordY])).flatten()
print("test rotaMat", rotaMat(0, 0, 0, 1), "\n")


forward, backward, left, right = 0, 180, 90, -90
currX, currY, currTheta = 0, 0, 0
distance = list(map(float, [i[2].strip("\n") for i in data]))
coordinates = []
for i in range(26):
	if data[i][1] == "forward\n":
		coord = rotaMat(currX, currY, currTheta, distance[i])
	elif data[i][1] == "backward\n":
		currTheta += backward
		coord = rotaMat(currX, currY, currTheta, distance[i])
	elif data[i][1] == "left\n":
		currTheta += left
		coord = rotaMat(currX, currY, currTheta, distance[i])
	elif data[i][1] == "right\n":
		currTheta += right
		coord = rotaMat(currX, currY, currTheta, distance[i])
	currX, currY = coord[0], coord[1]
	coordinates.append([currX, currY])
print(coordinates)

plt.plot([i[0] for i in coordinates], [i[1] for i in coordinates], "*-")
plt.show()