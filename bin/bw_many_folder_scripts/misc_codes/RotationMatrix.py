################################ README #####################################
# Writen by Lingyi Kong
# Last Update: June 16, 2015
# This module is used to handled various camera rotation in visit.
# It also comes with a few linear algebra function, which can be useful for expansion
# To import this module, run the following:
"""
import sys
sys.path.append("/PATH_TO_DIR_OF_THIS_MODULE")
import RotationMatrix as RM
"""
# You could also run this python script directly in visit
# to see what this module can do
# TODO execfile("/PATH_TO_SCRIPT/RotationMatrix.py")

############################## From Lingyi ##################################
# Matrices are probably the easest way to handle camera rotation stuff
# Since visit doesn't have native support for numpy
# and importing numpy in visit is quite a nuisance
# I decided to write my own linear algebra functions in this module
# Due to my limited knowledge and understanding about linear algebra
# This module currently only handles some basic rotations
# However, people might be able to make more sophisticated camera functions
# using the functions provided in this module
# most of the functions in this module work on matrix-form (2D) list
#	hence if you have a tuple (x,y,z), you need to do [list((x,y,z))]
#	to be able to pass it to the function
#############################################################################


from math import cos,sin,pi,sqrt

# Deep copy function
# Simple assignment "=" in python only assigns the address
# This function will create independt memory for new variable
def copy(a):
        b=[]
        if (type(a) == list):
                for i in xrange(len(a)):
                        b.append(copy(a[i]))
                return b
        else:
                return a


# Stacking 1*3 vectors to make a 3*3 matrix
# This function takes viewNormal (x-axis) and viewUp(z-axis) vectors
# using cross product (follows right-hand-rule) to calculate the third vector (y-axis)
# and then stack them by rows, ie [[x0,x1,x2],[y0,y1,y2],[z0,z1,z2]]
# viewNormal and viewUp are tuples in visit, use [list(viewNormal)]
#	to make it a 2D list
def vstack(v,u):
	w=[u[0][1]*v[0][2]-u[0][2]*v[0][1],u[0][2]*v[0][0]-u[0][0]*v[0][2],u[0][0]*v[0][1]-u[0][1]*v[0][0]]
	return [v[0],w,u[0]]


# Calculate the transpose of a matrix
def trans(a):
	b=[[a[i][j] for i in xrange(len(a))] for j in xrange(len(a[0]))]
	return b


# Finding the magnitude of a vector
# It is also the p=2 entrywise norm of a matrix
def mag(x):
	mag=0
	for i in xrange(len(x)):
		for j in xrange(len(x[0])):
			mag+=x[i][j]**2
	return sqrt(mag)


# multiply a matrix "a" by a scaler "x". xA
def scale(a,x):
	m=[[(a[j][i])*x for i in xrange(len(a[0]))] for j in xrange(len(a))]
	return m


# entry-wise substraction of matrices a-b
def sub(a,b):
	x=[[a[j][i]-b[j][i] for i in xrange(len(a[0]))] for j in xrange(len(a))]
	return x
			

# Matrix multiplication AB
def mult(a,b):
	m=[[0 for i in xrange(len(b[0]))] for j in xrange(len(a))]
	for i in xrange(len(a)):
		for j in xrange(len(b[0])):
			for k in xrange(len(a[0])):
				m[i][j]+=a[i][k]*b[k][j]
	return m

# single column pivoting operation in Gaussian elimination for solving linear equations
# see https://en.wikipedia.org/wiki/Gaussian_elimination
# To reduce rounding error, it will swap target row with subsequent rows
#	such that the corresponding diagonal entry is largest in magnitude
# see http://heath.cs.illinois.edu/scicomp/notes/chap02.pdf (page 53)
# The linear equation is Ax=B, solve for x
def pivot(a0,b0,row):
	a=copy(a0)
	b=copy(b0)
	index = row
	for i in xrange(row+1,len(a0)):
		if (abs(a[i][row]) > abs(a[index][row])):
			index = i
	a[index],a[row]=a[row],a[index]
	b[index],b[row]=b[row],b[index]
	
	return a,b


# Gaussian elimination method of solving linear equation Ax=B for x
# See http://heath.cs.illinois.edu/scicomp/notes/chap02.pdf (page 29)
# and https://en.wikipedia.org/wiki/Gaussian_elimination
def gauss(a0,b0):
	a=copy(a0)
	b=copy(b0)
	for i in xrange(len(a)):
		a,b=pivot(a,b,i)
		m=[[0 for I in xrange(len(a))] for J in xrange(len(a))]
		for I in xrange(len(a)):
			m[I][I]=1
		for j in xrange(i+1,len(a)):
			m[j][i]=-1.0*a[j][i]/a[i][i]
		a=mult(m,a)
		b=mult(m,b)
	return a,b
			

# Solving linear equation Ax=B for x, x will be returned as matrix
def solve(a0,b0):
	a,b=gauss(a0,b0)
	x=[[0 for i in xrange(len(b[0]))] for j in xrange(len(b))]
	for i in xrange(len(b[0])):
		for j in xrange(len(b)-1,-1,-1):
			x[j][i]=b[j][i]
			tmp=0
			for k in xrange(len(b)-1,j,-1):
				tmp+=a[j][k]*x[k][i]
			x[j][i]=1.0*(x[j][i]-tmp)/a[j][j]
	return x


# Finding change of coordinate transformation matrix between intrinsic (A) and extrinsic coordinates (B)
# It returns both the forward transformation (IE) as well as its inverse (EI)
# This function turned out to be unnecessary if A is identity matrix
# (Because in that case, TM and inv(TM) is simply B or trans(B))
# However, I'm keeping the function here in case it might be useful for future usage
#
# !!!!!	Due to the method I'm using in solving linear equation Ax=B
#	The transformation matrix x is a post-multiplying matrix
#	where tradinational rotation matrices are pre-multiplying matrices
#	This causes vectors in A are row vectors while in B are column vectors
#	hence if A is identity matrix, EI and IE are the same
def TM(vN,vU):
	a=[[1,0,0],[0,1,0],[0,0,1]]
	vNm=[list(vN)]
	vUm=[list(vU)]
	vN0=scale(vNm,1.0/mag(vNm))
	vU1=sub(vUm,scale(vN0,mult(vUm,trans(vN0))[0][0]))
	vU0=scale(vU1,1.0/mag(vU1))
	b=trans(vstack(vN0,vU0))
	IE=solve(a,b)
	EI=solve(trans(b),trans(a))
	return IE,EI


############################## Camera Functions ##############################

# Basic circular rotation about x,y,z axes
# Have the choice of either intrinsic or extrinsic axis
# Direction of rotation is determined by RHD (along the positive rotating axis)
# M=0 for intrinsic rotation (about the object's own axes)
# M=1 for extrinsic rotation (about viewer's axes)

def circle(vN,vU,theta,M=0,R=0):
	theta=-theta
# a minus for theta is needed becuase this is passive rotation
# See https://en.wikipedia.org/wiki/Active_and_passive_transformation

	#IE,EI=TM(vN,vU)	
	IE=trans(vstack([list(vN)],[list(vU)]))

# R=0,1,2 for rotating axes z,y,x
# I'm using the traditional pre-multiplying matrix for RM here

	if (R==0 or R=="Z" or R=="z"):
		RM=[[cos(theta),-sin(theta),0],[sin(theta),cos(theta),0],[0,0,1]]
	elif (R==1 or R=="Y" or R=="y"):
		RM=[[cos(theta),0,sin(theta)],[0,1,0],[-sin(theta),0,cos(theta)]]
	elif (R==2 or R=="X" or R=="x"):
		RM=[[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]]
	else:
		print("Error! Wrong choice of axis for 'R'!")
		return vN,vU

# I'm not very good at LA, so I can only try to explain what's happening below
# Please feel free to change the text here if you understand it better than me

	if (M == 0): # Intrinsic
		m=trans(mult(RM,IE))
# The full pseudo expression is (xe,ye,ze)=RM(xi,yi,zi)*IE
# since (xi,yi,zi)=identity, it's simply RM*IE
# In short, it rotates the object in its own coordinate and figure out
#	what the view is
# trans(m) simply makes m row-base again



	elif (M == 1): # extrinsic
		m=trans(mult(IE,RM))
# The full pseudo expression is (EI*RM)*(xe,ye,ze)
# I should use the pre-multiplying EI here, but in our construction
# pre-multiplying EI = IE, also (xe,ye,ze)=identity, so IE*RM
# This one simply rotates the view
# You will see when rotating about z, viewUp remains unchanged
#	when about x, viewNormal remains unchanged


	else:
		print("Error! Wrong choice of mode for 'M'!")
		return vN,vU
	return tuple(m[0]),tuple(m[2])	# return x,z for viewNumal and viewUp



############################ Code for example ########################
# The code below is not part of the module
# Instead they'll be run when you run this script directly in visit
# Add examples here if you made new functions
######################################################################
if __name__ == "__main__":
	from time import sleep
	import os
	from random import random
	
	# Create test sample data
	ExPath=os.path.expanduser("~")
	ExSample=ExPath+"/RotationMatrix_test.3d"
	f=open(ExSample,'w')
	f.write("x\ty\tz\tpts\n")
	pts=0
	for i in xrange(50):
		for j in xrange(10):
			for k in xrange(11):
				z=k/3.0
				r=sqrt(100-k**2)
				x=10+sqrt(r)*cos(2*pi/50*i)*j/9
				y=10+sqrt(r)*sin(2*pi/50*i)*j/9
				s=str(x)+"\t"+str(y)+"\t"+str(z)+"\t"+str(pts)+"\n"
				pts+=1
				f.write(s)
	for l in xrange(150):
		s=str(10)+"\t"+str(10.0)+"\t"+str(l/20.0)+"\t"+str(pts)+"\n"
		f.write(s)
	f.close()
	print("Done creation")
	# Visit Command
	OpenDatabase(ExSample)
	AddPlot("Pseudocolor","pts")
	DrawPlots()
	v=GetView3D()
	v.viewNormal=(random(),random(),random())
	v.viewUp=(random(),random(),random())
	print("Randomize a view angle")
	sleep(0.5)
	SetView3D(v)
	sleep(1)
	m=("0(intrinsic)","1(extrinsic)")
	r=("z","y","x")
	for i in xrange(2):
		for j in xrange(3):
			sleep(1)
			print("RM.circle(viewNormal,viewUp,theta,M=%s,R=%s)" % (m[i],r[j]))
			sleep(3)
			v=GetView3D()
			vn=v.viewNormal
        		vu=v.viewUp
			for k in xrange(50):
				theta=pi*k/5
				v.viewNormal,v.viewUp=circle(vn,vu,theta,i,j)
				sleep(0.2)
				SetView3D(v)
