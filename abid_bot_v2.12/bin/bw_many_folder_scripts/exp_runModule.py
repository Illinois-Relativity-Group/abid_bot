from visit import *
import numpy as np
import os
from os.path import isfile, join
from os import listdir, rename
from fnmatch import fnmatch
import csv
import random
import sys
import time
import datetime


#some function taken from visit source code that wasn't loading for some reason
def EvalCubicSpline(t, allX, allY):
    n = len(allY)
    if((allX[0] > t) or (allX[n-1] < t)):
        raise Exception('t must be in the range between the first and last X')
    for i in range(1, n):
        if(allX[i] >= t):
            break
    i1 = max(i-2, 0)
    i2 = max(i-1, 0)
    i3 = i
    i4 = min(i+1, n-1)
    X = (allX[i1], allX[i2], allX[i3], allX[i4])
    Y = (allY[i1], allY[i2], allY[i3], allY[i4])
    dx = (X[2] - X[1])
    invdx = 1. / dx
    dy1   = (Y[2] + (Y[0] * -1.)) * (1. / (X[2] - X[0]))
    dy2   = (Y[2] + (Y[1] * -1.)) * invdx
    dy3   = (Y[3] + (Y[1] * -1.)) * (1. / (X[3] - X[1]))
    ddy2  = (dy2 + (dy1 * -1)) * invdx
    ddy3  = (dy3 + (dy2 * -1)) * invdx
    dddy3 = (ddy3 + (ddy2 * -1)) * invdx
    u = (t - X[1])
    return (Y[1] + dy1*u + ddy2*u*u + dddy3*u*u*(u-dx))


########Operators########
def reflect():
        ref = ReflectAttributes()
        ref.reflections = (1,0,0,0,1,0,0,0)
        AddOperator("Reflect")
        SetOperatorOptions(ref)
        print("Reflect set")
def threshold(xml):
        thresh = ThresholdAttributes()
        LoadAttribute(xml, thresh)
        AddOperator("Threshold")
        SetOperatorOptions(thresh)
        print("Threshold set")
def iso(xml):
        iso = IsosurfaceAttributes()
        LoadAttribute(xml, iso)
        AddOperator("Isosurface")
        SetOperatorOptions(iso)
        print("Isosurface set")
#wrapper for box functions. Choose which box slicing method you want.
def box(param, addOp):
        boxy(param, addOp)
def boxxyplane(height, addOp): #only show xy plane slice
        if (addOp):#so we don't have multiple box operators
                print("Adding Box operator")
                AddOperator("Box", 0)
        BoxAtts = BoxAttributes()
        BoxAtts.amount = BoxAtts.Some  # Some, All
        BoxAtts.minx = -2000
        BoxAtts.maxx = 2000
        BoxAtts.miny = -2000
        BoxAtts.maxy = 2000
        BoxAtts.minz = -height/2
        BoxAtts.maxz = height/2
        BoxAtts.inverse = 0
        SetOperatorOptions(BoxAtts, 0)
        print("Box set")

def boxz(z, addOp): #only show bottom half, reveals inside
        if (addOp):#so we don't have multiple box operators
            print("Adding Box operator")
            AddOperator("Box", 0)
        BoxAtts = BoxAttributes()
        BoxAtts.amount = BoxAtts.Some  # Some, All
        BoxAtts.minx = -2000
        BoxAtts.maxx = 2000
        BoxAtts.miny = -2000
        BoxAtts.maxy = 2000
        BoxAtts.minz = -2000
        BoxAtts.maxz = z
        BoxAtts.inverse = 0
        SetOperatorOptions(BoxAtts, 0)
        print("Box set")

def boxy(y, addOp): #only show back half, reveals inside
        if (addOp):#so we don't have multiple box operators
                print("Adding Box operator")
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

#NOT box slicing function. These two functions (box/sphere+spinvec) are used to plot single spin vector.
def boxspinvec(x,y,z,addOp):
        if (addOp):
                print("Adding Spinvec Box operator")
                AddOperator("Box", 0)
        BoxAtts = BoxAttributes()
        BoxAtts.amount = BoxAtts.Some  # Some, All
        BoxAtts.minx = x-0.001
        BoxAtts.maxx = x+0.001
        BoxAtts.miny = y-0.001
        BoxAtts.maxy = y+0.001
        BoxAtts.minz = z-0.001
        BoxAtts.maxz = z+0.001
        BoxAtts.inverse = 0
        SetOperatorOptions(BoxAtts, 0)
        print("Box set")

# def thinbox(addOp):
#         if addOp:
#                 print("Adding ThinBox operator")
#                 AddOperator("Box", 0)
#         BoxAtts = BoxAttributes()
#         LoadAttribute("/scratch1/08796/jnd2/abid_bot_low_mass_m/bin/bw_many_folder_scripts/atts/skinny_box.xml", BoxAtts)
# 	SetOperatorOptions(BoxAtts, 0)
#         print("Cylinder-like Box set")

def cylinder_velocity(addOp):
        if addOp:
                print("Adding Cylinder Operator")
                AddOperator("Cylinder", 0)
        CylAtts = CylinderAttributes()
        CylAtts.point1=(0, 0, -150)
        CylAtts.point2=(0, 0, 150)
        #CylAtts.point1=(0, 0, -1500)
        #CylAtts.point2=(0, 0, 1500)
        CylAtts.radius=25
        CylAtts.inverse=0
        SetOperatorOptions(CylAtts,0)
        print("Cylinder Set")


#clip
def clip(com, norm, addOp):
        if (addOp):
                print("adding clip operator")
                AddOperator("Clip", 0)
        ClipAtts = ClipAttributes()
        ClipAtts.plane1Origin = com
        ClipAtts.plane1Normal = norm
        SetOperatorOptions(ClipAtts, 0)
        print("clip op set")



def clip_vec(x,y,z,addOp):
        if addOp:
                print("Adding Clip Operator")
                AddOperator("Clip", 0)
        ClipAtts = ClipAttributes()
        # LoadAttribute("/scratch1/08796/jnd2/abid_bot_low_mass_m/bin/bw_many_folder_scripts/atts/Clip_atts.xml", ClipAtts)
        ClipAtts.funcType= ClipAtts.Sphere
        ClipAtts.center=(x,y,z)
        ClipAtts.radius=35
        ClipAtts.sphereInverse=0

        SetOperatorOptions(ClipAtts,0)
        print("Clip for Vectors Set")

#### When adding VELOCITY VECTORS, the mesh of our data is concentrated largely around the black hole which results too much
#### clustering in this region compared to in the jet. The clip_vec and clip_vec_inverse operators will separately plot  
#### vectors around the black hole and those in the jet. The clip_vec removes vecotrs in a sphere around the origin whereas
#### clip_vec_inverse removes everything outside the sphere around the origin. 
def clip_vec_inverse(x,y,z,addOp):
        if addOp:
                print("Adding Inverse Clip Operator")
                AddOperator("Clip", 0)
        InClipAtts = ClipAttributes()
        # LoadAttribute("/scratch1/08796/jnd2/abid_bot_low_mass_m/bin/bw_many_folder_scripts/atts/Clip_atts_inverse.xml", InClipAtts)
        InClipAtts.funcType= InClipAtts.Sphere
        InClipAtts.center=(x,y,z)
        InClipAtts.radius=0.1
        InClipAtts.sphereInverse=1
        SetOperatorOptions(InClipAtts,0)
        print("Inverse Clip for Vectors Set")
 
def spherespinvec(x,y,z,addOp):
        if (addOp):
                print("Adding spinvec sphere op")
                AddOperator("SphereSlice",0)
        SphereAtts=SphereSliceAttributes()
        SphereAtts.origin=(x,y,z)
        SphereAtts.radius=0.07  #0.08
        SetOperatorOptions(SphereAtts,0)
        print("Sphere set")

def cylinder(x1, y1, r, addOp, z1, height=1000, spinfile=""): #for addOp argument, use 'frame==firstFrame'
        if (addOp):
                AddOperator("Cylinder", 0)
        CylinderAtts = CylinderAttributes()
        print("x1, y1, z1: ", x1, y1, z1)
        CylinderAtts.point1 = (x1, y1, z1)
        if bool(spinfile):
                f = open(spinfile, "r")
                lines = f.readlines()
                x,y,z = lines[10].strip().split()
                normvec = np.array([float(x), float(y), float(z)])
                normvec /= np.linalg.norm(normvec)
                x2,y2,z2 = np.array([x1,y1,z1]) + height*normvec
        else:
                x2,y2,z2 = x1,y1,height
        print("x2, y2, z2: ", x2, y2, z2)
        CylinderAtts.point2 = (x2, y2, z2)
        CylinderAtts.radius = r
        CylinderAtts.inverse = 0
        SetOperatorOptions(CylinderAtts, 0)
        print("Cylinder set")

########Setup########
def LoadandDefine(database, symbol, prefix="MHD_EVOLVE"):#loads database, defines variable
        OpenDatabase(database,0,"CarpetHDF5_2.1")
        DefineScalarExpression(symbol, "conn_cmfe(<"+database+"[0]id:"+prefix+"--"+symbol+">, <Carpet AMR-grid>)")
        print("{} Loaded".format(symbol))

def setAnnotations(lightlist=[]):#sets background, sets up text
        Ann = AnnotationAttributes()
        Ann.backgroundMode = Ann.Solid
        Ann.backgroundColor = (55,118,255,255) #stu blue
        #Ann.backgroundColor = (0,0,0,255) #black
        Ann.legendInfoFlag = 0
        Ann.databaseInfoFlag = 0
        Ann.userInfoFlag = 0
        Ann.axes3D.visible = 0
        Ann.axes3D.triadFlag = 0
        Ann.axes3D.bboxFlag = 0
        SetAnnotationAttributes(Ann)

        # Light
        for i,lamp in enumerate(lightlist):
                light = GetLight(i)
                lighttypes = [light.Ambient, light.Object, light.Camera]
                light.enabledFlag = 1
                light.direction = lamp[0]
                light.brightness = lamp[1]
                if len(lamp) > 2:
                        light.type = lighttypes[lamp[2]]
                else:
                        light.type = light.Camera
                SetLight(i, light)

        # Rendering
        '''
        rend = RenderingAttributes()
        rend.scalableActivationMode = rend.Always
        rend.doShadowing = 1
        rend.shadowStrength = 0.5
        rend.doDepthCueing = 1
        rend.depthCueingAutomatic = 1
        SetRenderingAttributes(rend)
        '''

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
        s.outputToCurrentDirectory = 1
        s.fileName = saveFolder

        s.width = 1920
        s.height = 1080

#        s.width = 1080
#        s.height = 1080

        s.screenCapture = 0
        s.stereo = 0 #Setting for 3D movie
        s.resConstraint = s.NoConstraint
        SetSaveWindowAttributes(s)

def getSeeds(fil):
        with open(fil, 'r') as f:
                return tuple(map(float, f.read().split()))

'''
def getSeeds(fil):#reads file and converts to tuples to be applied to plot
        file1 = open(fil,'r')
        data1 = csv.reader(file1,delimiter='\t')
        table1 = [row for row in data1]
        d1 = []
        print(table1)
        for i in range(len(table1)):
                for j in range(len(table1[i])):
                        d1.append(table1[i][j])
        print(d1)
        d1 = map(float,d1)
        mytuple1 = tuple(d1)
        return mytuple1
'''

def fill_bh(bh_func, bhNum, extrasDir, stateList, bh_formed):
        # When some frames in a folder have a BH and others don't, getting the right BH for each
        # frame is difficult.  This makes fake BH's off the screen so each frame will have a BH.
        # For BHBH cases, this fixes when BH1/2 and BH3 are both present
        if bh_func():
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
                        elif bhNum != '3' and not isfile(bhFile):
                                f = open(bhFile, 'w')
                                f.write("x\ty\tz\tbh" + bhNum + "p\n")
                                f.write("-1\t-1\t100000\t0\n")
                                f.write("1\t-1\t100000\t0\n")
                                f.write("-1\t1\t100000\t0\n")
                                f.write("1\t1\t100000\t0\n")
                                f.close()

def getLists(extrasDir, numBfieldPlots=1):
        #vars=[volumeXML,particleTXT,gridPointTXT,viewXML,TimeTXT,bh3D,bh23D,bh33D,trace3D,trace23D](stateList)
        fileNames1 = ["volume_", "grid_seeds_0_", "grid_seeds_1_", "view_", "time_", "bh1_", "bh2_", "bh3_", "trace1_", "trace2_", "spin_", "grid_Stream_0", "grid_Stream_1", "hplus_", "hcross_"]
        fileNames2 = [("particle_seeds_","txt"), ("Stream_","xml")]
        xmls=[]
        for fileName in fileNames1:
                tmp = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and\
                                f.find(fileName)  != -1 ]
                tmp.sort()
                xmls.append(tmp)
        for filetuple in fileNames2:
                fileName = filetuple[0]
                end = filetuple[1]
                tmp = {}
                for i in range(numBfieldPlots):
                        tmp_tmp = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find(fileName) != -1 and f.find("_{0}.{1}".format(i,end)) != -1 ]
                        tmp_tmp.sort()
                        tmp[fileName + str(i)] = tmp_tmp
                xmls.append(tmp)

        stateList = [ int(i[-8:-4]) for i in xmls[3] ]
        stateList.sort()
        xmls.append(stateList)
        print(xmls)
        print(len(xmls))
        return xmls

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
def PlotBH(database, idx, indx, ref=1):
        ActivateDatabase(database)
        bhp = 'bh' + idx + 'p'
        AddPlot("Pseudocolor",bhp)
        print("Add bh{} plot with index = {}".format(idx, indx))

        Pseudo = PseudocolorAttributes()
        SetActivePlots(indx)
        AddOperator("Delaunay")
        if ref:
                reflect()
        Pseudo.colorTableName = "gray"
        Pseudo.legendFlag = 0
        Pseudo.lightingFlag = 0

        SetPlotOptions(Pseudo)

def PlotTrace(database, idx, indx):
        ActivateDatabase(database)
        trace = 'trace' + idx
        AddPlot("Pseudocolor", "rho")
        print("Add trace{} plot with index = {}".format(idx, indx))

        SetActivePlots(indx)
        pointAtt = PseudocolorAttributes()
        pointAtt.pointType = pointAtt.Sphere
        pointAtt.minFlag = 1
        pointAtt.min = -1
        pointAtt.maxFlag = 1
        pointAtt.max = 0
        pointAtt.legendFlag = 0
        pointAtt.lightingFlag = 0
        if (idx=='1'):
                pointAtt.pointSizePixels = 8   #8 or 10 if you use 2 colors
                pointAtt.colorTableName = "blueParticles" #blue particles
        if (idx=='2'):
                pointAtt.pointSizePixels = 8
                pointAtt.colorTableName = "redParticles" #red particles

        SetPlotOptions(pointAtt)

def PlotB(database, indx, ref=1, ct='streamlines_white'):
        ActivateDatabase(database)
        AddPlot("Pseudocolor","BVec")   #plot 1
        print("Add streamline plot with index = {}".format(indx))

        SetActivePlots(indx)
        if ref:
                reflect()

        pseudoAtt = PseudocolorAttributes()
        pseudoAtt.legendFlag = 0
        pseudoAtt.minFlag = 1
        pseudoAtt.maxFlag = 1
        pseudoAtt.lightingFlag = 1
        pseudoAtt.colorTableName = ct
        pseudoAtt.useBelowMinColor = 1
        pseudoAtt.belowMinColor = (255, 255, 255, 255)
        pseudoAtt.useAboveMaxColor = 1
        pseudoAtt.aboveMaxColor = (255, 255, 255, 255)
        pseudoAtt.lineWidth = 3
        SetPlotOptions(pseudoAtt)

        AddOperator("IntegralCurve")
        return IntegralCurveAttributes()

def PlotVol(database, expression, indx, ref=1):
        ActivateDatabase(database)
        AddPlot("Volume", expression)
        print("Add {} volume plot with index = {}".format(expression, indx))
        SetActivePlots(indx)

        limit_levels = 0
        ##### EXPERIMENTAL MESH USAGE #####
        if limit_levels:
                silr = SILRestriction() #refinement level object
                level_category = silr.Categories()[0]
                sets = silr.SetsInCategory(level_category) #list of refinement levels
                sets_to_turn_off = sets[0:4] #refinement levels to turn off. 0 is outermost refinement level. THIS IS WHAT YOU NEED TO CHANGE
                print("Turning off density refinement levels: {}".format(sets_to_turn_off))
                for myset in sets_to_turn_off:
                        silr.TurnOffSet(myset) #Turn off refinement levels
                SetPlotSILRestriction(silr) #Set refinement level object
        ##### END EXPERIMENTAL #####

        if ref:
                reflect()
        return VolumeAttributes()

def PlotPseudo(database, expression, indx, ref=1):
        ActivateDatabase(database)
        AddPlot("Pseudocolor", expression)
        print("Add {} pseudo plot with index = {}".format(expression, indx))
        SetActivePlots(indx)
        if ref:
                reflect()
        return PseudocolorAttributes()

def PlotVelocity(database, expression, indx, ref=1):
        ActivateDatabase(database)
        AddPlot("Vector", expression)
        print("Add velocity plot with index = {}".format(indx))
        SetActivePlots(indx)

        # ##### EXPERIMENTAL MESH USAGE #####
        # silr = SILRestriction() #refinement level object
        # level_category = silr.Categories()[0]
        # sets = silr.SetsInCategory(level_category) #list of refinement levels
        # sets_to_turn_off = sets[0:3] #refinement levels to turn off. 0 is outermost refinement level. THIS IS WHAT YOU NEED TO CHANGE
        # print("Turning off velocity refinement levels: {}".format(sets_to_turn_off))
        # for myset in sets_to_turn_off:
        #       silr.TurnOffSet(myset) #Turn off refinement levels
        # SetPlotSILRestriction(silr) #Set refinement level object
        # ##### END EXPERIMENTAL #####
 
        if ref:
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


###################################################################################################
###################################################################################################
###################################################################################################


class VisitPlot:

        def __init__(self, plot_opts, arg_list):

                self.plot_opts = plot_opts

                (self.PlotDensAsVol,    # Plot density in a volume plot
                self.PlotDensAsIso,             # Plot density in a pseudocolor plot as isosurfaces
                self.PlotDensLinear,    # Plot linear scale density rather than log scale
                self.PlotVel,                   # Plot velocity arrows
                self.PlotSpinVec,               # Plot BH spin vector
                self.PlotBsq2r,                 # Plot B squared over 2 rho as volume
                self.PlotBsq2r_iso,             # Plot B squared over 2 rho as iso
                self.PlotVelCustom,             # Plot velocity arrows with custom generated .vtk database
                self.PlotGW2D,                  # Plot Gravitational waves 2D
                self.PlotGW3D,                  # Plot Gravitational waves 3D
                self.Plotg00,                   # Plot g00 from metric
                self.refPlot,                   # Reflect plot over xy plane
                self.cutPlot,                   # Only show back half (y>0), needs view like: (0,-x,y)
                self.bgcolor
                ) = self.plot_opts
                print("XDXDXDXDXDXDXXXDXDXDXDX")
                print(self.refPlot, self.cutPlot)
                print("XDXDXDXDXDXDXXXDXDXDXDX")
                self.arg_list = arg_list

                self.h5dir, self.extrasDir, self.saveFolder, self.rank, self.total_ranks, self.numBfieldPlots, self.vector1XML, self.vector2XML, self.spinvecXML ,self.bsq2rXML, self.bsq2r_pseudoXML, self.bsq2r_isoXML, self.max_density, self.rho_pseudoXML, self.rho_isoXML, self.g00_pseudoXML, self.g00_isoXML, self.VelCustomFile, self.gw3D_volXML = self.arg_list

                self.rank                       = int(self.rank)
                self.total_ranks        = int(self.total_ranks)
                self.myView                     = GetView3D()

                # Append a '/' if necessary
                self.h5dir              += '/' if self.h5dir[-1] != '/'         else ''
                self.extrasDir  += '/' if self.extrasDir[-1] != '/' else ''

                # The first line picks out the files that contain "volume_" in the directory, extrasDir
                # The sorting should sort in numerical order
                (self.volumeXML, self.gridPointsTXT_0, self.gridPointsTXT_1, self.viewXML, self.timeTXT, self.bh13D, self.bh23D, self.bh33D, self.trace3D, self.trace23D, self.spinvtk, self.gridStream_0, self.gridStream_1, self.hplus, self.hcross, self.particlesDict, self.StreamDict, self.stateList) = getLists(self.extrasDir, self.numBfieldPlots)

                self.CheckFiles()

                self.rho_bdir           = self.h5dir + "rho_b.file_* database"
                self.Bxdir                      = self.h5dir + "Bx.file_* database"
                self.Bydir                      = self.h5dir + "By.file_* database"
                self.Bzdir                      = self.h5dir + "Bz.file_* database"
                self.smallb2dir         = self.h5dir + 'smallb2.file_* database'
                self.vxdir                      = self.h5dir + "vx.file_* database"
                self.vydir                      = self.h5dir + "vy.file_* database"
                self.vzdir                      = self.h5dir + "vz.file_* database"
                self.g00dir                     = self.h5dir + "g00.file_* database"
                self.bh1dir             = self.extrasDir + "bh1_*.3d database"
                self.bh2dir             = self.extrasDir + "bh2_*.3d database"
                self.bh3dir             = self.extrasDir + "bh3_*.3d database"
                self.trace1dir          = self.extrasDir + "trace1_*.3d database"
                self.trace2dir          = self.extrasDir + "trace2_*.3d database"
                self.spinvtk            = self.extrasDir + "spin_*.vtk database"
                self.hplus              = self.extrasDir + "hplus_*.vtk database"
                self.hcross              = self.extrasDir + "hcross_*.vtk database"

                self.tot_frames = len(self.stateList)
                self.firstFrame = int(round(( self.rank*1.0 /self.total_ranks)*self.tot_frames))
                self.lastFrame  = int(round(((self.rank+1.0)/self.total_ranks)*self.tot_frames))

                self.dbs, self.plot_idx = self.LoadDatabases()
                self.txt = self.SetAnnotations(self.bgcolor)
                print('\tSet up complete! VisitPlot created')

        def __repr__(self):
                plots = ['PlotDensAsVol', 'PlotDensAsIso', 'PlotDensLinear', 'PlotVel', 'PlotSpinVec', 'PlotBsq2rAsVol', 'PlotBsq2rAsIso', 'Plotg00', 'PlotGW2D', 'PlotGW3D', 'refPlot', 'cutPlot']
                args = ['h5dir', 'extrasDir', 'saveFolder', 'rank', 'total ranks', 'numBfieldPlots', 'vectorXML', 'vector2XML','spinvecXML', 'bsq2rXML', 'bsq2r_pseudoXML', 'bsq2r_isoXML', 'max_density', 'rho_pseudoXML', 'rho_isoXML', 'g00_pseudoXML', 'g00_isoXML', 'VelCustomFile', 'gw3d_volXML']

                myFrame = ''
                for plt, opt in zip(plots, self.plot_opts):
                        myFrame += str(plt).ljust(15)[:15] + '= %s\n' % opt
                myFrame += '\n'
                for arg, val in zip(args, self.arg_list):
                        myFrame += str(arg).ljust(15)[:15] + '= %s\n' % val
                return myFrame
        

        def density_vol(self):          return self.PlotDensAsVol > 0
        def density_iso(self):          return self.PlotDensAsIso > 0
        def density_linear(self):       return self.PlotDensLinear > 0
        def bsq2r(self):                        return self.PlotBsq2r > 0 and not self.density_vol()
        def bsq2r_iso(self):                    return self.PlotBsq2r_iso > 0 and not self.density_vol()
        def velocity(self):                     return self.PlotVel > 0
        def spinvec(self):                      return self.PlotSpinVec > 0
        def gw2D(self):                           return self.PlotGW2D > 0
        def gw3D(self):                           return self.PlotGW3D > 0
        def g00(self):                          return self.Plotg00 > 0
        def bh_formed(self):            return len(self.bh13D) > 0
        def binary_formed(self):        return len(self.bh23D) > 0
        def merge_formed(self):         return len(self.bh33D) > 0
        def trace1(self):                       return len(self.trace3D) > 0
        def trace2(self):                       return len(self.trace23D) > 0
        def particles(self):            return len(self.particlesDict) > 0 and len(self.particlesDict["particle_seeds_0"]) > 0
        def gridPoints(self):           return len(self.gridPointsTXT_0) > 0
        def fields(self):                       return self.particles() or self.gridPoints()

        def idx(self, name):
                return self.plot_idx.index(name)

        def LoadAttr(self, path, name):
                try: LoadAttribute(path, self.__dict__[name])
                except:
                        if type(path) == type(self.__dict__[name]):
                                setattr(self, name, path)
                        else:
                                print("'{}' is neither a string nor a view object, using VisIt default instead".format(path))


#############################################

        def CheckFiles(self):
                #This adjusts the bh_*.3d files so that the black hole doesn't show up earlier than it's supposed to
                #This will use bh3 data to overwrite the empty bh1 and bh2 files whenever bh1 and bh3 appear together in one folder. Probably won't do anything but necessary for BHBH cases
                fill_bh(self.bh_formed    , '1', self.extrasDir, self.stateList, self.bh_formed)
                fill_bh(self.binary_formed, '2', self.extrasDir, self.stateList, self.bh_formed)
                fill_bh(self.merge_formed , '3', self.extrasDir, self.stateList, self.bh_formed)

                #Checking bh files again ################
                self.bh13D, self.bh23D, self.bh33D = recheckBH(self.extrasDir)

                print("PlotGW2D is " + str(self.PlotGW2D))

                print("density:         {}".format(self.density_vol() or self.density_iso()))
                print("bsq2r:           {}".format(self.bsq2r()))
                print("bsq2r_iso:       {}".format(self.bsq2r()))
                print("fields:          {}".format(self.fields()))
                print("particles:       {}".format(self.particles()))
                print("gridPoints:      {}".format(self.gridPoints()))
                print("trace1:          {}".format(self.trace1()))
                print("trace2:          {}".format(self.trace2()))
                print("velocity:        {}".format(self.velocity()))
                print("BH1:             {}".format(self.bh_formed()))
                print("BH2:             {}".format(self.binary_formed()))
                print("BH3:             {}".format(self.merge_formed()))
                print("GW2D:            {}".format(self.gw2D()))
                print("GW3D:            {}".format(self.gw3D()))
                #add check for spinvtk file

#############################################

        def LoadDatabases(self):
                dbs = []
                plot_idx = []

                if self.density_vol() or self.density_iso():
                        LoadandDefine(self.rho_bdir, "rho_b")
                        #LoadandDefine(self.smallb2dir, "smallb2")
                        #DefineScalarExpression("logbsq2r","log10(<smallb2>/(2*<rho_b>), -200)")
                        DefineScalarExpression("logrho","log10(<MHD_EVOLVE--rho_b>/" + self.max_density + ")")
                        OpenDatabase("/anvil/scratch/x-rnarasimhan/abid_bot_gw/box.3d")
                        dbs += [self.rho_bdir]
                        plot_idx += ["density"]
                        #plot_idx += ["3dbox"]

                if self.bsq2r() or self.bsq2r_iso():
                        LoadandDefine(self.rho_bdir, "rho_b")
                        LoadandDefine(self.smallb2dir, "smallb2")
                        #LoadandDefine(self.vxdir, "vx")
                        #LoadandDefine(self.vydir, "vy")
                        #LoadandDefine(self.vzdir, "vz")
                        #dbs += [self.vxdir, self.vydir, self.vzdir]
                        #long_expression = ("(<smallb2>/(2*<rho_b>))*"
                        #                   "(1-(((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)^2)/((<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>))))/"
#                                           "((1.0)*"
#                                           "(1-(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*"
#                                           "(1-(((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)^2)/((<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>))))))")
#                        DefineScalarExpression("temp", long_expression)
#                        expression = "log10(sqrt(<temp>*<temp>/(1-(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>))), -200)"
#
#                        DefineScalarExpression("logbsq2r", expression)
                        DefineScalarExpression("logbsq2r", "log10(<smallb2>/(2*<rho_b>))")
                        dbs += [self.smallb2dir, self.rho_bdir]
                        plot_idx += ["bsq2r"]

                if self.fields():
                        LoadandDefine(self.Bxdir, "Bx")
                        print("loaded Bx")
                        LoadandDefine(self.Bydir, "By")
                        print("loaded By")
                        LoadandDefine(self.Bzdir, "Bz")
                        print("loaded Bz")
                        DefineVectorExpression("BVec","{Bx,By,Bz}")
                        print("defined vector expression")
                        dbs += [self.Bxdir, self.Bydir, self.Bzdir]
                        if self.particles():
                                for i in range(self.numBfieldPlots):
                                        plot_idx += ["particles{}".format(i)]
                        if self.gridPoints(): 
                                plot_idx += ["gridPoints_0"]
                                plot_idx += ["gridPoints_1"]

                if self.bh_formed():
                        print("Loading bh1's...")
                        OpenDatabase(self.bh1dir)
                        dbs += [self.bh1dir]
                        plot_idx += ["bh1"]

                if self.binary_formed():
                        print("Loading bh2's...")
                        OpenDatabase(self.bh2dir)
                        dbs += [self.bh2dir]
                        plot_idx += ["bh2"]

                if self.merge_formed():
                        print("Loading bh3's...")
                        OpenDatabase(self.bh3dir)
                        dbs += [self.bh3dir]
                        plot_idx += ["bh3"]

                if self.trace1():
                        print("Loading Particle Tracer...")
                        OpenDatabase(self.trace1dir, 0, "Point3D_1.0")
                        dbs += [self.trace1dir]
                        plot_idx += ["trace1"]

                if self.trace2():
                        print("Loading Particle Tracer 2...")
                        OpenDatabase(self.trace2dir, 0, "Point3D_1.0")
                        dbs += [self.trace2dir]
                        plot_idx += ["trace2"]

                if self.velocity():
                        #if not self.density_vol() and not self.density_iso():
                        #        LoadandDefine(self.rho_bdir, "rho_b")
                        #        dbs += [self.rho_bdir]
                        #        plot_idx += ['density']

                        if not self.bsq2r() and not self.bsq2r_iso():
                               LoadandDefine(self.smallb2dir, "smallb2")
                               LoadandDefine(self.rho_bdir, "rho_b")
               #                LoadandDefine(self.smallb2dir, "smallb2")
               #                LoadandDefine(self.Bxdir, "Bx")
               #                LoadandDefine(self.Bydir, "By")
               #                LoadandDefine(self.Bzdir, "Bz")
                        #        LoadandDefine(self.vxdir, "vx")
                        #        LoadandDefine(self.vydir, "vy")
                        #        LoadandDefine(self.vzdir, "vz")
                               #DefineScalarExpression("logbsq2r","log10(<smallb2>/(2*<rho_b>), -200)")
#                               print("============ PRINT 1 =============")
#                               DefineScalarExpression("cosX", "conn_cmfe( (<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>) / (sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)), <Carpet AMR-grid>)")
#                               print("============ PRINT 2 =============")
#                               DefineScalarExpression("gamma", "conn_cmfe( 1 / sqrt(1 - (<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)  ), <Carpet AMR-grid>)")
#                               print("============ PRINT 3 =============")
#                               DefineScalarExpression("bsq2r", "conn_cmfe(<smallb2>/(2*<rho_b>), <Carpet AMR-grid>)")
#                               print("============ PRINT 4 =============")
#                               DefineScalarExpression("fac", "conn_cmfe( (1 - <cosX>*<cosX>) / (<gamma>*(1 - (<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*(1-<cosX>*<cosX>)) ), <Carpet AMR-grid>)")
#                               print("============ PRINT 5 =============")
#                               DefineScalarExpression("logbsq2r", "log10(<fac>*<bsq2r>)")
                        #        long_expression = ("log10(( <smallb2>/(2*<rho_b>))*((1-"
                        #                           "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))*"
                        #                           "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>))))/"
                        #                           "((1/sqrt(1-(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)))*"
                        #                           "(1-((<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*(1-"
                        #                           "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))*"
                        #                           "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))))))), -200)")
                               #long_expression = ("log10(( <MHD_EVOLVE--smallb2>/(2*<MHD_EVOLVE--rho_b>))*((1-"
                               #                   "((<MHD_EVOLVE--Bx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--vz>)/(sqrt(<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)*sqrt(<MHD_EVOLVE--Bx>*<MHD_EVOLVE--Bx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--By>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--Bz>)))*"
                               #                   "((<MHD_EVOLVE--Bx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--vz>)/(sqrt(<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)*sqrt(<MHD_EVOLVE--Bx>*<MHD_EVOLVE--Bx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--By>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--Bz>))))/"
                               #                   "((1/sqrt(1-(<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)))*"
                               #                   "(1-((<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)*(1-"
                               #                   "((<MHD_EVOLVE--Bx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--vz>)/(sqrt(<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)*sqrt(<MHD_EVOLVE--Bx>*<MHD_EVOLVE--Bx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--By>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--Bz>)))*"
                               #                     "((<MHD_EVOLVE--Bx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--vz>)/(sqrt(<MHD_EVOLVE--vx>*<MHD_EVOLVE--vx>+<MHD_EVOLVE--vy>*<MHD_EVOLVE--vy>+<MHD_EVOLVE--vz>*<MHD_EVOLVE--vz>)*sqrt(<MHD_EVOLVE--Bx>*<MHD_EVOLVE--Bx>+<MHD_EVOLVE--By>*<MHD_EVOLVE--By>+<MHD_EVOLVE--Bz>*<MHD_EVOLVE--Bz>)))))))))")
               #                long_expression = ("log10(( <MHD_EVOLVE--smallb2>/(2*<MHD_EVOLVE--rho_b>))*((1-"
               #                    "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))*"
               #                    "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>))))/"
               #                    "((1/sqrt(1-(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)))*"
               #                    "(1-((<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*(1-"
               #                    "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))*"
               #                    "((<Bx>*<vx>+<By>*<vy>+<Bz>*<vz>)/(sqrt(<vx>*<vx>+<vy>*<vy>+<vz>*<vz>)*sqrt(<Bx>*<Bx>+<By>*<By>+<Bz>*<Bz>)))))))))")
                               print("============ PRINT 1 =============")
                               DefineScalarExpression("logbsq2r", "log10(<smallb2>/(2*<rho_b>))")
                               print("============ PRINT 2 =============")
                               dbs += [self.smallb2dir]
                               plot_idx += ["bsq2r"]
                        
                        LoadandDefine(self.vxdir, 'vx')
                        LoadandDefine(self.vydir, 'vy')
                        LoadandDefine(self.vzdir, 'vz')

                        DefineVectorExpression("vVec","{vx,vy,vz}")

                        # DefineVectorExpression("vVec_temp","{vx,vy,vz}")
                        # DefineVectorExpression("vVec","if(gt(magnitude(vVec_temp), 0.5) , vVec_temp , {0,0,0})") #Remove small arrows
                        # DefineVectorExpression("vVec","if(gt(logbsq2r, -1.0), vVec_temp, {0,0,0})") #Only show arrows around jet, need to load smallb2 database
                        dbs += [self.vxdir,self.vydir,self.vzdir]
                        plot_idx += ["vel1"]
                if self.velocity():
                        #if not self.density_vol() and not self.density_iso():
                        #        LoadandDefine(self.rho_bdir, "rho_b")
                        #        dbs += [self.rho_bdir]
                        #        plot_idx += ['density']

                        #if not self.bsq2r() and self.density_vol():
                        #        LoadandDefine(self.smallb2dir, "smallb2")
                        #        DefineScalarExpression("logbsq2r","log10(<smallb2>/(2*<rho_b>), -200)")
                        #        dbs += [self.smallb2dir]
                        #        plot_idx += ["bsq2r"]
                        
                        #LoadandDefine(self.vxdir, 'vx')
                        #LoadandDefine(self.vydir, 'vy')
                        #LoadandDefine(self.vzdir, 'vz')
                        #DefineVectorExpression("vVec_temp","{vx,vy,vz}")
                        # DefineVectorExpression("vVec","if(gt(magnitude(vVec_temp), 0.5) , vVec_temp , {0,0,0})") #Remove small arrows
                        #DefineVectorExpression("vVec","if(gt(logbsq2r, -0.5), vVec_temp, {0,0,0})") #Only show arrows around jet, need to load smallb2 database
                        dbs += [self.vxdir,self.vydir,self.vzdir]
                        plot_idx += ["vel2"]

                if self.spinvec():
                        #if not self.density_vol() and not self.density_iso():
                        #       LoadandDefine(self.rho_bdir, "rho_b")
                        #       dbs += [self.rho_bdir]
                        #       plot_idx += ['density']

                        OpenDatabase(self.spinvtk,0,"VTK")
                        dbs+=[self.spinvtk]
                        plot_idx += ["spin"]

                if self.g00():
                        print("Loading g00...")
                        LoadandDefine(self.g00dir, 'g00', 'BSSN')
                        dbs += [self.g00dir]
                        plot_idx += ["g00"]

                #if we have velocity plot and not bsq2r plot, then the bsq2r plot_idx must be at the end or else indexing will be thrown off
                if self.velocity() and not (self.bsq2r() or self.bsq2r_iso()):
                        bsq2r_idx = plot_idx.index("bsq2r")
                        plot_idx = plot_idx[:bsq2r_idx] + plot_idx[bsq2r_idx+1:] + ["bsq2r"]

                if self.gw2D():
                        if any(filename.startswith("hplus")  for filename in os.listdir(self.extrasDir)):
                                OpenDatabase(self.hplus, 0, "VTK")
                                dbs+=[self.hplus]
                        else:
                                OpenDatabase(self.hcross, 0, "VTK")
                                dbs+=[self.hcross]
                        DefineScalarExpression("modifiedwave", "<GW-FIELD>/(exp(-polar_radius(mesh)+10)+1)/(exp(-70 +polar_radius(mesh))+1)")
                        print("modifiedwave Loaded")

                        
                        
                        plot_idx += ["gw2D"]
                        plot_idx += ["gw2Dmesh"]
                        print("Loaded gw2D database")

                if self.gw3D():
                        if any(filename.startswith("hplus")  for filename in os.listdir(self.extrasDir)):
                                OpenDatabase(self.hplus, 0, "VTK")
                                dbs+=[self.hplus]
                        else:
                                OpenDatabase(self.hcross, 0, "VTK")
                                dbs+=[self.hcross]
                        #DefineScalarExpression("modifiedwave", "<GW-FIELD>/(exp(-polar_radius(mesh)+10)+1)/(exp(-70 +polar_radius(mesh))+1)")
                        DefineScalarExpression("modifiedwave", "<GW-FIELD>/(exp(-polar_radius(mesh)+10)+1)/(exp(-300 +polar_radius(mesh))+1)")
                        AddPlot("Volume","modifiedwave")
                        print("modifiedwave Loaded")

                        self.gw3DvolAtts = VolumeAttributes()
                        
                        plot_idx += ["gw3D"]
                        print("Loaded gw3D database")


                print("\tDone")
                print("Databases loaded: {}\n".format(dbs))
                print("Plotting: {}".format(plot_idx))

                CreateDatabaseCorrelation("Everything", dbs, 0)
                time.strftime("%Y-%m-%d %H:%M:%S")
                return (dbs, plot_idx)



        def SetAnnotations(self, bgcolor='blue', lightlist=[]):
                #####   Set up the annotations
                Ann = AnnotationAttributes()
                Ann.backgroundMode = Ann.Solid
                if self.PlotGW2D:
                        Ann.backgroundColor = (56, 140, 180, 255) #same color as GW_plane
                elif bgcolor=='blue':
                        Ann.backgroundColor = (55,118,255,255) #stu blue
                elif bgcolor=='black':
                        Ann.backgroundColor = (0,0,0,255) #black
                elif bgcolor=='grey' or bgcolor=='gray':
                        Ann.backgroundColor = (145,145,145,255)
                else:
                        Ann.backgroundColor = (55,118,255,255) #stu blue default
                Ann.legendInfoFlag = 0
                Ann.databaseInfoFlag = 0
                Ann.userInfoFlag = 0
                Ann.axes3D.visible = 0
                Ann.axes3D.triadFlag = 0
                Ann.axes3D.bboxFlag = 0
                SetAnnotationAttributes(Ann)

                #####   light list contains [(direction), brightness, type=camera]
                #lightlist = [[(0, 0, -1), 1], [(0, -1, 0), 0.6 ], [(-0.026, 0.978, -0.207), 0.75]]
                #lightlist = [[(0, 0, -1), 1], [(0, 0, -1), 0.75, 0 ]]

                # Light
                for i,lamp in enumerate(lightlist):
                        light = GetLight(i)
                        lighttypes = [light.Ambient, light.Object, light.Camera]
                        light.enabledFlag = 1
                        light.direction = lamp[0]
                        light.brightness = lamp[1]
                        if len(lamp) > 2:
                                light.type = lighttypes[lamp[2]]
                        else:
                                light.type = light.Camera
                        SetLight(i, light)

                #save window settings
                setSave(self.saveFolder)

                # Clock
                txt = CreateAnnotationObject("Text2D")
                txt.position = (0.75, 0.95) # (x,y), where x and y range from 0 to 1
                txt.useForegroundForTextColor = 0
                txt.textColor = (255, 255, 255, 255)
                txt.fontBold = 1
                txt.fontFamily = txt.Times # Because I think Times looks cooler
                print("Annotations set up")

                return txt

#############################################

        def SetPlots(self):
                DeleteAllPlots()

                if self.density_vol():
                        if self.density_linear(): self.vol = PlotVol(self.rho_bdir, "rho_b", self.idx("density"), self.refPlot)
                        else:                     self.vol = PlotVol(self.rho_bdir, "logrho", self.idx("density"), self.refPlot)
                if self.density_iso():
                        if self.density_linear(): self.rho_atts = PlotPseudo(self.rho_bdir, "rho_b", self.idx("density"), self.refPlot)
                        #else:                     self.rho_atts = PlotPseudo(self.rho_bdir, "logbsq2r",self.idx("density"), self.refPlot)
                        else:                     self.rho_atts = PlotPseudo(self.rho_bdir, "logrho",self.idx("density"), self.refPlot)
                if self.bsq2r():                  self.bsq_atts = PlotVol(self.smallb2dir, "logbsq2r", self.idx("bsq2r"), self.refPlot)
                if self.bsq2r_iso():              self.bsq_iso_atts = PlotPseudo(self.smallb2dir, "logbsq2r", self.idx("bsq2r"), self.refPlot)
                if self.particles():
                        self.stream_particles_dict = {}
                        print("Hey hi hello whats up")
                        print(self.stream_particles_dict)
                        for i in range(self.numBfieldPlots):
                                self.stream_particles_dict["stream_particles_{}".format(i)] = PlotB(self.Bxdir, self.idx("particles{}".format(i)), ref=self.refPlot, ct='streamlines_white')

                if self.gridPoints():             
                        self.stream_gridPoints_0 = PlotB(self.Bxdir, self.idx("gridPoints_0"), ref=self.refPlot, ct='streamlines_white')
                        self.stream_gridPoints_1 = PlotB(self.Bxdir, self.idx("gridPoints_1"), ref=self.refPlot, ct='streamlines_white')
                if self.bh_formed():              PlotBH(self.bh1dir, '1', self.idx("bh1"), self.refPlot)
                if self.binary_formed():          PlotBH(self.bh2dir, '2', self.idx("bh2"), self.refPlot)
                if self.merge_formed():           PlotBH(self.bh3dir, '3', self.idx("bh3"), self.refPlot)
                if self.trace1():                 PlotTrace(self.trace1dir, '1', self.idx("trace1"))
                if self.trace2():                 PlotTrace(self.trace2dir, '2', self.idx("trace2"))
                if self.velocity():               self.vector1_atts = PlotVelocity(self.vxdir, "vVec", self.idx("vel1"))
                if self.velocity():               self.vector2_atts = PlotVelocity(self.vxdir, "vVec", self.idx("vel2"))
                if self.spinvec():                self.spinvec_atts = PlotVelocity(self.spinvtk, "spinvec", self.idx("spin"))
                if self.g00():                    self.g00_atts = PlotPseudo(self.g00dir, "g00", self.idx("g00"), self.refPlot)
                #if self.gwaves():                 self.gwaves = PlotGW(self.gwavesdir, "gw", self.idx("gw"))

#############################################

        def SetAtts(self, frame, att_list):
                print("Loading Attibutes")
                view, rho_vol, rho_pseudo, bsq2r, bsq2r_pseudo, bsq2r_iso, vector1, vector2, spinvec, g00_att, seedfile, stream, gw3d_volXML = att_list

                state = self.stateList[frame] - self.stateList[0]
                print("Loading state {}".format(state))
                SetTimeSliderState(frame) #if statelist is [3,4,5], frame=3(h5data) and state=0(xml list).
                tcur = self.timeTXT[state][5:-4]
                print("t/M = {}".format(int(float(tcur))))
                self.txt.text = "t/M = {}".format(int(float(tcur)))
                #self.txt.text = ""

                self.LoadAttr(view, "myView")

                ### adjust the cm focus ###
                self.CoM = getCoM(self.extrasDir + self.timeTXT[state])
#                self.myView.focus = self.CoM
                self.CoM_x, self.CoM_y, self.CoM_z = self.CoM

                if self.density_vol(): print(rho_vol)
                time.strftime("%Y-%m-%d %H:%M:%S")

                if self.density_vol():          self.LoadAttr(rho_vol, "vol")
                if self.density_iso():          LoadAttribute(rho_pseudo, self.rho_atts)
                if self.bsq2r():                        LoadAttribute(bsq2r, self.bsq_atts)
                if self.bsq2r_iso():                    LoadAttribute(bsq2r_pseudo, self.bsq_iso_atts)
                if self.velocity():                     LoadAttribute(vector1, self.vector1_atts)
                if self.velocity():                     LoadAttribute(vector2, self.vector2_atts)
                if self.spinvec():                      LoadAttribute(spinvec, self.spinvec_atts)

                if len(seedfile) > 0 and isfile(seedfile):
                        if len(stream) > 0:
                                LoadAttribute(stream, self.stream_particles_dict["stream_particles_0"])
                        else:
                                print('Using Stream_0.xml for Streamline plot')
                                LoadAttribute(self.StreamDict["Stream_0"],\
                                  self.stream_particles_dict["stream_particles_0"])
                        self.stream_particles_dict["stream_particles_0"].pointList = getSeeds(seedfile)
                elif self.particles():
                        for i in range(self.numBfieldPlots):
                                try: #incase particles start in the middle of a folder
                                        tmp_list = self.StreamDict["Stream_{}".format(i)]
                                        tmp_list1 = self.particlesDict["particle_seeds_{}".format(i)]
                                        streamXML_path = self.extrasDir + tmp_list[tmp_list.index("Stream_{0:04d}_{1}.xml".format(state,i))]
                                        particles_path = self.extrasDir + tmp_list1[tmp_list1.index("particle_seeds_{0:04d}_{1}.txt".format(state,i))]
                                        print("Loading {0} into {1}".format(streamXML_path.split("/")[-1], particles_path.split("/")[-1]))
                                        LoadAttribute(streamXML_path, self.stream_particles_dict["stream_particles_{}".format(i)])
                                        self.stream_particles_dict["stream_particles_{}".format(i)].pointList = getSeeds(particles_path)
                                except:
                                        print("Could not load streamline xml into streamlineattributes, using VisIt default instead")
                                        break

                if self.gridPoints():
                        gridstreamXML_path_0 = self.extrasDir + self.gridStream_0[state]
                        gridstreamXML_path_1 = self.extrasDir + self.gridStream_1[state]
                        LoadAttribute(gridstreamXML_path_0, self.stream_gridPoints_0)
                        LoadAttribute(gridstreamXML_path_1, self.stream_gridPoints_1)
                        self.stream_gridPoints_0.pointList = getSeeds(self.extrasDir+self.gridPointsTXT_0[state])
                        self.stream_gridPoints_1.pointList = getSeeds(self.extrasDir+self.gridPointsTXT_1[state])
                        print("grid point succeed in setatts")
                if self.g00():                          LoadAttribute(g00_att, self.g00_atts)

#############################################

        def PlotFrame(self, frame, forceAddOp=0):
                ######implement loaded plot settings
                print("setting settings")
                if self.density_vol():
                        SetActivePlots(self.idx("density"))
                        SetPlotOptions(self.vol)
                        print("volume set")
                        if self.cutPlot: 
#                            pass
                            #box(self.CoM_y, forceAddOp or frame==self.firstFrame)
                            clip(self.CoM, self.myView.viewNormal, forceAddOp or frame==self.firstFrame)
                if self.density_iso():
                        density_plots = self.idx("density")
                        #density_plots = (self.idx("density"), self.idx("3dbox"))
                        SetActivePlots(density_plots)
                        SetPlotOptions(self.rho_atts)
                        iso(self.rho_isoXML)
                        reflect()
                        print("pseudocolor set")
                        if self.cutPlot: 
                            print("cutplotting")
                            #box(self.CoM_y, forceAddOp or frame==self.firstFrame)
                            clip(self.CoM, self.myView.viewNormal, forceAddOp or frame==self.firstFrame)
                        '''ActivateDatabase ("/anvil/scratch/x-rnarasimhan/abid_bot_gw/box.3d")
                        AddPlot ("Pseudocolor", "box")
                        Pseudobox = PseudocolorAttributes()
                        Pseudobox.colorTableName = "white"
                        SetPlotOptions(Pseudobox)'''
                if self.bsq2r():
                        SetActivePlots(self.idx("bsq2r"))
                        SetPlotOptions(self.bsq_atts)
                        print("bsq2r set")
                        if self.cutPlot: 
                            box(self.CoM_y, forceAddOp or frame==self.firstFrame)
                            #clip(self.CoM, self.myView.viewNormal, forceAddOp or frame==self.firstFrame)
                if self.bsq2r_iso():
                        SetActivePlots(self.idx("bsq2r"))
                        SetPlotOptions(self.bsq_iso_atts)
                        iso(self.bsq2r_isoXML)
                        reflect()
                        print("bsq2r set")
                        if self.cutPlot: 
                            box(self.CoM_y, forceAddOp or frame==self.firstFrame) 
                            #clip(self.CoM, self.myView.viewNormal, forceAddOp or frame==self.firstFrame)
                if self.particles():
                        for i in range(self.numBfieldPlots):
                                SetActivePlots(self.idx("particles{}".format(i)))
                                SetOperatorOptions(self.stream_particles_dict["stream_particles_{}".format(i)])
                                print("streamline %d set" % i)
                if self.gridPoints():
                        SetActivePlots(self.idx("gridPoints_0"))
                        SetOperatorOptions(self.stream_gridPoints_0)
                        SetActivePlots(self.idx("gridPoints_1"))
                        SetOperatorOptions(self.stream_gridPoints_1)
                        print("grid point succeed in plotframe")
                if self.velocity():
                        SetActivePlots(self.idx("vel1"))
                        SetPlotOptions(self.vector1_atts)
                        #boxy(100, forceAddOp or frame==self.firstFrame)
                        #cylinder(self.CoM_x,self.CoM_y, 3, forceAddOp or frame==self.firstFrame, -100, height=100, spinfile=self.spinvtk[:-14]+"{:04d}".format(frame)+".vtk")
                        # cylinder_velocity(forceAddOp or frame==self.firstFrame)
                        # clip_vec(self.CoM_x, self.CoM_y, self.CoM_z, forceAddOp or frame==self.firstFrame)
                        print("velocities 1 set")
                        #if self.cutPlot: box(self.CoM_y, forceAddOp or frame==self.firstFrame)
                if self.velocity():
                        SetActivePlots(self.idx("vel2"))
                        SetPlotOptions(self.vector2_atts)
                        #boxy(100, forceAddOp or frame==self.firstFrame)
                        #cylinder(self.CoM_x,self.CoM_y, 3, forceAddOp or frame==self.firstFrame, -100, height=100, spinfile=self.spinvtk[:-14]+"{:04d}".format(frame)+".vtk")
                        # cylinder_velocity(forceAddOp or frame==self.firstFrame)
                        clip_vec_inverse(self.CoM_x, self.CoM_y, self.CoM_z, forceAddOp or frame==self.firstFrame)
                        print("velocities 2 set")
                        #if self.cutPlot: box(self.CoM_y, forceAddOp or frame==self.firstFrame)

                if self.spinvec():
                        SetActivePlots(self.idx("spin"))
                        SetPlotOptions(self.spinvec_atts)
                        #spherespinvec doesn't center correctly
                        boxspinvec(self.CoM_x,self.CoM_y,self.CoM_z, forceAddOp or frame==self.firstFrame)
                        print("spinvec set")
                        #if self.cutPlot: box(self.CoM_y, forceAddOp or frame==self.firstFrame)
                if self.g00():
                        SetActivePlots(self.idx("g00"))
                        SetPlotOptions(self.g00_atts)
                        iso(self.g00_isoXML)
                        reflect()
                        print("g00 set")


                if self.PlotVelCustom:
                        # print(self.VelCustomFile)
                        OpenDatabase(self.VelCustomFile)
                        AddPlot("Vector", "test")
                        v = VectorAttributes()
                        # print(self.vector1XML)
                        LoadAttribute(self.vector1XML, v)
                        v.stemWidth = 0.01
                        SetPlotOptions(v)
                        # print(v)
                        # print("set plot options!!!!!")
                        reflect()

                        ### stems
                        AddPlot("Vector", "test")
                        v.stemWidth = 0.05
                        v.vectorColor = (1, 50, 32, 255)
                        v.headSize = 0.0
                        SetPlotOptions(v)
                        reflect()
                
                if self.PlotGW2D:
                        if any(filename.startswith("hplus")  for filename in os.listdir(self.extrasDir)):
                                ActivateDatabase(self.hplus)
                        else:
                                ActivateDatabase(self.hcross)
                        wave_zone_r=40
                        #OpenDatabase(self.hplus, 0)
                        #OpenDatabase(self.hcross, 0)
                        #DefineScalarExpression("modifiedwave", "<GW-FIELD>/(exp(-polar_radius(mesh)+10)+1)/(exp(-70 +polar_radius(mesh))+1)")
                        AddPlot("Pseudocolor", "GW-FIELD")
                        Pseudo = PseudocolorAttributes()
                        Pseudo.colorTableName = "gw_plane"
                        Pseudo.minFlag = 1
                        Pseudo.min = -100
                        Pseudo.maxFlag = 1
                        Pseudo.max = 100
                        Pseudo.smoothingLevel = 1 #(0, NONE); (1, Fast); (2, High)
                        Pseudo.legendFlag = 0
                        SetPlotOptions(Pseudo)


                        AddPlot("Mesh", "mesh")
                        m = MeshAttributes()
                        m.foregroundFlag = 0
                        m.legendFlag = 0
                        m.smoothingLevel = m.Fast
                        SetPlotOptions(m)

                        gw2Dplots = (self.idx("gw2D"), self.idx("gw2Dmesh"))
                        SetActivePlots(gw2Dplots)

                        AddOperator("Resample")
                        rAtts = ResampleAttributes()
                        rAtts.is3D = 0
                        rAtts.samplesX = 200
                        rAtts.samplesY = 200
                        SetOperatorOptions(rAtts)

                        AddOperator("Elevate")
                        elevAtts = ElevateAttributes()
                        elevAtts.variable = "GW-FIELD"
                        elevAtts.useXYLimits = elevAtts.Never
                        SetOperatorOptions(elevAtts)

                        AddOperator("Cylinder")
                        CylinderAtts = CylinderAttributes()
                        CylinderAtts.point1 = (0, 0, 10000)
                        CylinderAtts.point2 = (0, 0, -10000)
                        CylinderAtts.radius = wave_zone_r
                        CylinderAtts.inverse = 1
                        SetOperatorOptions(CylinderAtts)

                        c0 = View3DAttributes()
                        c0.viewNormal = (0, 1.2, 1)
                        # c0.viewNormal = (0, 0.5, 1)
                        c0.focus = (15,10,0)
                        # c0.focus = (150, 50, 0)
                        c0.viewUp = (-0.2, -1.2, 1)
                        # c0.viewUp = (-0.25, 0, 1)
                        c0.viewAngle = 30
                        c0.parallelScale = 129.904 #200
                        c0.nearPlane = -698.12
                        c0.farPlane = 698.12
                        c0.imagePan = (0, 0)
                        c0.imageZoom = 0.7 #1.0 #3.2 #2.2
                        c0.perspective = 1
                        c0.eyeAngle = 2
                        c0.centerOfRotationSet = 0
                        c0.centerOfRotation = (7.2533, 7.2533, 0)
                        c0.axis3DScaleFlag = 0
                        c0.axis3DScales = (1, 1, 5000)
                        c0.shear = (0, 0, 1)        

                        self.myView = c0

                        SetActivePlots(self.idx("gw2D"))

                        print("2D gravitational waves set")


                if self.PlotGW3D:
                        '''if any(filename.startswith("hplus")  for filename in os.listdir(self.extrasDir)):
                                ActivateDatabase(self.hplus)
                        else:
                                ActivateDatabase(self.hcross)'''
                        wave_zone_r=5.0
                       
                        #AddPlot("Volume","modifiedwave")


                        '''c0 = View3DAttributes()
                        c0.viewNormal = (0, 0, 1)
                        c0.focus = (0, 0, 0)
                        c0.viewUp = (0, 1, 0)
                        c0.viewAngle = 30
                        c0.parallelScale = 1800.73 #200
                        c0.nearPlane = -3601.45
                        c0.farPlane = 3601.45
                        c0.imagePan = (0, 0)
                        #c0.imagePan = (0, 0.04)
                        c0.imageZoom = 1 #2.2
                        c0.perspective = 1
                        c0.eyeAngle = 2
                        c0.centerOfRotationSet = 0
                        c0.centerOfRotation = (7.2533, 7.2533, 0)
                        c0.axis3DScaleFlag = 0
                        c0.axis3DScales = (1, 1, 1)
                        c0.shear = (0, 0, 1)
                        
                        self.myView = c0'''

                        #vol2 = VolumeAttributes()
                        LoadAttribute(self.gw3D_volXML, self.gw3DvolAtts)
                        SetPlotOptions(self.gw3DvolAtts)                     

                        
                        print("3D gravitational waves set")

                DrawAndSave(self.myView)
                time.strftime("%Y-%m-%d %H:%M:%S")

                xmltxt = '/'.join(self.saveFolder.split('/')[:-1]) + '/xml.txt'
                if(not isfile(xmltxt)):
                        with open(xmltxt,'w') as xt:
                                xt.write("View:\n")
                                xt.write(str(self.myView))
                                if self.density_vol():
                                        xt.write('\n\n\nVol:\n')
                                        xt.write(str(self.vol))

#############################################

        def PlotEvolve(self):
                print('Starting filming')
                time.strftime("%Y-%m-%d %H:%M:%S")
                for frame in range(self.firstFrame, self.lastFrame):
                        state   = self.stateList[frame] - self.stateList[0]
                        viewAtt = self.extrasDir + self.viewXML[state]
                        volAtt  = self.extrasDir + self.volumeXML[state]
                        movie_attributes = [viewAtt, volAtt, self.rho_pseudoXML, self.bsq2rXML, self.bsq2r_pseudoXML, self.bsq2r_isoXML, self.vector1XML, self.vector2XML, self.spinvecXML, self.g00_pseudoXML, self.gw3D_volXML, '','']
                        self.SetAtts(frame, movie_attributes)
                        self.PlotFrame(frame, 1)

#############################################

        def PlotZoom(self, zoomopts):
                frame, zoomsteps, view1, vol1, view2, vol2 = zoomopts
                print("plot zoom test print")
                print(self.rank)
                print(self.total_ranks)
                print(zoomsteps)
                frame_i = int(round((self.rank*1.0)/self.total_ranks*zoomsteps))
                frame_f = int(round((self.rank+1.0)/self.total_ranks*zoomsteps))
                print("frame start: " + str(frame_i) + "\nframe_end: " + str(frame_f))

                view_i = View3DAttributes(); LoadAttribute(view1, view_i)
                view_f = View3DAttributes(); LoadAttribute(view2, view_f)

                vol_i = VolumeAttributes(); LoadAttribute(vol1, vol_i)
                vol_f = VolumeAttributes(); LoadAttribute(vol2, vol_f)

                cpts = (view_i, view_f)
                oi, of, cr = list(map(list,[vol_i.freeformOpacity, vol_f.freeformOpacity, vol_i.freeformOpacity]))

                ai, af, ar = list(map(float,[vol_i.opacityAttenuation, vol_f.opacityAttenuation, vol_i.opacityAttenuation]))

                v = vol_i
                x = [0,1]
                for my_i in range(frame_i, frame_f):
                        t = float(my_i) / float(zoomsteps - 1)
                        c = EvalCubicSpline(t, x, cpts) # Old visit function. You won't find it in the new docs. Go here instead: http://visit.ilight.com/svn/visit/trunk/releases/2.10.0/VisItPythonManual.pdf
                        for i in range(len(oi)):
                                cr[i] = oi[i] + t*(of[i] - oi[i])
                        ar = ai + t*(af - ai)
                        v.freeformOpacity = tuple(cr)
                        v.opacityAttenuation = ar
                        movie_attributes = [c, v, self.rho_pseudoXML, self.bsq2rXML, self.bsq2r_pseudoXML, self.bsq2r_isoXML, self.vector1XML, self.vector2XML, self.spinvecXML, self.g00_pseudoXML, self.gw3D_volXML, '','']
                        self.SetAtts(frame, movie_attributes)
                        self.PlotFrame(frame, forceAddOp=1)

#############################################

        def PlotFlyOver(self, zoomopts):
                frame, num_frames, view_xml, vol_xml = zoomopts
                from math import pi, sin, cos, tan, atan2, sqrt

                print("in floy over")
                def cross(a,b):
                        x=a[1]*b[2]-a[2]*b[1]
                        y=a[2]*b[0]-a[0]*b[2]
                        z=a[0]*b[1]-a[1]*b[0]
                        return (x,y,z)

                def newton(x,f,y):#     adjust initial theta to match new theta not theta0, newtons method on eqn
                        #                               x+f*sin(2x)-y=0
                        for i in range (0,10):
                                x=x-(x+f*sin(2*x)-y)/(1+2*f*cos(2*x))
                        return x

                frame_i = int(round((self.rank*1.0)/self.total_ranks*num_frames))
                frame_f = int(round((self.rank+1.0)/self.total_ranks*num_frames))
                print("frame start: " + str(frame_i) + "\nframe_end: " + str(frame_f))

                myVol = VolumeAttributes(); LoadAttribute(vol_xml, myVol)

                myView = View3DAttributes(); LoadAttribute(view_xml, myView)
                myViewNormal = myView.viewNormal
                myViewUp = myView.viewUp

                for i in range(frame_i, frame_f):
                        factor = 0.4
                        #factor slows down rotation when looking into jet,
                        #                       higher value slows down more.  0<factor<0.5
                        #                       factor=0: spins at constant rate
                        #                       factor=0.5: comes to instantaeneous stop at top & bottom

                        theta = 2*pi*i/(num_frames)#(n-1) makes last frame same as first

                        xhat=myViewNormal[0]
                        yhat=myViewNormal[1]
                        zhat=myViewNormal[2]

                        rhat=sqrt(xhat*xhat+yhat*yhat)
                        theta0=atan2(zhat,rhat)
                        theta0=newton(theta0,factor,theta0)

                        theta_temp=theta0+theta
                        theta_new=theta_temp+factor*sin(2*theta_temp)


                        z_new=sin(theta_new)
                        y_new=cos(theta_new)*(yhat/rhat)
                        x_new=cos(theta_new)*(xhat/rhat)
                        viewNormal = (x_new, y_new, z_new)
                        print("Normal ", viewNormal)
                        perp=cross((xhat,yhat,0),(0,0,zhat))
                        print("perp ", perp)
                        viewUp=cross(perp,viewNormal)
                        print("up: ", viewUp)

                        newView = myView
                        newView.viewNormal = viewNormal
                        newView.viewUp = viewUp

                        movie_attributes = [newView, myVol, self.rho_pseudoXML, self.bsq2rXML, self.bsq2r_pseudoXML, self.bsq2r_isoXML, self.vector1XML, self.vector2XML, self.spinvecXML, self.g00_pseudoXML, self.gw3D_volXML, '','']
                        self.SetAtts(frame, movie_attributes)
                        self.PlotFrame(frame, forceAddOp=1)


#############################################

        def PlotFlyAround(self, zoomopts):
                frame, num_frames, view_xml, vol_xml = zoomopts
                from math import cos, sin, pi, sqrt

                frame_i = int(round((self.rank*1.0)/self.total_ranks*num_frames))
                frame_f = int(round((self.rank+1.0)/self.total_ranks*num_frames))
                print("frame start: " + str(frame_i) + "\nframe_end: " + str(frame_f))

                def vstack(v,u):
                        w=[u[0][1]*v[0][2]-u[0][2]*v[0][1],u[0][2]*v[0][0]-u[0][0]*v[0][2],u[0][0]*v[0][1]-u[0][1]*v[0][0]]
                        return [v[0],w,u[0]]

                def trans(a):
                        b=[[a[i][j] for i in xrange(len(a))] for j in xrange(len(a[0]))]
                        return b

                def mult(a,b):
                        m=[[0 for i in xrange(len(b[0]))] for j in xrange(len(a))]
                        for i in xrange(len(a)):
                                for j in xrange(len(b[0])):
                                        for k in xrange(len(a[0])):
                                                m[i][j]+=a[i][k]*b[k][j]
                        return m


                def circle(vN,vU,theta,M=0,R=0):
                        theta=-theta

                        IE=trans(vstack([list(vN)],[list(vU)]))

                        if (R==0 or R=="Z" or R=="z"):
                                RM=[[cos(theta),-sin(theta),0],[sin(theta),cos(theta),0],[0,0,1]]
                        elif (R==1 or R=="Y" or R=="y"):
                                RM=[[cos(theta),0,sin(theta)],[0,1,0],[-sin(theta),0,cos(theta)]]
                        elif (R==2 or R=="X" or R=="x"):
                                RM=[[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]]
                        else:
                                print("Error! Wrong choice of axis for 'R'!")
                                return vN,vU

                        if (M == 0): # Intrinsic
                                m=trans(mult(RM,IE))
                        elif (M == 1): # extrinsic
                                m=trans(mult(IE,RM))
                        else:
                                print("Error! Wrong choice of mode for 'M'!")
                                return vN,vU

                        return tuple(m[0]),tuple(m[2])

                myVol = VolumeAttributes(); LoadAttribute(vol_xml, myVol)

                myView = View3DAttributes(); LoadAttribute(view_xml, myView)
                myViewNormal = myView.viewNormal
                myViewUp = myView.viewUp

                for i in range(frame_i, frame_f):
                        phi = 2*pi*i/(num_frames)#(n-1) makes last frame same as first
                        viewNormal, viewUp = circle(myViewNormal, myViewUp, phi, 0, 0)

                        newView = myView
                        newView.viewNormal = viewNormal
                        newView.viewUp = viewUp

                        movie_attributes = [newView, myVol, self.rho_pseudoXML, self.bsq2rXML, self.bsq2r_pseudoXML, self.bsq2r_isoXML, self.vector1XML, self.vector2XML, self.spinvecXML, self.g00_pseudoXML, self.gw3D_volXML, '','']
                        self.SetAtts(frame, movie_attributes)
                        self.PlotFrame(frame, forceAddOp=1)
###################END#######################
