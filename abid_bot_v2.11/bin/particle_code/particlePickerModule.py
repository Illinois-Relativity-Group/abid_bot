import numpy as np
from scipy import spatial

print("PP Module Loaded")

def dist(Avec, Bvec): #2d or 3d distance
	ret=0
	for x,y in zip(Avec, Bvec):
		ret += (float(x)-float(y))**2
	return ret**0.5

def genFiles(lineNumbers, filesOrigin, folderDest, reflectZ=1, ext='txt', idx=0):
	"""Takes list of line numbers and creates txt/3d files for Visit"""
	lineNumbers = list(set(lineNumbers)); #Remove duplicates
	lineNumbers.sort()
	print("Plot # {}".format(idx))
	print("We got {} particles".format(len(lineNumbers)))
	print("lineNumbers:",lineNumbers)

	if (folderDest[-1] != '/'): folderDest += '/'

	fil = open(filesOrigin, 'r')
	for datFile in fil:
		datFile = datFile.strip() #remove whitespace
		fName = datFile.split('/')[-1][:-4] #just filename not path, remove extension
		fName = "{:010.3f}".format(float(fName))
		myString = folderDest + fName + "_{}.".format(idx) + ext

		with open(datFile, 'r') as dat, open(myString, 'w') as saveFile:
			if (ext == '3d'): saveFile.write("x\ty\tz\trho\n")
			particleCount = 0

			for lineNumber, line in enumerate(dat):
				if (particleCount >= len(lineNumbers)): break #found all particles
				if (lineNumbers[particleCount] == lineNumber): 
					particleCount += 1
					data = line.split()
					saveString = "{}\t{}\t{}".format(data[1], data[2], data[3])

					if (ext == '3d'):
						rho = '1.0'
						if (len(data)>4): rho = data[4]
						endString ="\t{}\n".format(rho)

					else: endString = "\n"

					saveString += endString
					saveFile.write(saveString)

					if (reflectZ):
						saveString = "{}\t{}\t{}".format(data[1], data[2], '-'+data[3])
						saveString += endString
						saveString.replace('--','')
						saveFile.write(saveString)
	print("Done generating {} files!".format(ext))	

def genFilesOrigin(bigTimeStep, filesDir, startTime=0.0, endTime=-1):
	"""Creates list of all dat files used, writes to filesOrigin.txt"""
	from os import listdir
	print("Generating filesOrigin...")

	if (filesDir[-1] != '/'): filesDir += '/'
	myFiles = listdir(filesDir)
	
	keyMap = {}#key=time, value=file
	myFloats = []#times
	for file in myFiles:
		key = float(file[:-4])
		myFloats.append(key)
		keyMap[key] = file
	myFloats.sort()

	if (endTime == -1): largestNumber = myFloats[-1]
	else: largestNumber = endTime
	
	shortList = []
	timeList = []
	cur = startTime
	while (cur < largestNumber):
		timeList.append(cur)
		cur += bigTimeStep

	for time in timeList:#find closest times for particles
		closestTime = min(myFloats, key=lambda x:abs(x-time))
		shortList.append(keyMap[closestTime])
	print(len(shortList)," files found")

	filesOrigin = open(filesDir[:-4]+"filesOrigin.txt", 'w')
	for time in shortList:
		myString = filesDir + time +"\n"
		filesOrigin.write(myString)
	print("Done generating Files Origin!")
	filesOrigin.close()

	return

def findInVolume(sourceFile, maxParticles, volumeFunction, Seed=-1):
	"""Finds all particles in specified volume and returns line numbers"""
	
	print("Finding in volume...")
	import random
	lineNumbers = []
	with open(sourceFile, 'r') as datFile:
		for lineNumber, line in enumerate(datFile):
			data = line.split()
			x, y, z = data[1:4]
			if (volumeFunction(x,y,z)): lineNumbers.append(lineNumber)

	if (Seed != -1): random.seed(Seed)
	else: random.seed()

	random.shuffle(lineNumbers)
	return lineNumbers[:maxParticles]

def findInVolumeAllTimes(filesOrigin, maxParticles, volumeFunction, startIdx=-1, endIdx=-1):
	
	lineNumbers = []
	
	for fOrigin in filesOrigin:
		with open(fOrigin, 'r') as datFile:
			for lineNumber, line in enumerate(datFile):

				data = line.split()
				x, y, z = data[1:4]
				if(volumeFunction(x,y,z)): lineNumbers.append(lineNumber)

	lineNumbers = list(set(lineNumbers))
	random.shuffle(lineNumbers)
	return lineNumbers[:maxParticles]

def nearestNeighbor(sourceFile, listOfPoints):
	"""Takes in list of points and returns list of closest line numbers"""
	print("Finding Nearest Neighbor...")
	lineNumbers = []
	print("starting with {}  points".format(str(len(listOfPoints))))
	raw_data = np.loadtxt(sourceFile)
	xs = raw_data[:,1]; ys = raw_data[:,2]; zs = raw_data[:,3]
	tree = spatial.KDTree(list(zip(xs.ravel(), ys.ravel(), zs.ravel())))
	print("hello")
	for seed in listOfPoints:
		q = tree.query(seed); print(q)
		lineNumbers.append(q[1])
#	for seed in listOfPoints:
#		datFile = open(sourceFile, 'r')
#		minDist = 10000; minIdx = -1
#		for lineNumber, line in enumerate(datFile):
#			data = line.strip().split()
#			particle = [float(x) for x in data[1:4] ]
#			newDist = dist(seed, particle)
#			if newDist < minDist: minDist = newDist; minIdx = lineNumber
#		lineNumbers.append(minIdx) 
	lineNumbers = list(set(lineNumbers))
	print("Nearest Neighbor finds {} points".format(len(lineNumbers)))
	print("Done finding nearest neighbor")
	return lineNumbers

def loadLOP(filename):
	import numpy
	listOfPoints = numpy.loadtxt(filename)
	LOP = []
	for i in listOfPoints:
		LOP.append(i)
	return LOP

