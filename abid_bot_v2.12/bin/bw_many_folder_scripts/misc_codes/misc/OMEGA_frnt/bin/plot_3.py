import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from os import listdir
from sys import argv
import pylab
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

#print("imported")



#This program plots all files at once and saves one image

M=float(argv[1])
dt=float(argv[2])
n_frac=float(argv[3])
offset=2 #number of points to ignore near origin


# plot t =0 data in red

#fig=plt.figure(figsize=(9.0,8.0))
#fig.subplots_adjust(left=0.15)
#fig.subplots_adjust(bottom=0.13)
#fig.subplots_adjust(top=0.95)
#fig.subplots_adjust(right=0.95)
#ax1=fig.add_subplot(1,1,1)

#plt.rc('text', usetex=True)
#plt.rc('font', family='freeserif')

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
ax1=fig.add_subplot(1,1,1)


plt.tick_params(which='major', length=10, width=1)
ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
ax1.grid()
ax1.xaxis.set_ticks_position('both')
ax1.yaxis.set_ticks_position('both')

print("settings")

#plot the last and first data point
files=listdir("w_data")
times=[int(i[2:-4]) for i in files]
times.sort(key=int)
last_t = times[-1]
#first_t = times[0]
first_t= 14451
data0 = pylab.loadtxt("w_data/w_"+str(first_t).zfill(5)+".txt")
period=2*np.pi/data0[offset,1]/M
#print(period)
plt.plot(data0[offset:,0]/M, data0[offset:,1]*M, ls='-', lw=2, color=[0,0,0], label=r"$t/P_c = $"+str(int(np.ceil(first_t/period)/10)))
#print("here")
last_toM = float(last_t)
data_last = pylab.loadtxt("w_data/w_"+str(last_t).zfill(5)+".txt")
#plt.plot(data_last[offset:,0]/M, data_last[offset:,1]*M, '--', lw=3, color=[0,0,0], label="t/M="+str(int(last_toM))+"(last)")
print('period=',period)



# plot other time-averaged data
files_temp=listdir("t_ave/")
files=[]
for i in files_temp:
	if(i[:5]=="w_ave"):
		files.append(i)
files.sort()
n=len(files)

data=[]
times1=[]
for num,i in enumerate(files):
	data.append(np.loadtxt("t_ave/"+i))
	data[num]=data[num][data[num][:,0].argsort()]
	#print(i)
	times1.append(i[5:-4])


times=[str(int(t)).zfill(5) for t in times1]
period2=int((int(times[-1])-int(times[-2])))
print('period2=',period2)
#period=period2

'''
for i in range(1,n,2):
	t_over_P = int(int(times[i])/period)+1
	blues=[float(3*(n-i))/(5*n),float(4*(n-i))/(5*n),float((n-i))/n]     
	plt.rc('legend', fontsize=11)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=blues, label=str(t_over_P)) 
	        #plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=blues, label="t/M="+str(int(times[i])))                                                                                             
'''

n_thread=int(n*n_frac)
step=int(np.ceil(n_thread/7))
timelist=[i for i in range(step,n_thread,step)]
'''
for i in timelist[0:1]:
	t_over_P = int(int(times[4])/(10*period))+1
	colors = [0/255.,220/255.,220/255.] 
	plt.rc('legend', fontsize=20)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))
'''
for i in timelist[0:2]:
	t_over_P = int(int(times[i])/(10*period))+1
	colors = [0/255.,1.,0/255.]
	plt.rc('legend', fontsize=20)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))
'''
for i in timelist[2:3]:
        t_over_P = int(int(times[13])/(10*period))+1
        colors = [200/255.,0/255.,200/255.]
        plt.rc('legend', fontsize=20)
        plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))
'''
for i in timelist[2:4]:
	t_over_P = int(int(times[i])/(10*period))+1
	colors = [0/255.,0/255.,255/255.]
	plt.rc('legend', fontsize=20)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))
'''
for i in timelist[4:5]:
	t_over_P = int(int(times[21])/(10*period))+1
	colors = [0.825,.2,0.]
	plt.rc('legend', fontsize=20)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))
'''
for i in timelist[4:]:
	t_over_P = int(int(times[i])/(10*period))+1
	colors = [1.,0.,0.]
	plt.rc('legend', fontsize=20)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= r'$t/P_c = $'+ str(t_over_P))

'''
for i in [18,20]:
        t_over_P = int(int(times[i])/period)+1
	colors = [0.0,0.0,0.0]
        plt.rc('legend', fontsize=11)
        plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=colors, label= '       '+ str(t_over_P))
'''



"""
x=np.linspace(.5,5,101)
x_tail = (np.abs(data[n-1][offset:,0]/M-x[-1])).argmin()
def curve(x):
	return M*0.000025*(x*M/1000)**(-3/2)
last_data = data[n-1][offset:,1][x_tail]*M
curve_offset = np.abs(curve(x[-1])-last_data)*1.97
print(curve_offset)
#curve_offset=0



plt.plot(x,curve(x)+curve_offset, '--', lw=6, color=(0,0,1,.9)) #, label="r^-3/2")
"""






#plt.vlines(1.19,0,.325,linestyles='dashed')
plt.xlim(.01,5)
plt.ylim(.05,0.2)#1.6e-4*M)
plt.xlabel(r'$r/M$', fontsize=20)
plt.ylabel(r'$M\ \Omega$', fontsize=20)
#plt.title("Evolution of Omega (P = %.2f M)" %period)
plt.title(r'NS2-SLy-Delay', fontsize=20)
#plt.annotate(r'$\sim r^{-3/2}$',xy=(3,last_data*2.5),fontsize=18, color = 'b')
plt.legend()
#plt.show()
plt.savefig("png_ave/AllTimes_mode3_zoom.png", dpi=300)
