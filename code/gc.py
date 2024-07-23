from collections import Counter


a=Counter()
out_3=open("gc.txt","a")
    
for line in file.readlines():
    a+=dict(Counter(line.rstrip("\n")))
    h=dict(Counter(line.rstrip("\n")))
    length=len(line.rstrip("\n"))
    if("A" in h):
        global dic_A;
        dic_A[h["A"]/length] = dic_A.get(h["A"]/length, 0) + 1  
    else:
        dic_A[0] = dic_A.get(0, 0) + 1 
    if("C" in h):
        global dic_C;
        dic_C[h["C"]/length] = dic_C.get(h["C"]/length, 0) + 1  
    else:
        dic_C[0] = dic_C.get(0, 0) + 1 
    if("G" in h):
        global dic_G;
        dic_G[h["G"]/length] = dic_G.get(h["G"]/length, 0) + 1  
    else:
        dic_G[0] = dic_G.get(0, 0) + 1 
    if("T" in h):
        global dic_T;                    
        dic_T[h["T"]/length] = dic_T.get(h["T"]/length, 0) + 1   
    else:
        dic_T[0] = dic_T.get(0, 0) + 1
    out_3.write(str(gc(line.rstrip("\n")))+"\t")
out_3.write("\n")
out_3.close()


file.close()