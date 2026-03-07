"""
script for reading all components of g00 and writing to new h5 files"
written by: Kyle Nelli
edited by: Dr. Roland Haas, NCSA
updated: 4/17/19

run as: python3 make_g00.py directory_string
"""

import h5py as h5
import numpy as np
from glob import glob
from sys import argv

dir_str = argv[1]
g00_components = ["gxx", "gyy", "gzz", "gxy", "gxz", "gyz", "shiftx", "shifty", "shiftz", "lapm1", "psi"]
g00_str = "BSSN::g00"

#calculate g00 from a master array dictionary (mad) of the form {"comp_name": 4d numpy array with time being the first axis}
def Calc_g00(mad):
	g00 = mad["psi"]**4 * (mad["gxx"]*mad["shiftx"]**2 + mad["gyy"]*mad["shifty"]**2 + mad["gzz"]*mad["shiftz"]**2 + 2*(mad["gxy"]*mad["shiftx"]*mad["shifty"] + mad["gxz"]*mad["shiftx"]*mad["shiftz"] + mad["gyz"]*mad["shifty"]*mad["shiftz"] ) ) - (mad["lapm1"] + 1 )**2

	return g00

print("starting...")
for folder in dir_str.split("+")[1:]:
	folder = folder if folder[-1]=="/" else folder + "/"
	print("Making g00 files for {}".format(folder))
	num_files = len(glob(folder + g00_components[0] + ".file_*.h5"))
	for i in range(0,num_files):
		#progess update
		#if i % 10 == 0:
			#print("Creating files {}-{}".format(i,i+9) if i+9<num_files else "Creating files {}-{}".format(i,num_files-1))
	
		master_file_dict = {}
		outfile = h5.File(folder + "g00.file_{}.h5".format(i), "w")
	
		#loop over all components of g00
		#add the whole file to a dictionary with the key as the component
		for component in g00_components:
			infile = h5.File(folder + "{}.file_{}.h5".format(component,i), "r")
			master_file_dict[component] = infile
	
		master_array_dict = {}
		param_list = []
		#loop over all components again to add all array data to a dictionary
		for component in g00_components:
			temp_list = []
			temp_keys = list(master_file_dict[component].keys()) #list of keys to access all data
			for key in temp_keys:
				dataset = master_file_dict[component][key] #the actual data

				#copy all datasets from one component for reference on shape and dtype
				if component=="gxx":
					param_list.append(dataset)
			
				#this group doesn't have any data so don't add it to the array dictionary
				if dataset.name=="/Parameters and Global Attributes":
					continue
			
				#add numpy array of data to temp list
				temp_list.append(np.array(dataset, dtype='<f8'))
		
			#add temp list to dictionary
			master_array_dict[component] = np.array(temp_list)
	
		#calcualte g00
		g00 = Calc_g00(master_array_dict)
		#gxx = Recalc_gxx(master_array_dict) #testing
	
		#sort param list by the name of its members
		param_list.sort(key= lambda x: x.name)
		for j,param in enumerate(param_list):
			#write all data that isn't the group Parameters and Global Atts to new file
			if param.name!="/Parameters and Global Attributes":
				#get name of random dataset which includes the it, tl, rl, c
				#but get rid of the actual name
				split_name = param.name.split()[1:]
			
				#make new name with g00 but including corresponding it, tl, rl, c
				name = " ".join(split_name)
				dset = outfile.create_dataset(g00_str + " " + name, data=g00[j], dtype=param.dtype)
		                # RH: add required attributes
			
				for attr in param.attrs:
					dset.attrs[attr] = param.attrs[attr]
			
				dset.attrs['name'] = g00_str
			else:
				#create the parameters group with corrected field 'Datasets'
				ga = outfile.create_group("Parameters and Global Attributes")
				ga_keys = list(param.keys())
				for key in ga_keys:
					if key != "Datasets":
						ga.create_dataset(param[key].name, data=param[key])
					else:
						#turn the name of the new files to ascii characters
						#including the ::g00
						#the [10, 0] is necessary (don't really know why)
						temp_data = [ord(mystr) for mystr in g00_str] + [10, 0]
						ga.create_dataset(param[key].name, data=temp_data)
			
				ga.attrs.create("nioprocs", num_files, dtype='int32')

		outfile.close()
print("done :)")
