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


        
def diff_predict_encode_modulate(image):
    # covert image to gray image
    gray_image_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image_1.astype(np.int32)
    # DPCM
    height, width = gray_image.shape
    encoded_image = np.zeros((height, width), dtype=np.int32)
    
    for i in range(0, height):
        for j in range(0, width):
            if(i==0 and j!=0):
                predicted_value=gray_image[i, j-1]
                diff = gray_image[i, j] - predicted_value
                encoded_image[i, j] = diff
            elif(i!=0 and j==0):
                predicted_value=gray_image[i-1, j]
                diff = gray_image[i, j] - predicted_value
                encoded_image[i, j] = diff
            else:
                predicted_value = gray_image[i-1, j] + gray_image[i, j-1] - gray_image[i-1, j-1]
                diff = gray_image[i, j] - predicted_value
                encoded_image[i, j] = diff
    encoded_image[0,0]=gray_image[0,0]
    return encoded_image
    #return gray_image
def find_max(matrix):
    max_val = float('-inf')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if abs(matrix[i][j]) > max_val:
                max_val = matrix[i][j]
    return max_val


def int_to_zigzag(n):

    return (n << 1) ^ (n >> 31);

def zigzag_to_int(n):  


    return ((n) >> 1) ^ -(n & 1); 

def process(file):
    image = cv2.imread(file)

    #DPCM
    encoded_image = diff_predict_encode_modulate(image)
    vector = encoded_image.ravel()
    a=[]
    #Zigzag
    for i in vector:
       a.append(int_to_zigzag(i)) 
    out=open("matrix.txt","w")
    
    for k in a:
        out.write(str(k)+"\t")
    out.close()
    return encoded_image.shape[0],encoded_image.shape[1]



def getMaxDupChar(s, startIndex, curMaxLen, maxLen):
    if startIndex == len(s) - 1:
        return max(curMaxLen, maxLen)
    if list(s)[startIndex] == list(s)[startIndex + 1]:
        return getMaxDupChar(s, startIndex + 1, curMaxLen + 1, maxLen)
    else:
        return getMaxDupChar(s, startIndex + 1, 1, max(curMaxLen, maxLen))
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
 

def rs_encode_bitstream(binary_code): #add rs
    binary_code=binary_code.replace('A','00').replace('C','01').replace('G','10').replace('T','11')
    rsc = RSCodec(2)
    bytes_msg=bytes(int(binary_code[i:i+8],2)for i in range(0,len(binary_code),8))
    array_msg=bytearray(bytes_msg)
    array_msg=rsc.encode(array_msg)

    binary_code=''.join(format(x,'08b') for x in array_msg)
    data=''.join(str(int(binary_code[t:t+2],2)) for t in range(0, len(binary_code),2))
    return data.replace('0','A').replace('1','C').replace('2','G').replace('3','T')
    

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

def depth_first(path):       
    
    for i in os.listdir(path):
        child = os.path.join(path, i)
        if os.path.isdir(child):
            depth_first(child)
        else:
            if(os.path.splitext(child)[1] == ".png"): #image file type
                
                aa,bb=process(child)  #DPCM-ZigZag
                subprocess.run(["g++", "dp-compress.cpp", "-o", "test"], capture_output=True, text=True) 
                input_data=str(aa)+"\n"+str(bb)
                result=subprocess.run(["./test"], input=input_data,capture_output=True, text=True)#DP-compress
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
                
                from collections import Counter


                
                #decode

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



                
if __name__ == "__main__":

    file_path = '/fs0/home/xuqi/encrpy_balance_GC/dataset/x-ray'  #image dataset
    depth_first(file_path)
    


