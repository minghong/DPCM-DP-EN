import cv2
import numpy as np
import sys
import os
import subprocess
from math import *
import time
import re
from collections import Counter
from PIL import Image
import random

import re
import subprocess
import math
from reedsolo import RSCodec

from decimal import Decimal


       








#24 mapping rules
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
    


def logistic_map(x, r):
    return r * x*(1-x)


def split_string_by_length(string, length):
    result = []
    for i in range(0, len(string), length):
        result.append(string[i:i+length])
    return result  

            



def decode_1(sequence):
    bits=""
    per=split_string_by_length(sequence,3)
    
    for i in per:
        bits+=i[0].replace('A','00').replace('C','01').replace('G','10').replace('T','11')
        bits+=i[1].replace('A','00').replace('C','01').replace('G','10').replace('T','11')
        bits+=i[2].replace('A','0').replace('C','0').replace('G','1').replace('T','1')
    
    return int(bits,2)*1e-5

def decode_2(sequence,x,r):
    string_local=""
    for aa in sequence:
        x = logistic_map(x, r)
        
        q=int((x*24000))%24   
        trans=method(q)
        reverse_dict1 = dict([(value,key) for (key,value) in trans.items()])
        string_local+=dna_decode(aa, reverse_dict1)
    return string_local

def zigzag_to_int(n):  


    return ((n) >> 1) ^ -(n & 1); 
def dna_decode(binary,DNA_encoding):

    return DNA_encoding[binary]
 

    

def rs_decode_bitstream(binary_code):

    rsc = RSCodec(2)
    #convert a string like ACTCA to an array of ints like [10, 2, 4]
    
    
    binary_code=binary_code.replace('A','00').replace('C','01').replace('G','10').replace('T','11')
    bytes_msg=bytes(int(binary_code[i:i+8],2)for i in range(0,len(binary_code),8))
    array_msg=bytearray(bytes_msg)
      
    data=rsc.decode(array_msg)
    binary_code=''.join(format(x,'08b') for x in data[0]) #转二进制
    data=''.join(str(int(binary_code[t:t+2],2)) for t in range(0, len(binary_code),2))
    return data.replace('0','A').replace('1','C').replace('2','G').replace('3','T')


if __name__ == "__main__":
    file=open("dna.txt")

    bitstream=""
    r = 3.9 
    dic_bitstream={}
    for line in file.readlines():
        sequence=rs_decode_bitstream(line.rstrip("\n"))
        f=decode_1(sequence[:12])
        dic_bitstream[f]=decode_2(sequence[12:],round(f,5),r)
    # sort small to large
    sorted_dict = {key: dic_bitstream[key] for key, value in sorted(dic_bitstream.items())}
    for value in sorted_dict.values():
        bitstream+=value 
        

    #decompress
    start=time.time()
    count=0
    d=[]
    bitstream=bitstream[:all_len_bitstream]
    while(count<len(bitstream)):
        
        number_of_bits=int(bitstream[count:count+4],2)+1;count_temp=int(bitstream[count+4:count+12],2)+1
        for i in range(count_temp):
            d.append(zigzag_to_int(int(bitstream[count+12+i*number_of_bits:count+12+(i+1)*number_of_bits],2)))
        count+=(number_of_bits*count_temp+12)
            

    matrix = np.reshape(d, (aa, bb))

    a,b=matrix.shape
    encoded_image = np.zeros((a, b), dtype=np.int32)

    for i in range(a):
        for j in range(b):
            if(i==0 and j==0):
                encoded_image[i][j] = matrix[i][j]
            elif(i==0):
                encoded_image[i][j] = encoded_image[i][j-1] + matrix[i][j]
            elif(j==0):
                encoded_image[i][j] = encoded_image[i-1][j] + matrix[i][j]
            else:
                encoded_image[i][j] = encoded_image[i-1][j] + encoded_image[i][j-1] - encoded_image[i-1][j-1]+ matrix[i][j]
    #output image
    image = Image.fromarray(np.uint8(encoded_image))
    image.save('01.png')