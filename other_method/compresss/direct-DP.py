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

from decimal import Decimal


def G(motif):

    process = subprocess.Popen('echo "%s" | RNAfold --noPS --noGU --noconv -T 59.1' % motif,
                               stdout=subprocess.PIPE, shell=True)

    process.wait()
    if process.returncode == 0:
        line = process.stdout.read().decode().split('\n')[1]
        new=Decimal(str(line)[str(line).rfind("(")+1:str(line).rfind(")")])
    if(new>-30):
        return True
    else:
        return False
        
def diff_predict_encode_modulate(image):
    # 将图像转换为灰度图
    gray_image_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image_1.astype(np.int32)
    return gray_image
    # 差分预测编码调制
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

    # 进行差分预测编码调制
    encoded_image = diff_predict_encode_modulate(image)
    vector = encoded_image.ravel()
    a=[]
    for i in vector:
       a.append(i) 
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
'''
def undired(string):
    if("AAA" in string):
        return False;
    if("TTT" in string):
        return False;
    if("CCC" in string):
        return False;
    if("GGG" in string):
        return False;
    return True
'''
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
        x = logistic_map(x, r) # 迭代计算
        
        q=int((x*24000))%24   
        trans=method(q)
        reverse_dict1 = dict([(value,key) for (key,value) in trans.items()])
        string_local+=dna_decode(aa, reverse_dict1)
    return string_local

def zigzag_to_int(n):  


    return ((n) >> 1) ^ -(n & 1); 
def dna_decode(binary,DNA_encoding):

    return DNA_encoding[binary]
def depth_first(path):       # 深度优先遍历文件夹，栈，先进后出，先找到最深的，再弹出来，消耗内存
    
    for i in os.listdir(path):
        child = os.path.join(path, i)
        if os.path.isdir(child):
            depth_first(child)
        else:
            if(os.path.splitext(child)[1] == ".png"):
                start=time.time()
                out_2=open("result_2.txt","a+")
                aa,bb=process(child)
                out_2.write(child+"\t"+str(os.path.getsize(child)*8)+"\t"+str(aa)+"\t"+str(bb)+"\t"+str(aa*bb*8)+"\t")
                subprocess.run(["g++", "dp-compress.cpp", "-o", "test"], capture_output=True, text=True)
                input_data=str(aa)+"\n"+str(bb)
                
                result=subprocess.run(["./test"], input=input_data,capture_output=True, text=True)
                out_2.write(result.stdout+"\t")
                
                
                
                out_2.write(str(time.time()-start)+"\t")
                start=time.time()
                with open("matrix.txt", 'r') as file:   #得到图像弓形数组向量
                    for line in file:
                        line = line.strip()
                        data = line.split("\t")

                #编码
                count=0
                bits_01=""
                with open("signal_pixel.txt", 'r') as file:  #根据动态规划结果将图像向量转为01比特
                    for line in file:
                        line = line.strip()
                        tmp = line.split(" ")
                        for i in range(int(tmp[0])):
                            binary_str = bin(int(data[count+i]))[2:]
                            binary_str = '0' * (int(tmp[1]) - len(binary_str)) + binary_str
                            
                            bits_01+=binary_str
                        count+=int(tmp[0])
                 
                
                
                out_2.write(str(time.time()-start)+"\t")
                start=time.time()
                count=0
                d=[]
                with open("signal_pixel.txt", 'r') as file:
                    for line in file:
                        line = line.strip()
                        tmp = line.split(" ")
                        a=int(tmp[0]);b=int(tmp[1])
                        for i in range(a):
                            d.append((int(bits_01[count+i*b:count+(i+1)*b],2)))
                        count+=(a*b)
                        
                #预测解码操作
                matrix = np.reshape(d, (aa, bb))

                
                
                
                
                image = Image.fromarray(np.uint8(matrix))
                image.save('01.png')
                out_2.write(str(time.time()-start)+"\n")
                out_2.close()
                
                
                
                
                
                


                
if __name__ == "__main__":


    out_2=open("result_2.txt","a+")
    out_2.write("file-name\tfile-size\theight\twight\theight*wight\tdp-size\tdp-compress-time\ttemp-time\tdecompress-time\n")
    out_2.close()
    file_path = '/fs0/home/xuqi/encrpy_balance_GC/dataset/x-ray'
    depth_first(file_path)



