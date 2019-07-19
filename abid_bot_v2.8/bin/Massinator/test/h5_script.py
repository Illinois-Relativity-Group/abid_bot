import math
import numpy as np
from scipy import integrate
f=open('2dstar.txt',"r")

def Remove(duplicate): 
	final_list = [[], []] 
	for i in range(len(duplicate[0])): 
		if duplicate[0][i] not in final_list[0]: 
			final_list[0].append(duplicate[0][i])
			final_list[1].append(duplicate[1][i])
			#final_list[1].append(duplicate[1][i])
	return final_list 
def bubbleSort1(arr):
	n = len(arr[0])
 
    # Traverse through all array elements
	for i in range(n):
 
        # Last i elements are already in place
		for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
			if arr[0][j] > arr[0][j+1] :
				arr[0][j], arr[0][j+1] = arr[0][j+1], arr[0][j]
				arr[1][j], arr[1][j+1] = arr[1][j+1], arr[1][j]
def bubbleSort2(arr):
	n = len(arr)
 
    # Traverse through all array elements
	for i in range(n):
 
        # Last i elements are already in place
		for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
			if arr[j] > arr[j+1] :
				arr[j], arr[j+1] = arr[j+1], arr[j]
				arr[j], arr[j+1] = arr[j+1], arr[j]
def badVolIntegrate(arr):
	n = len(arr[0])
	result = 0
	previous_radius= arr[0][0]
	previous_rho=arr[1][0]
	for i in range(1, n):
		result += previous_rho * ((4.0/3)*math.pi)*(arr[0][i]**3 - previous_radius**3)
		previous_radius = arr[0][i]
		previous_rho = arr[1][i]
	print('Mass: ' + str(result))
def goodVolIntegrate(arr):	
	n = len(arr[0])
	result = 0
	areadens=[]
	for i in range(0,len(arr[1])):
		areadens.append(arr[1][i]*4*math.pi*arr[0][i]**2)
	result=integrate.simps(areadens,arr[0])
	print('Mass: ' + str(result))
def goodVolIntegrate2d(dicto,listo):
	discs=[]
	newlisto=[]
	#do one integration for each z value to find mass concentrated at that z
	for z in listo:
		#print(z)
		newlisto.append(float(z))
		xs=[]
		ringdens=[]
		for pt in dicto[z]:
			xs.append(float(pt[0]))
			ringdens.append(float(pt[1])*float(pt[0])*2*math.pi)
		try:
			discdens=integrate.simps(ringdens,xs)
		except:
			print(len(ringdens),len(xs),z)
			exit()
		discs.append(discdens)
	#integrate across all z values
	result=integrate.simps(discs,newlisto)
	print('Mass: ' + str(result))
		
lines=f.readlines()
#zdict maps each z value to a list of tuples of the form (x, rho)
zdict={}
#list of all z values. needed for integration later.
zlist=[]
for x in lines:
	vals=x.split(' ')
	if abs(float(vals[2]))<=.87: 
		if vals[2] not in zdict:
			zdict[vals[2]]=[]
		zdict[vals[2]].append((vals[1],vals[3]))
		if vals[2] not in zlist:
			zlist.append(vals[2])
		#result[2].append(x.split(' ')[3])
#this loop removes duplicate data and sorts the list at each z. later integration assumes the density is ordered by x
for z in zdict:
	data = [[], []]
	for x in range(len(zdict[z])):
		#print(float(z))
		if float(zdict[z][x][0]) >= 0 and (float(zdict[z][x][0])**2+float(z)**2) <=(.87)**2:
			#print("yes")
			data[0].append(float(zdict[z][x][0]))
			data[1].append(float(zdict[z][x][1]))
			#data[2].append(float(result[2][x]))
	data = Remove(data)
	bubbleSort1(data)
	zdict[z]=[]
	for i in range (len(data[0])):
		zdict[z].append((data[0][i],data[1][i]))
#print(len(data[0]))
#print(len(data[1]))
#print(len(data[0]))
#print(len(data[1]))
zlist2=sorted(zlist, key=float)
#print(len(data[0]))
#print(data[0])
#print(data[1])

goodVolIntegrate2d(zdict,zlist2)

f.close()
