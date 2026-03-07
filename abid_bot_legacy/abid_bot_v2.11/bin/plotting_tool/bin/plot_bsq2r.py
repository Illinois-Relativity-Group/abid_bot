import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from sys import argv

from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from mpl_toolkits.mplot3d import Axes3D

oldversion=int(argv[3])
M_ADM=2.6

root = "/home1/07525/tg868241/stbrmt_abid/plotting_tool/"
filename=root+argv[1]
savefolder=root+"plots/"


plt.rc('font', serif='palatino')
#plt.rc('font', weight='black')
print("setting 1")
plt.rc('mathtext', default='sf')
plt.rc('xtick.major', pad=8)
plt.rc('ytick.major', pad=8)
plt.rc('xtick.major', size=13)
plt.rc('ytick.major', size=13)
plt.rc('xtick.major', width=1.5)
plt.rc('ytick.major', width=1.5)
plt.rc('xtick.minor', size=7)
plt.rc('ytick.minor', size=7)
plt.rc('xtick.minor', width=1)
plt.rc('ytick.minor', width=1)
plt.rc('xtick', direction='in')
plt.rc('ytick', direction='in')
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)

fig=plt.figure(figsize=(9.0,8.0))
fig.subplots_adjust(left=0.15)
fig.subplots_adjust(bottom=0.13)
fig.subplots_adjust(top=0.95)
fig.subplots_adjust(right=0.95)

#ax1=fig.add_subplot(1,1,1)


#plt.tick_params(which='major', length=10, width=1)
#ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
#ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
#ax1.grid()
#ax1.xaxis.set_ticks_position('both')
#ax1.yaxis.set_ticks_position('both')

print("1")
data=np.loadtxt(filename, delimiter='\t')
print (data[0])

if oldversion:
	x=data[:,1]/M_ADM
	y=data[:,2]
else:
	x=data[:,2]
	y=data[:,3]

i=0
while x[i]<4570:
	i=i+1

print(i)
x=x[i:]
y=y[i:]

x=x-x[0]

fit = np.polyfit(x, y, 4)
p1 = np.poly1d(fit)
print(p1)

yfit = p1(x)

plt.rc('legend', fontsize=20)
plt.scatter(x,y, marker='x')
plt.plot(x, yfit, color=(0,0,0))
#plt.xlim(.01,5)
#plt.ylim(.05,0.2)#1.6e-4*M)
plt.xlabel(r'$(t-t_{bh})/M$', fontsize=20)
plt.ylabel(r'$log(b^2/2\rho_0)$', fontsize=20)
plt.title('bsq2r_v_time, '+argv[2], fontsize=20)

plt.savefig(savefolder+argv[2]+".png",dpi=100)
