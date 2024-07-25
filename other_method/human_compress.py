#coding: utf-8
from PIL import Image

import time

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
class node: 

    def __init__(self,right=None,left=None, parent=None, weight=0, code=None):
        self.left = left 
        self.right = right 
        self.parent = parent 
        self.weight = weight 
        self.code = code 
        

def picture_convert(filename): 
    picture = Image.open(filename)
    w,h=picture.size
    picture = picture.convert('L')
    return picture,w,h
 
#定义函数，统计每个像素出现的次数
def pixel_number_caculate(list):
    pixel_number={}
    for i in list:
        if i not in pixel_number. keys():
            pixel_number[i]=1 
        else:
            pixel_number[i] += 1 
    return pixel_number
 

def node_construct(pixel_number): 
    node_list =[]
    for i in range(len(pixel_number)):
        node_list.append(node(weight=pixel_number[i][1],code=str(pixel_number[i][0])))
    return node_list
 

def node_construct(pixel_number): 
    node_list =[]
    for i in range(len(pixel_number)):
        node_list.append(node(weight=pixel_number[i][1],code=str(pixel_number[i][0])))
    return node_list
 

def tree_construct(listnode):
    listnode = sorted(listnode,key=lambda node:node.weight) 
    while len(listnode) != 1:
        #每次取权值的两个像素点进行合并
        low_node0,low_node1 = listnode[0], listnode[1]
        new_change_node = node()
        new_change_node.weight = low_node0.weight + low_node1.weight
        new_change_node.left = low_node0
        new_change_node.right = low_node1
        low_node0.parent = new_change_node
        low_node1.parent = new_change_node
        listnode.remove(low_node0)
        listnode.remove(low_node1)
        listnode.append(new_change_node)
        listnode = sorted(listnode, key=lambda node:node.weight) 
    return listnode

def Huffman_Coding(picture):

    width = picture.size[0]
    height = picture.size[1]
    im = picture.load()

 

    list =[]
    for i in range(width):
        for j in range(height): 
            list.append(im[i,j])
 
    pixel_number = pixel_number_caculate(list)
    pixel_number = sorted(pixel_number.items(),key=lambda item:item[1])
           
 
    node_list = node_construct(pixel_number)

    head = tree_construct(node_list)[0]
           

    coding_table = {}
    for e in node_list:
        new_change_node = e
        coding_table.setdefault(e.code,"")
        while new_change_node !=head:
            if new_change_node.parent.left == new_change_node: 
                coding_table[e.code] = "1" + coding_table[e.code] 
            else:
                coding_table[e.code] = "0" + coding_table[e.code] 
            new_change_node = new_change_node. parent

    coding_result = ''
    for i in range(width):
        for j in range(height):
            for key,values in coding_table.items(): 
                if str(im[i,j]) == key:
                    coding_result = coding_result+values 
    return coding_result,coding_table

def Decoding(width,height,coding_table,coding_result): 
    code_read_now=''#当前读到的编码 
    new_pixel =[] 
    i = 0
    while (i != coding_result.__len__()):
        #每次往后读一位
        code_read_now = code_read_now + coding_result[i]
        for key in coding_table.keys():
            #如果当前读到的编码在编码表里存在 
            if str(code_read_now) == str(coding_table[key]): 
                new_pixel. append(key) 
                code_read_now =''
                break
        i +=1

    decode_image = Image.new( 'L' ,(width,height)) 
    k = 0 
    #篇予像聚值
    for i in range(width):
        for j in range(height):
            decode_image.putpixel((i,j),(int(new_pixel[k]))) 
            k+=1
    decode_image.save('decode.png')
from PIL import Image
def depth_first(path):       
    
    for i in os.listdir(path):
        child = os.path.join(path, i)
        if os.path.isdir(child):
            depth_first(child)
        else:
            if(os.path.splitext(child)[1] == ".png"):

                picture,w,height = picture_convert(child)
                h,table=Huffman_Coding(picture)

                Decoding(w,height,table,h)



file_path = '/fs0/home/xuqi/encrpy_balance_GC/dataset/x-ray'
depth_first(file_path)
