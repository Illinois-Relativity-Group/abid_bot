import os
bh_f_list = "bhfiles.txt"
f = open(bh_f_list, "r")
for line in f.readlines():
    li = line.strip()
    fnlen=len(li)
    t = int(li[4:fnlen-3])
    if t % 512 != 0:
        os.remove("bhdata/" + li)

