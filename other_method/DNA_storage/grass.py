import os
import Chamaeleo
from Chamaeleo.methods.flowed import YinYangCode
from Chamaeleo.utils.data_handle import save_model, load_model
from Chamaeleo.utils.pipelines import TranscodePipeline
from collections import Counter
import os
import Chamaeleo
from Chamaeleo.methods.fixed import *
import numpy as np
from PIL import Image
import time
import os
import Chamaeleo
from Chamaeleo.methods.fixed import *
import numpy as np
import signal

from PIL import Image
def encode(model_path, input_path, output_path):
    coding_scheme = Grass()
    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=False)
    pipeline.transcode(direction="t_c", input_path=input_path, output_path=output_path,
                       segment_length=270, index=True)
    save_model(path=model_path, model=coding_scheme, need_logs=False)
    pipeline.output_records(type="string")


def decode(model_path, input_path, output_path):
    coding_scheme = load_model(path=model_path, need_logs=False)
    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=False)
    pipeline.transcode(direction="t_s", input_path=input_path, output_path=output_path, index=True)
    pipeline.output_records(type="string")
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
                start=time.time()
                root_path = os.path.dirname(Chamaeleo.__file__)
                current_path = os.path.dirname(os.path.realpath(__file__))
                generated_file_path = current_path

                
                write_file_path = os.path.join(generated_file_path, "target.png")
                temp_model_path = os.path.join(generated_file_path, "model.pkl")
                dna_path = os.path.join(generated_file_path, "target.dna")
                
                out_2=open("yinyang.txt","a+")
                out_2.write(child+"\t")
                start=time.time()
                
                
         

                
                
                encode(model_path=temp_model_path, input_path=child, output_path=dna_path)
                
                out_2.write(str(time.time()-start)+"\t")
                file = open("target.dna")
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
                               
                
                
                start=time.time()
                decode(model_path=temp_model_path, input_path=dna_path, output_path=write_file_path)
                out_2.write(str(time.time()-start)+"\n")
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
