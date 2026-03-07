# usage: change the format of spin data so it works with changes made in abid_bot_v2.11
# written by eric yu 6/9/22
#
# if you have 2 spin vectors at the same time, then the data will have 7 columns like
#
# time  Sx1     Sy1     Sz1     Sx2     Sy2     Sz2
#
# this script splits it up into two seperate files of the format
#
# time  Sx      Sy      Sz
#
# so we have one file for each BH
#
# sometimes you may get a file from Milton that has a lot of columns
# ask him which ones should be plotted
# # # CHANGE THIS LIST OF SPIN FILES # # # # # # #
# all of these files should be in the same format (i.e. have the same number of columns excluding comments)
spinf_list = ['bhns_BHspin_processed.mon']
# you may not need out2, rename files and change columns accordingly
# col[0] = Sx, col[1] = Sy, col[2] = Sz, make sure you don't go out of bounds
# indices relating to columns of the original spinf are 0-indiced
outf1 = 'bhns_BHspin_processed2.mon'; cols1 = [10, 11, 12]
out2_flag = False
outf2 = 'BHspin_ah2.mon'; cols2 = [17, 18, 19]
# # # # # # # # # # # # # # # # # # # # # # # # #
#list of the first Time of each file so there are no overlaps
firstTimes = []
for spinf in spinf_list:
        f = open(spinf, 'r')
        firstTime = f.readlines()[1].strip().split()[0]
        firstTimes.append(firstTime)
        print(firstTime)
        f.close()
out1 = open(outf1, 'w')
if out2_flag: out2 = open(outf2, 'w')

out1.write("#Time       Sx1     Sy1     Sz1\n")
if out2_flag: out2.write("#Time       Sx2     Sy2     Sz2\n")

numFiles = len(spinf_list)

for i in range(numFiles):
        f = open(spinf_list[i], 'r')
        for line in f.readlines():
                li = line.strip()
                if not li.startswith('#'):
                        lis = li.split()
                        if len(lis) != 4:
                                if (i == numFiles - 1) or ((i != numFiles - 1) and (lis[0] < firstTimes[i + 1])):
                                        out1.write(lis[0] + ' ' + lis[cols1[0]] + ' ' + lis[cols1[1]] + ' ' + lis[cols1[2]] + '\n')
                                        if out2_flag: out2.write(lis[0] + ' ' + lis[cols2[0]] + ' ' + lis[cols2[1]] + ' ' + lis[cols2[2]] + '\n')
        f.close()



out1.close()
if out2_flag: out2.close()