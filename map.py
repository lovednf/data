import os
import re
import numpy as np
import matplotlib.pyplot as plt
import ImgMatch
import math


path = os.getcwd()
dirName = [dirnames for root,dirnames,filenames in os.walk(path)]
subDirList = list(filter(lambda x: re.match(r'(\d+)', x) != None, dirName[0]))
subdir = sorted(subDirList, key = lambda x:int(re.match(r'(\d+)', x).group()))
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
print("test rotaMat", rotaMat(1, 1, -90, 5), "\n")


def calDistance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))


def main():
	forward, backward, left, right = 0, 180, 90, -90
	currX, currY, currTheta = 0, 0, 0
	distance = list(map(float, [i[2].strip("\n") for i in data]))
	distance.append(0)
	coordinates = []

	for i in range(26):
		if data[i][1] == "forward\n":
			coord = rotaMat(currX, currY, currTheta, distance[i + 1])
		elif data[i][1] == "backward\n":
			currTheta += backward
			coord = rotaMat(currX, currY, currTheta, distance[i + 1])
		elif data[i][1] == "left\n":
			currTheta += left
			coord = rotaMat(currX, currY, currTheta, distance[i + 1])
		elif data[i][1] == "right\n":
			currTheta += right
			coord = rotaMat(currX, currY, currTheta, distance[i + 1])
		currX, currY = coord[0], coord[1]
		coordinates.append([currX, currY])

		if len(coordinates) > 1:
			for j in range(len(coordinates) - 1):
				if calDistance(coordinates[i], coordinates[j]) < 5:
					ImgListNow = ImgMatch.ReadSingleNode(path + "/" + subdir[i] + "/img/")
					ImgListBefore = ImgMatch.ReadSingleNode(path + "/" + subdir[j] + "/img/")
					simiValue = ImgMatch.GetSimilarity(ImgListNow, ImgListBefore)
					print(subdir[i], subdir[j], ":", simiValue)
					if simiValue > 0.2:
						coordinates[i] = coordinates[j]
						currX, currY = coordinates[i][0], coordinates[i][1]

	coordinates.insert(0, [0, 0])
	print(coordinates)
	plt.plot([i[0] for i in coordinates], [i[1] for i in coordinates], "*-")
	plt.show()



if __name__ == '__main__':
    surf = cv2.xfeatures2d.SURF_create(300)
    bf = cv2.BFMatcher_create()
    main()

