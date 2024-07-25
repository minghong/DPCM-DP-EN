file=open("DPCM-DP-EN\\gc.txt")
out=open("DPCM-DP-EN_gc.txt","w")
k=100000
a=0
for line in file.readlines():
    tmp=line.rstrip("\n").split("\t")
    for data in tmp:
        try:
            if(a<=k):
                out.write(str(float(data))+"\n")
                a+=1
        except:
            pass
out.close()

file=open("church\\gc.txt")
out=open("church_gc.txt","w")
a=0
for line in file.readlines():
    tmp=line.rstrip("\n").split("\t")
    for data in tmp:
        try:
            if(a<=k):
                out.write(str(float(data))+"\n")
                a+=1
            else:
                break
        except:
            pass
out.close()
file=open("Grass\\gc.txt")
out=open("Grass_gc.txt","w")
a=0
for line in file.readlines():
    tmp=line.rstrip("\n").split("\t")
    for data in tmp:
        try:
            if(a<=k):
                out.write(str(float(data))+"\n")
                a+=1
            else:
                break
        except:
            pass
out.close()

file=open("Fountain\\gc.txt")
out=open("fountain_gc.txt","w")
a=0
for line in file.readlines():
    tmp=line.rstrip("\n").split("\t")
    for data in tmp:
        try:
            if(a<=k):
                out.write(str(float(data))+"\n")
                a+=1
            else:
                break
        except:
            pass
out.close()
file=open("Yinyang\\gc.txt")
out=open("yinyang_gc.txt","w")
a=0
for line in file.readlines():
    tmp=line.rstrip("\n").split("\t")
    for data in tmp:
        try:
            if(a<=k):
                out.write(str(float(data))+"\n")
                a+=1
            else:
                break
        except:
            pass
out.close()
