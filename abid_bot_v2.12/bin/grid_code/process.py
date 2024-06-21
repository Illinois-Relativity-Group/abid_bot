bh_f = "bhcen1_og.txt"
out_f = "bhcen1.txt"
f = open(bh_f, 'r')
out = open(out_f, 'w')
i = 0
for line in f.readlines():
    if i % 2 == 0: out.write(line)
    i += 1



f.close()
out.close()

