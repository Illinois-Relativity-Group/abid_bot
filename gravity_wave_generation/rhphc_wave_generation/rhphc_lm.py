###########################################################################################
#                                                                                         #
# Script to plot central and max density over time.                                       #
# Author: Antonios Tsokaros October 13 2016.                                              #
#                                                                                         #
###########################################################################################

import math
import numpy as np
from matplotlib import rc
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, ScalarFormatter, FormatStrFormatter
from scipy.interpolate import interp1d
from scipy import interpolate
import sys

# Default properties:
rc('text', usetex=True)
rc('font', family='serif')
#rc('font', serif='palatino')
#rc('font', weight='bolder')
rc('mathtext', default='sf')
rc("lines", markeredgewidth=2)
rc("lines", linewidth=3)
rc('axes', labelsize=30)
rc("axes", linewidth=2)
rc('xtick', labelsize=28)
rc('ytick', labelsize=28)
rc('legend', fontsize=20)
rc('xtick.major', pad=8)
rc('ytick.major', pad=8)
rc('xtick.major', size=13)
rc('ytick.major', size=13)
rc('xtick.minor', size=7)
rc('ytick.minor', size=7)
# Some colors:
green1='#00ff00'
dgreen='#006400'  # Dark green
orange='#ffba00'
dorange='#ff8c00' # Dark orange
sorange='#ff6700' # Safety orange
dbrown='#654321'  # Dark brown
sbrown='#8b4513'  # Saddle brown
lbrown='#b5651d'  # Light brown 
mpurple='#9370db' # Medium purple 
rpurple='#7851a9' # Royal purple
#============================================================================

# COCAL values
Madm_vol = 1.770505844009962E+00
Madm_sur = 1.770817020849460E+00
M0       = 2.012313787861947E+00
J_vol    = 2.669475708398540E+00
J_sur    = 2.668545059235427E+00
rhoc     = 1.564676771905078E-03
MoR      = 2.500000000000000E-01

# Value from Psi4_rad.mon.* column 44
r_extr   = 1.4177658634E+002

# Note that the code computes r*h so we normalize by M and *1000.
oom = 1000.0/Madm_sur
xoffset = 0.7*r_extr

print "COCAL: Madm_vol, Madm_sur, M0 :", Madm_vol, Madm_sur, M0
print "COCAL: Jadm_vol, Jadm_sur,    :", J_vol, J_sur
print "COCAL: rhoc, M/R              :", rhoc, MoR 
print "====================================================================="
print "Dynamical time scale t_d/M ~ (M/R)^(-3/2)   :", MoR**(-1.5)
print "Secular time scale of GW t_s/M ~ (M/R)^(-4) :", MoR**(-4)
print "====================================================================="
print "GW extraction radius :", r_extr
print "====================================================================="

#============================================================================
data_t=[]; data_hp=[]; data_hc=[]

# Some global variables:
labelsize = 30
rc('xtick', labelsize=30)
rc('ytick', labelsize=30)

if ( len(sys.argv) == 3 ):
  l = int(sys.argv[1])
  m = int(sys.argv[2])
else :
  print "Usage: python Psi4_all.py  l m"
  print "Usage: 2 <= l <= 4 and -l <= m <= l"
  exit()

if(l==2):
  if  (m== 2):  colhp=1 ;  colhc=2 ; 
  elif(m== 1):  colhp=3 ;  colhc=4 ;
  elif(m== 0):  colhp=5 ;  colhc=6 ;
  elif(m==-1):  colhp=7 ;  colhc=8 ;
  elif(m==-2):  colhp=9 ;  colhc=10;
  else:
    print "Wrong choice of m"
elif(l==3):
  if  (m== 3):  colhp=11;  colhc=12;
  elif(m== 2):  colhp=13;  colhc=14;
  elif(m== 1):  colhp=15;  colhc=16;
  elif(m== 0):  colhp=17;  colhc=18;
  elif(m==-1):  colhp=19;  colhc=20;
  elif(m==-2):  colhp=21;  colhc=22;
  elif(m==-3):  colhp=23;  colhc=24;
  else:
    print "Wrong choice of m"
elif(l==4):
  if  (m== 4):  colhp=25;  colhc=26;
  elif(m== 3):  colhp=27;  colhc=28;
  elif(m== 2):  colhp=29;  colhc=30;
  elif(m== 1):  colhp=31;  colhc=32;
  elif(m== 0):  colhp=33;  colhc=34;
  elif(m==-1):  colhp=35;  colhc=36;
  elif(m==-2):  colhp=37;  colhc=38;
  elif(m==-3):  colhp=39;  colhc=40;
  elif(m==-4):  colhp=41;  colhc=42;
  else:
    print "Wrong choice of m"
else:
  print "l,m=",l,",",m
  print "Must choose 2 <= l <= 4 and -l <= m <= l ...exiting"
  exit()
print "Mode (l,m)=(",l,",",m,")"

data = np.loadtxt("rhphc.dat")

# Possibly not unique
data_t1 = data[:,0]           # retarded time
data_hp1 = data[:,colhp]
data_hc1 = data[:,colhc]

print "Length of lists: ", len(data_t1), " === ", len(data_hp1)
#for i in range(0,len(data_t1)): 
#  print '%15d%15.5e' % (data_t1[i], data_rhoc1[i])

# Make lists unique
j=0
for i in range(0,len(data_t1)): 
  if data_t1[i] not in data_t :
    data_t.append(data_t1[i])
    data_hp.append(data_hp1[i])
    data_hc.append(data_hc1[i])
    j = j + 1
print "Length of unique lists: ", len(data_t), " === ", len(data_hp)

hp_max = max(data_hp)
hp_min = min(data_hp)
hc_max = max(data_hc)
hc_min = min(data_hc)

hpm = oom*max(abs(hp_max), abs(hp_min))
hcm = oom*max(abs(hc_max), abs(hc_min))

# Create a figure instance:
fig = plt.figure(figsize=(16.0,12.0))
#fig.subplots_adjust(left=0.14)
#fig.subplots_adjust(bottom=0.10)
fig.subplots_adjust(top=0.9)
#fig.subplots_adjust(right=0.97)
fig.subplots_adjust(hspace=0.1)
fig.subplots_adjust(wspace=0.1)


# Create an axes instance:
ax1 = fig.add_subplot(2,1,1) # # of rows, # of columns, plot # running by row.
ax12= ax1.twiny()

hp_line, = ax1.plot(data_t, [i*oom for i in data_hp], linestyle='-', color='red')

# Plot legend:
mylegend = ax1.legend((hp_line,),\
                     ("$l=$"+str(l)+", "+"$m=$"+str(m),),\
                     loc=(0.7,0.85),\
                     borderaxespad=0.02,\
                     labelspacing=0.01,\
                     markerscale=0,\
                     handlelength=2  )

# Modify legend
mylegend.draw_frame(True)
mylegendtext = mylegend.get_texts()
mylegendlines = mylegend.get_lines()
plt.setp(mylegendtext, fontsize=30)
plt.setp(mylegendlines, linewidth=3)

# Plot properties:
xa=0.0;                  xb=500;                      dx=(xb-xa)/10.
xa=data_t[0] + xoffset;  xb=data_t[len(data_t)-1];    dx=(xb-xa)/10.
ya=-1.1*hpm;   yb=1.1*hpm;   dy=(yb-ya)/10.
print "xa=", xa, "   xb=", xb, "   length of time:", len(data_t)

xlim = (xa,xb)
ylim = (ya,yb)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.xaxis.set_minor_locator(mticker.MultipleLocator(dx/2.0))
ax1.xaxis.set_major_locator(mticker.MultipleLocator(dx))
y_formatter = mticker.ScalarFormatter(useOffset=True)
ax1.yaxis.set_major_formatter(y_formatter)
ax1.set_xticklabels([])
ax1.grid(color='black', linestyle=':', linewidth=0.5)
ax1.set_ylabel(r'$(r/M) h_{+}\ \ (\times 10^{-3})$', fontsize=labelsize)

#ax1Ticks = ax1.get_xticks()   
#ax12Ticks = ax1Ticks[1:]
#ax12.xaxis.set_minor_locator(mticker.MultipleLocator(dx/2.0))

#def tick_function(X):
#    V = X/Madm_sur
#    return ["%.1f" % z for z in V]

#ax12.set_xticks(ax12Ticks)
#ax12.set_xbound(ax1.get_xbound())
#ax12.set_xticklabels(tick_function(ax12Ticks), fontsize=24, family='serif', usetex=False)

xa12 = xa/Madm_sur;    xb12=xb/Madm_sur;   dx12=(xb12-xa12)/10.
x12lim = (xa12, xb12)
ax12.set_xlim(x12lim)
ax12.xaxis.set_minor_locator(mticker.MultipleLocator(dx12/2.0))
ax12.xaxis.set_major_locator(mticker.MultipleLocator(dx12))
ax12.xaxis.labelpad = 20
ax12.set_xlabel(r'$t_{\rm ret} [M]$', fontsize=labelsize)
#ax12.set_xlabel(r'$t-r_{\star} [M]$', fontsize=labelsize)
#plt.text(0.25,0.67,r'COCAL: $|H|_2$',fontsize=labelsize,transform=fig.transFigure)



# Create an axes instance:
ax2 = fig.add_subplot(2,1,2) # # of rows, # of columns, plot # running by row.
ax22= ax2.twiny()

hc_line, = ax2.plot(data_t, [i*oom for i in data_hc], linestyle='-', color='blue')

# Plot legend:
mylegend = ax2.legend((hc_line,),\
                     ("$l=$"+str(l)+", "+"$m=$"+str(m),),\
                     loc=(0.7,0.85),\
                     borderaxespad=0.02,\
                     labelspacing=0.01,\
                     markerscale=0,\
                     handlelength=2  )

# Modify legend
mylegend.draw_frame(True)
mylegendtext = mylegend.get_texts()
mylegendlines = mylegend.get_lines()
plt.setp(mylegendtext, fontsize=30)
plt.setp(mylegendlines, linewidth=3)

# Plot properties:
xa=0.0;                  xb=500;                      dx=(xb-xa)/10.
xa=data_t[0] + xoffset;  xb=data_t[len(data_t)-1];    dx=(xb-xa)/10.
ya=-1.1*hcm;   yb=1.1*hcm;   dy=(yb-ya)/10.
print "xa=", xa, "   xb=", xb

xlim = (xa,xb)
ylim = (ya,yb)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2.xaxis.set_minor_locator(mticker.MultipleLocator(dx/2.0))
ax2.xaxis.set_major_locator(mticker.MultipleLocator(dx))
y_formatter = mticker.ScalarFormatter(useOffset=False)
ax2.yaxis.set_major_formatter(y_formatter)
ax2.grid(color='black', linestyle=':', linewidth=0.5)
ax2.xaxis.labelpad = 20
#ax2.set_xlabel(r'$t-r_{\star} [M_{\odot}]$', fontsize=labelsize)
ax2.set_xlabel(r'$t_{\rm ret} [M_{\odot}]$', fontsize=labelsize)
ax2.set_ylabel(r'$(r/M) h_{\times}\ \ (\times 10^{-3})$', fontsize=labelsize)

xa22 = xa/Madm_sur;    xb22=xb/Madm_sur;   dx22=(xb22-xa22)/10.
x22lim = (xa22, xb22)
ax22.set_xlim(x22lim)
ax22.xaxis.set_minor_locator(mticker.MultipleLocator(dx22/2.0))
ax22.xaxis.set_major_locator(mticker.MultipleLocator(dx22))
ax22.set_xticklabels([])

plt.savefig("rhphc_" + sys.argv[1] + "_" + sys.argv[2] + ".png")
#plt.show()

# Clear figure:
#fig.clear()


