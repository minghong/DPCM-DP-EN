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
                try:

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

                    signal.alarm(0)
                    try:
                      
                        Decode(file_in = encoded, out = decoded,
                               header_size = 4,  ## seed size 
                               chunk_num = chunk, ## source file chunk number
                               rs = 2,  ## reedsolo code byte number
                               
                               delta = 0.001, 
                               c_dist = 0.025,  
                               max_homopolymer = 3, 
                               gc = 0.1, 


                               max_hamming = 0).main()

                    except:
                            pass
                except Exception as e:
                    print(e)

if __name__ == "__main__":

    file_path = '/fs0/home/xuqi/encrpy_balance_GC/dataset/x-ray'
    depth_first(file_path)

