from os import listdir
from sys import argv
ct=0
for fil in listdir('vel_data_iter2'):
	ct+=1
	if(ct%50==0):
		print(ct)
	with open('vel_data_iter2/'+fil,'r') as data_t:
		checkset=set([i for i in data_t])
		with open('vel_data_iter_clean2/'+fil,'w') as outfile:
			for line in checkset:
				outfile.write(line)
