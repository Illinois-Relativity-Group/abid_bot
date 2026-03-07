import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from os import listdir
from sys import argv
import pylab

#This program plots all files at once and saves one image

M=float(argv[1])
dt=float(argv[2])
n_frac=float(argv[3])
offset=2 #number of points to ignore near origin


# plot t =0 data in red


#plot the last and first data point
files=listdir("w_data")
times=[int(i[2:-4]) for i in files]
times.sort()
last_t = times[-1]
first_t = times[0]
data0 = pylab.loadtxt("w_data/w_"+str(first_t).zfill(6)+".txt")
plt.plot(data0[offset:,0]/M, data0[offset:,1]*M, ls='-', lw=4, color=[1,0,0], label="t/P="+str(first_t))
last_toM = float(last_t)
data_last = pylab.loadtxt("w_data/w_"+str(last_t).zfill(6)+".txt")
#plt.plot(data_last[offset:,0]/M, data_last[offset:,1]*M, '--', lw=3, color=[0,0,0], label="t/M="+str(int(last_toM))+"(last)")
period=2*np.pi/data0[0,1]/M
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


times=[str(int(t)).zfill(6) for t in times1]
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
step=int(np.ceil(n_thread*0.1))
timelist=[i for i in range(step,n_thread,step)]
for i in timelist[0:3]:
	t_over_P = int(int(times[i])/period)+1
	colors = [255/255.,220/255.,0/255.] 
	plt.rc('legend', fontsize=11)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= '       '+ str(t_over_P))

for i in timelist[3:6]:
	t_over_P = int(int(times[i])/period)+1
	colors = [95/255.,158/255.,160/255.]
	plt.rc('legend', fontsize=11)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= '       '+ str(t_over_P))

for i in timelist[6:]:
	t_over_P = int(int(times[i])/period)+1
	colors = [65/255.,105/255.,225/255.]
	plt.rc('legend', fontsize=11)
	plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M, ls='-', lw=2, color=colors, label= '       '+ str(t_over_P))
'''
for i in [18,20]:
        t_over_P = int(int(times[i])/period)+1
	colors = [0.0,0.0,0.0]
        plt.rc('legend', fontsize=11)
        plt.plot(data[i][offset:,0]/M,data[i][offset:,1]*M,lw=2, color=colors, label= '       '+ str(t_over_P))
'''




x=np.linspace(200,350,101)
x_tail = (np.abs(data[n-1][offset:,0]/M-x[-1])).argmin()
def curve(x):
	return M*0.000025*(x*M/1000)**(-3/2)
last_data = data[n-1][offset:,1][x_tail]*M
curve_offset = np.abs(curve(x[-1])-last_data)*1.97





plt.plot(x,curve(x)+curve_offset, '--', lw=6, color=(0,0,1,.9)) #, label="r^-3/2")

plt.xlim(0,5)
plt.ylim(0,0.1*M)#1.6e-4*M)
plt.xlabel(r'$r/M$')
plt.ylabel(r'$\Omega \times M$')
plt.title("Evolution of Omega (P = %.2f M)" %period)
plt.annotate(r'$\sim r^{-3/2}$',xy=(225,last_data*2.5),fontsize=18, color = 'b')
plt.legend()
#plt.show()
plt.savefig("png_ave/AllTimes_mode3.png", dpi=300)
