import particlePickerModule as pPM
from particlePickerModule import dist
from os.path import isfile
from sys import argv
from math import pi, sin, cos

bigTimeStep = float(argv[1])
first_time = argv[2]
root_dir = argv[3]
x1c = float(argv[4])
y1c = float(argv[5])
x2c = float(argv[6])
y2c = float(argv[7])
ext = argv[8] #"txt" or "3d"

def sphere(x,y,z):
	rad = 1
	center = [0, 0, 0]
	r = dist([x, y, z],center)
	return (r < rad)

def two_sphere(x,y,z):
	rad1 = 1
	center1 = [1, 0, 0]
	rad2 = 1
	center2 = [-1, 0, 0]
	r = min( dist([x, y, z], center1), dist([x, y, z], center2) )
	return (r < rad)

def cyl(x,y,z):
	rad = 1
	center = [3, 3]
	r = dist([x, y], center)
	return (r < rad)

def ringsLOP(): #Makes ListOfPoints of rings above a center
	rads = [0.55, 0.30]
	zs	 = [0.40, 0.55]
	center = [2.56128, 0.48982, 0]
	steps = 10
	ret = []
	for rad,z in zip(rads,zs):
		for i in range(steps):
			theta = 2*pi*i/steps
			seed = [center[0]+rad*cos(theta), center[1]+rad*sin(theta), center[2]+z]
			ret.append(seed)
	print("Nearest Neighbor should have ~{} points".format(len(ret)))
	return ret

def ballLOP(): #Makes ListOfPoints of a ball around a center
	rads = [0.5, 1.0]
	center = [0, 0, 0]
	steps_vert = 10
	steps_horz = 10
	ret = []
	for rad in rads:
		for i in range(steps_vert):
			theta = 2*pi*i/steps_vert
			for j in range(steps_horz):
				phi = pi*j/steps_horz
				seed_x = center[0]+rad*sin(theta)*cos(phi)
				seed_y = center[1]+rad*sin(theta)*sin(phi)
				seed_z = center[2]+rad*cos(theta)
				seed = [seed_x, seed_y, seed_z]
				ret.append(seed)
	print("Nearest Neighbor should have ~{} points".format(len(ret)))
	return ret

folderDest = root_dir + 'seeds/'
datFolder = root_dir + 'dat/' 
sourceFile = datFolder + first_time + '.dat'
filesOrigin = root_dir + 'filesOrigin.txt'
reflectZ = 1
maxParticles = 10
volumeFunction = cyl

if not isfile(filesOrigin):
	pPM.genFilesOrigin(bigTimeStep,datFolder, float(first_time))

if (ext == 'txt'): #Bfields
###################
	lineNumbers = pPM.findInVolume(sourceFile, maxParticles, volumeFunction)

	#listOfPoints = ringsLOP() #points
	#listOfPoints = ballLOP()  #points
	#lineNumbers += pPM.nearestNeighbor(sourceFile, listOfPoints)

	#prev_seed = "/u/sciteam/wongsutt/scratch/SMS_2017_extint/abid_bot_v2.5/bin/particle_code/seeds/012400.000.txt"
	#listOfPoints = pPM.loadLOP(prev_seed)
	#lineNumbers = pPM.findNearestNeighbor(sourceFile, listOfPoints)

	pPM.genFiles(lineNumbers, filesOrigin, folderDest,reflectZ, 'txt')
####################


if (ext == '3d'): #Particles
	lineNumbers = pPM.findInVolume(sourceFile2, maxParticles, volumeFunction) #line number
	#lineNumbers += pPM.findInVolume(sourceFile, maxParticles, volumeFunction)

	listOfPoints = ringsLOP() #points
	#listOfPoints = ballLOP()  #points
	lineNumbers += pPM.nearestNeighbor(sourceFile, listOfPoints)

	#prev_seed = "/u/sciteam/wongsutt/scratch/SMS_2017_extint/abid_bot_v2.5/bin/particle_code/seeds/012400.000.txt"
	#listOfPoints = pPM.loadLOP(prev_seed)
	#lineNumbers = pPM.findNearestNeighbor(sourceFile, listOfPoints)

	pPM.genFiles(lineNumbers, filesOrigin, folderDest,reflectZ, '3d')

