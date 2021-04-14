import math
import numpy
from scipy import integrate
f=open('1dstar.txt',"r")

def Remove(duplicate): 
	final_list = [[], []] 
	for i in range(len(duplicate[0])): 
		if duplicate[0][i] not in final_list[0]: 
			final_list[0].append(duplicate[0][i])
			final_list[1].append(duplicate[1][i])
	return final_list 
def bubbleSort(arr):
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
lines=f.readlines()
result= [[], []]
for x in lines:
	result[0].append(x.split(' ')[1])
	result[1].append(x.split(' ')[2])
data = [[], []]
for x in range(len(result[0])):
	if float(result[0][x]) >= 0:# and float(result[0][x]) <=.87: #and float(result[0][x]) <=1.5:
		data[0].append(float(result[0][x]))
		data[1].append(float(result[1][x]))
#print(len(data[0]))
#print(len(data[1]))
data = Remove(data)
#print(len(data[0]))
#print(len(data[1]))
bubbleSort(data)
#print(len(data[0]))
#print(data[0])
#print("\n")
#print(data[1])
#for i in range(len(data[1])):
#	if numpy.isclose(data[1][i],0.0007862454):
#		print(data[0][i])
goodVolIntegrate(data)

f.close()
