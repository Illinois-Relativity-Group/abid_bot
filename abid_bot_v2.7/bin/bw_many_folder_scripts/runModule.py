from visit import *
from os.path import isfile, join
from os import listdir
import csv

########Operators########
def reflect():
	ref = ReflectAttributes()
	ref.reflections = (1,0,0,0,1,0,0,0)	
	AddOperator("Reflect")
	SetOperatorOptions(ref)
	print("Reflect set")
	
def box(y, addOp): #only show back half, reveals inside
	if (addOp):#so we don't have multiple box operators
		AddOperator("Box", 0)
	BoxAtts = BoxAttributes()
	BoxAtts.amount = BoxAtts.Some  # Some, All
	BoxAtts.minx = -2000
	BoxAtts.maxx = 2000
	BoxAtts.miny = y
	BoxAtts.maxy = 2000
	BoxAtts.minz = -2000
	BoxAtts.maxz = 2000
	BoxAtts.inverse = 0
	SetOperatorOptions(BoxAtts, 0)
	print("Box set")

def cylinder(x, y, r, addOp, z=1000): #for addOp argument, use 'frame==firstFrame'
	if (addOp):
		AddOperator("Cylinder")
	CylinderAtts = CylinderAttributes()
	CylinderAtts.point1 = (x, y, -z)
	CylinderAtts.point2 = (x, y, z)
	CylinderAtts.radius = r
	CylinderAtts.inverse = 0
	SetOperatorOptions(CylinderAtts)
	print("Cylinder set")

########Setup########
def LoadandDefine(database, symbol):#loads database, defines variable
	print("Loading {}...".format(symbol))
	OpenDatabase(database,0,"CarpetHDF5_2.1")
	DefineScalarExpression(symbol, "conn_cmfe(<" + database + "[0]id:MHD_EVOLVE--" + symbol + ">, <Carpet AMR-grid>)")
	print("...Done")

def setAnnotations():#sets background, sets up text
	Ann = AnnotationAttributes()
	Ann.backgroundMode = Ann.Solid
	Ann.backgroundColor = (55,118,255,255) #stu blue
	#Ann.backgroundColor = (0,0,0,255) #black
	#Ann.legendFlag = 0
	Ann.databaseInfoFlag = 0
	Ann.userInfoFlag = 0
	Ann.axes3D.visible = 0
	Ann.axes3D.triadFlag = 0
	Ann.axes3D.bboxFlag = 0
	SetAnnotationAttributes(Ann)

	# Clock
	txt = CreateAnnotationObject("Text2D")
	txt.position = (0.75, 0.95) # (x,y), where x and y range from 0 to 1
	txt.useForegroundForTextColor = 0
	txt.textColor = (255, 255, 255, 255)
	txt.fontBold = 1
	txt.fontFamily = txt.Times # Because I think Times looks cooler
	print("Annotations set up")
	return txt

def setSave(saveFolder): #sets saveattributes
	s = SaveWindowAttributes()
	s.format = s.PNG
	s.fileName = saveFolder
	s.width = 1920
	s.height = 1080
	s.screenCapture = 0
	s.stereo = 0 #Setting for 3D movie
	s.resConstraint = s.NoConstraint
	SetSaveWindowAttributes(s) 

def getSeeds(fil):#reads file and converts to tuples to be applied to plot
	file1 = open(fil,'r')
	data1 = csv.reader(file1,delimiter='\t')
	table1 = [row for row in data1]
	d1 = []
	for i in range(len(table1)):
		for j in range(len(table1[i])):
			d1.append(table1[i][j])
	d1 = map(float,d1)
	mytuple1 = tuple(d1)
	return mytuple1

def fill_bh(bh_func, bhNum, extrasDir, stateList):
	#When some frames in a folder have a BH and others don't, getting the right BH for each frame is
	#difficult.  This makes fake BH's off the screen so each frame will have a BH.
	#For BHBH cases, this fixes when BH1/2 and BH3 are both present
	if bh_func:
		for i in stateList:
			bhFile = extrasDir + 'bh' + bhNum + '_' + str(i).zfill(6) + '.3d'
			if bhNum == '3' and bh_formed() and isfile(bhFile):
				f = open(bhFile, 'r')
				g = open( extrasDir + 'bh1_' + str(i).zfill(6) + '.3d', 'w')
				h = open( extrasDir + 'bh2_' + str(i).zfill(6) + '.3d', 'w')
				f.readline()
				g.write("x\ty\tz\tbh1p\n")
				h.write("x\ty\tz\tbh2p\n")
				for line in f:
					g.write(line)
					h.write(line)
				f.close()
				g.close()
				h.close()
				rename(bhFile, extrasDir + 'unused3_' + str(i).zfill(6) + '.3d')
			elif not bhNum == '3' and not isfile(bhFile):
				f = open(bhFile, 'w')
				f.write("x\ty\tz\tbh" + bhNum + "p\n")
				f.write("-1\t-1\t100000\t0\n")
				f.write("1\t-1\t100000\t0\n")
				f.write("-1\t1\t100000\t0\n")
				f.write("1\t1\t100000\t0\n")
				f.close()

def getLists(extrasDir):
	#vars=[volumeXML,particleTXT,gridPointTXT,viewXML,TimeTXT,bh3D,bh23D,bh33D,trace3D,trace23D](stateList)
	fileNames=["volume_","particle_seeds_","grid_seeds_","view_","time_","bh1_","bh2_","bh3_","trace1_","trace2_"]
	vars=[]
	for fileName in fileNames:
		tmp = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find(fileName)  != -1 ]
		tmp.sort()
		vars.append(tmp)
	stateList = [ int(i[-8:-4]) for i in vars[3] ]
	stateList.sort()
	vars.append(stateList)
	print(vars)
	print(len(vars))
	return vars

def recheckBH(extrasDir):
	bh13D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh1_") != -1 ]
	bh13D.sort()

	bh23D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh2_") != -1 ]
	bh23D.sort()

	bh33D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh3_") != -1 ]
	bh33D.sort()
	return bh13D, bh23D, bh33D

def getCoM(CoMfile):
	cmfile = open(CoMfile, 'r')
	cmarray = cmfile.readline().split()
	CoM_x = float(cmarray[0])
	CoM_y = float(cmarray[1])
	CoM_z = float(cmarray[2])
	CoM = (CoM_x,CoM_y,CoM_z)
	print("CoM: {}".format(CoM))
	return CoM

########Plot########
def PlotBH(database, id, indx):
	ActivateDatabase(database)
	bhp = 'bh' + id + 'p'
	AddPlot("Pseudocolor",bhp)
	print("Add bh{} plot with index = {}".format(id, indx))

	Pseudo = PseudocolorAttributes()
	SetActivePlots(indx)
	AddOperator("Delaunay")
	reflect()

	Pseudo.colorTableName = "gray"
	Pseudo.legendFlag = 0
	Pseudo.lightingFlag = 0

	SetPlotOptions(Pseudo)

def PlotTrace(database, id, indx):
	ActivateDatabase(database)
	trace = 'trace' + id
	AddPlot("Pseudocolor", "rho")
	print("Add trace{} plot with index = {}".format(id, indx))

	SetActivePlots(indx)
	pointAtt = PseudocolorAttributes()
	pointAtt.pointType = pointAtt.Sphere
	pointAtt.minFlag = 1
	pointAtt.min = -1
	pointAtt.maxFlag = 1
	pointAtt.max = 0
	pointAtt.legendFlag = 0
	pointAtt.lightingFlag = 0
	if (id=='1'):
		pointAtt.pointSizePixels = 8   #8 or 10 if you use 2 colors 
	if (id=='2'):
		pointAtt.pointSizePixels = 4
		pointAtt.colorTableName = "PiYG" #Green at position 1

	SetPlotOptions(pointAtt)

def PlotB(database, indx):
	ActivateDatabase(database)
	AddPlot("Streamline","BVec")	#plot 1
	print("Add streamline plot with index = {}".format(indx))
	
	SetActivePlots(indx)
	reflect()
	return StreamlineAttributes()

def PlotVol(database, expression, indx):
	ActivateDatabase(database)
	AddPlot("Volume", expression)
	print("Add {} volume plot with index = {}".format(expression, indx))
	SetActivePlots(indx)
	reflect()
	return VolumeAttributes()

def PlotVelocity(database, expression, indx):
	ActivateDatabase(database)
	AddPlot("Vector", expression)
	print("Add velocity plot with index = {}".format(indx))
	SetActivePlots(indx)
	reflect()
	return VectorAttributes()


########Save########
def DrawAndSave(myView):
	DrawPlots()
	SetView3D(myView)
	print("\nView:")
	print(myView)
	SaveWindow()
	print("Saved Window")
