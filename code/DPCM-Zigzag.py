import cv2
import numpy as np

def diff_predict_encode_modulate(image):
    
    gray_image_1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image_1.astype(np.int32)
    
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


image = cv2.imread('lena.bmp')


encoded_image = diff_predict_encode_modulate(image)
vector = encoded_image.ravel()
a=[]
for i in vector:
   a.append(int_to_zigzag(i)) 
out=open("matrix.txt","w")
for k in a:
    out.write(str(k)+"\t")
out.close()