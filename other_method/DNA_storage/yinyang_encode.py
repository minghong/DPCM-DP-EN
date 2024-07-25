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
    coding_scheme = YinYangCode()
    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=None, need_logs=False)
    pipeline.transcode(direction="t_c", input_path=input_path, output_path=output_path,
                       segment_length=130, index=True)
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
def depth_first(path):       
    
    for i in os.listdir(path):
        child = os.path.join(path, i)
        if os.path.isdir(child):
            depth_first(child)
        else:
            if(os.path.splitext(child)[1] == ".png"):
                root_path = os.path.dirname(Chamaeleo.__file__)
                current_path = os.path.dirname(os.path.realpath(__file__))
                generated_file_path = current_path

                
                write_file_path = os.path.join(generated_file_path, "target.png")
                temp_model_path = os.path.join(generated_file_path, "model.pkl")
                dna_path = os.path.join(generated_file_path, "target.dna")
                

                try:
                    timeout_duration = 100
         

                    signal.signal(signal.SIGALRM, handle_timeout)
                    signal.alarm(timeout_duration)
                    
                    encode(model_path=temp_model_path, input_path=child, output_path=dna_path)
                    signal.alarm(0)

                    decode(model_path=temp_model_path, input_path=dna_path, output_path=write_file_path)

                except Exception as e:
                    print(e)

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
