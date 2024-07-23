import random
import numpy as np
from PIL import Image
import re
import numpy as np
from collections import Counter
import random
import numpy as np
from PIL import Image
import re
import numpy as np

import random
from collections import Counter

import os

def getMaxDupChar(s, startIndex, curMaxLen, maxLen):
    if startIndex == len(s) - 1:
        return max(curMaxLen, maxLen)
    if list(s)[startIndex] == list(s)[startIndex + 1]:
        return getMaxDupChar(s, startIndex + 1, curMaxLen + 1, maxLen)
    else:
        return getMaxDupChar(s, startIndex + 1, 1, max(curMaxLen, maxLen))

def method(num):
    if(num==0):
        return {"00": "A","11": "T","10": "C","01": "G"}
    if(num==1):
        return {"00": "A","11": "T","10": "G","01": "C"}
    if(num==2):
        return {"00": "A","11": "G","10": "T","01": "C"}
    if(num==3):
        return {"00": "A","11": "G","10": "C","01": "T"}
    if(num==4):
        return {"00": "A","11": "C","10": "T","01": "G"}
    if(num==5):
        return {"00": "A","11": "C","10": "G","01": "T"}
    if(num==6):
        return {"00": "G","11": "C","10": "T","01": "A"}
    if(num==7):
        return {"00": "G","11": "C","10": "A","01": "T"}
    if(num==8):
        return {"00": "G","11": "T","10": "C","01": "A"}
    if(num==9):
        return {"00": "G","11": "T","10": "A","01": "C"}
    if(num==10):
        return {"00": "G","11": "A","10": "C","01": "T"}
    if(num==11):
        return {"00": "G","11": "A","10": "T","01": "C"}
    if(num==12):
        return {"00": "C","11": "G","10": "T","01": "A"}
    if(num==13):
        return {"00": "C","11": "G","10": "A","01": "T"}
    if(num==14):
        return {"00": "C","11": "T","10": "G","01": "A"}
    if(num==15):
        return {"00": "C","11": "T","10": "A","01": "G"}
    if(num==16):
        return {"00": "C","11": "A","10": "T","01": "G"}
    if(num==17):
        return {"00": "C","11": "A","10": "G","01": "T"}
    if(num==18):
        return {"00": "T","11": "A","10": "C","01": "G"}
    if(num==19):
        return {"00": "T","11": "A","10": "G","01": "C"}
    if(num==20):
        return {"00": "T","11": "G","10": "C","01": "A"}
    if(num==21):
        return {"00": "T","11": "G","10": "A","01": "C"}
    if(num==22):
        return {"00": "T","11": "C","10": "G","01": "A"}
    if(num==23):
        return {"00": "T","11": "C","10": "A","01": "G"}
    
def dna_encode(binary,DNA_encoding):

    return DNA_encoding[binary]
def image_to_bitstream(image_path):
    img = Image.open(image_path)
    img_arr = np.array(img)   
    
    bitstream = ''.join([f"{bin(pixel)[2:].zfill(8)}" for pixel in img_arr.flatten()])
    return bitstream


def bitstream_to_image(bitstream, image_size):
    array_length = image_size[0] * image_size[1]
    
    image_array = np.array([int(bitstream[i:i+8], 2) for i in range(0, array_length*8, 8)], dtype=np.uint8)
    image_array = image_array.reshape(image_size[1], image_size[0])
    image = Image.fromarray(image_array)
    return image
def logistic_map(x, r):
    return r * x*(1-x)
def gc(sequence):
    dic=dict(Counter(sequence))
    for k in ["A","T","G","C"]:
        dic.setdefault(k,0)
    return (dic["G"]+dic["C"])/(dic["A"]+dic["T"]+dic["G"]+dic["C"])
def test(string):
    if("AAAA" in string):
        return False;
    if("TTTT" in string):
        return False;
    if("CCCC" in string):
        return False;
    if("GGGG" in string):
        return False;
    return True

def split_string_by_length(string, length):
    result = []
    for i in range(0, len(string), length):
        result.append(string[i:i+length])
    return result  
def encode_1(binary):
      
    DNA_encoding = {"00": "A","01": "C","10": "G","11": "T"}
    binary_list = [binary[i: i+2] for i in range(0, len(binary), 2)]    
    DNA_list = []
    for num in binary_list:
        for key in list(DNA_encoding.keys()):
            if num == key:
                DNA_list.append(DNA_encoding.get(key))

    return "".join(DNA_list)

def encode_2(binary,base):
    
    if(binary=="0"):
        if(base=="A"):
            return "C"
        else:
            return "A"
    else:
        if(base=="T"):
            return "G"
        else:
            return "T"
def five_bits_to_three_base(number):
    bases=""
    x=bin(number)[2:].zfill(20)
    per=split_string_by_length(x, 5)
    for i in per:
        bases+=encode_1(i[0:2])
        bases+=encode_1(i[2:4])
        bases+=encode_2(i[4],encode_1(i[2:4]))
    
    return bases
  

if __name__ == "__main__":
    with open("matrix.txt", 'r') as file:   
        for line in file:
            line = line.strip()
            data = line.split("\t")   #image matrix

    #encode
    count=0
    bits_01=""
    with open("signal_pixel.txt", 'r') as file:  #covert matrix to bitstream 
        for line in file:
            line = line.strip()
            tmp = line.split(" ")
            number_of_bits=bin(int(tmp[1])-1)[2:].zfill(4)  #number_of_bits
            count_temp=bin(int(tmp[0])-1)[2:].zfill(8)      #count
            #4-bits(number_of_bits)+8-bits(count)+dynamic-bits(pixel)
            bits_01=bits_01+number_of_bits+count_temp
            for i in range(int(tmp[0])):
                binary_str = bin(int(data[count+i]))[2:]
                binary_str = '0' * (int(tmp[1]) - len(binary_str)) + binary_str  
                
                bits_01+=binary_str    
            count+=int(tmp[0])
    all_len_bitstream=len(bits_01)
    bits_01+="0"*(304-(len(bits_01)-len(bits_01)//304*304))        
    f= 0 # initial para
    r = 3.9 
    out=open("dna.txt","w")
    binary=split_string_by_length(bits_01, 304)     
    for m in binary:
        
        flag=1
        f=round(f+0.00001,5)
        while(flag==1):
            
            
            string=""
            x=f
            bits_2=re.findall(r'\w{2}', m) 
            for aaa in bits_2:
                x = logistic_map(x, r) #
                q=int((x*24000))%24    
                string+=dna_encode(aaa, method(q))
            #para to base
            sequence=five_bits_to_three_base(round(f*1e5))+string
            
            sequence_rs=rs_encode_bitstream(sequence)
            #iterate
            if(gc(sequence_rs)<=0.6 and gc(sequence_rs)>=0.4 and test(sequence_rs)):
                flag=0
                out.write(sequence_rs+"\n")
            else:
                f=round(f+0.00001,5)
      
    out.close()                




