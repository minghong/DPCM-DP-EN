# encoding: utf-8
import os
from time import sleep
import math
import time
from encode import Encode
from decode import Decode
import signal
from collections import Counter
def gc(sequence):
    dic=dict(Counter(sequence))
    for k in ["A","T","G","C"]:
        dic.setdefault(k,0)
    return (dic["G"]+dic["C"])/(dic["A"]+dic["T"]+dic["G"]+dic["C"])
def handle_timeout(signum, frame):
    raise Exception("Timeout!")
    
def depth_first(path):       # 深度优先遍历文件夹，栈，先进后出，先找到最深的，再弹出来，消耗内存
    
    for i in os.listdir(path):
        child = os.path.join(path, i)
        if os.path.isdir(child):
            depth_first(child)
        else:
            if(os.path.splitext(child)[1] == ".png"):
                source = child
                encoded = 'test.encoded'
                decoded = 'test.png'
                sourcesize = (os.path.getsize(source))
                size = 30 
                chunk = math.ceil(sourcesize / size)
                out_2=open("result_2.txt","a+")
                out_2.write(child+"\t")
                    
                try:
                    print(source)
                    timeout_duration = 20
         

                    signal.signal(signal.SIGALRM, handle_timeout)
                    signal.alarm(timeout_duration)
                    start=time.time()
                    Encode(file_in=source,out=encoded,
                           size=size,
                           rs=2,  ## reedsolo code byte number
                           
                           ## biological parameter
                           max_homopolymer=3,
                           gc=0.1,
                           delta=0.001,
                           c_dist=0.025,
                           
                           ## ensure stop > chunk size
                           stop = chunk*1.3,
                           no_fasta=True).main()
                    
                    out_2.write(str(time.time()-start)+"\t")
                    signal.alarm(0)
                    file = open(encoded,"r")
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
                    out_2.write(str(a["A"])+"\t")
                    out_2.write(str(a["T"])+"\t")
                    out_2.write(str(a["G"])+"\t")
                    out_2.write(str(a["C"])+"\t")
                    file.close()
                    
                    
                    
                    
                    try:
                        
                        
                        start=time.time()
                        
                        Decode(file_in = encoded, out = decoded,
                               header_size = 4,  ## seed size 
                               chunk_num = chunk, ## source file chunk number
                               rs = 2,  ## reedsolo code byte number
                               
                               delta = 0.001, 
                               c_dist = 0.025,  
                               max_homopolymer = 3, 
                               gc = 0.1, 


                               max_hamming = 0).main()
                        out_2.write(str(time.time()-start)+"\n")
                        out_2.close()
                    except:
                        out_2.write("wrong"+"\n")
                        out_2.close()
                except Exception as e:
                    print(e)
                    out_2.write("TLE"+"\n")
                    out_2.close()
if __name__ == "__main__":
    dic_A={}
    dic_C={}
    dic_G={}
    dic_T={}

    file_path = '/fs0/home/xuqi/encrpy_balance_GC/dataset/x-ray'
    depth_first(file_path)
    out_A=open("A.txt","w");out_C=open("C.txt","w");out_G=open("G.txt","w");out_T=open("T.txt","w")
    for k,v in dic_A.items():
        out_A.write(str(k)+"\t"+str(v)+"\n")
    out_A.close()
    for k,v in dic_C.items():
        out_C.write(str(k)+"\t"+str(v)+"\n")
    out_C.close()
    for k,v in dic_G.items():
        out_G.write(str(k)+"\t"+str(v)+"\n")
    out_G.close()
    for k,v in dic_T.items():
        out_T.write(str(k)+"\t"+str(v)+"\n")
    out_T.close()
