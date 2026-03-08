# code to plot the punctures

import numpy as np
import matplotlib
from matplotlib import rc
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from os import makedirs
import os
from scipy.interpolate import CubicSpline

scratch = "/data/jbamber/" 
home = os.environ["HOME"] + "/"

psi_hlm_path = "/data/codyolson/psi4_analysis_code/psi4_hlm_Monoenergetic_N25_yc0.819_ID2_chi0.7_spacial_sigma"
sim_name =  "Monoenergetic_N25_yc0.605_ID2_chi0.7_aligned" #"Monoenergetic_N25_yc0.819_ID2_chi0.7_aligned_restart_20_v12" #"Monoenergetic_N25_yc0.819_ID2_chi0.7_spacial_sigma" 

num_modes = 77
M_ADM = 11.16186509 #11.70455003 #11.5598573559999 #11.527308443 #11.5598573559999 

#r_list = [300.0, 420.0, 600.0, 1200.0, 1600.0, 1800.0] #,400.0]
#r_columns = [5,0,1,2,3,4]

r_list = [300.0, 420.0, 600.0, 1200.0, 1600.0, 1800.0] #,400.0]
r_columns = [0,1,2,3,4,5]

def smart_genfromtxt(file_path):
  data = []
  with open(file_path,"r") as f:
    for line in f:
      li=line.strip()
      if not li.startswith("#"):
        data_line = line.split()[:13]
        if (len(data_line)>0):
          if (len(data_line)<(2*len(r_list)+1)):
            #print("data line = ",data_line)
            data_line = data_line + ["0.00","0.00"]
          #print("data_line.shape = ",len(data_line))
          data.append(np.array(data_line,dtype=float))
  out_data = np.array(data)
  #.astype(np.float)
  return out_data


def save_IllinoisGRMHD_like_data(sim_name):
  # load first mode
  try:
    makedirs(psi_hlm_path + "/" + sim_name)
  except:
    pass
  data = smart_genfromtxt(scratch + sim_name + "/data/Weyl4_mode_22.dat")
  t = data[:,0]
  N_rows = len(t)
  #
  out_data_list = []
  for ir in range(0,len(r_list)):
    out_data_list.append(np.zeros((N_rows,2*num_modes+2+3)))
  for ir in range(0,len(r_list)):
    out_data_list[ir][:,0] = t
  #
  nmode = 0
  headers = "  Time                "
  for l in [2,3,4,5,6,7,8]:
    for im in range(0,2*l+1):
      m = l - im
      headers += "Re(psi4_{:d}{:d})".format(l,m).ljust(20)
      headers += "Im(psi4_{:d}{:d})".format(l,m).ljust(20)
      raw_data = smart_genfromtxt(scratch + sim_name + "/data/Weyl4_mode_{:d}{:d}.dat".format(l,m))[:N_rows,:]
      data = np.zeros((N_rows,1+len(r_list)*2))
      start_index = np.argmin(np.abs(t - raw_data[0,0]))
      data[start_index:,:] = raw_data[:(N_rows-start_index),:]
      for ir in range(0,len(r_list)):
        column = 1 + r_columns[ir]*2
        r = r_list[ir]
        Psi_Re = data[:,column]
        Psi_Im = data[:,column+1]
        out_data_list[ir][:,1+2*nmode] = Psi_Re/r
        out_data_list[ir][:,1+2*nmode+1] = Psi_Im/r
      nmode += 1
  headers += "r_areal".ljust(20)
  headers += "Fake g^tt".ljust(20)
  headers += "Fake g^tr".ljust(20)
  headers += "Fake g^rr".ljust(20)
  for ir in range(0,len(r_list)):
    out_data_list[ir][:,1+2*77] = r_list[ir]
    out_data_list[ir][:,1+2*77+1] = -1.0/(1 - 2*M_ADM/r_list[ir])
    out_data_list[ir][:,1+2*77+2] = 0.0
    out_data_list[ir][:,1+2*77+3] = (1 - 2*M_ADM/r_list[ir])
    #out_name = psi_hlm_path + "/" + sim_name + "/Psi4_rad.mon.{:d}".format(ir+1)
    out_name = scratch + sim_name + "/data/" + "Psi4_rad.mon.{:d}".format(ir+1)
    np.savetxt(out_name,out_data_list[ir],fmt="%20.10e",delimiter="",header=headers)
    out_name = psi_hlm_path + "/" + sim_name + "/Psi4_rad.mon.{:d}".format(ir+1)
    np.savetxt(out_name,out_data_list[ir],fmt="%20.10e",delimiter="",header=headers)
    print("saved ", out_name)
  #


save_IllinoisGRMHD_like_data(sim_name)