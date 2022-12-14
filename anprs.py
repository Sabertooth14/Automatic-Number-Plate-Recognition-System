# -*- coding: utf-8 -*-
"""ANPRS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NhH-zRcAgOix1nSVYnRYl7TzukU0H7Oi

Install all the libraries
"""

!pip install easyocr
!pip install imutils

import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils
import easyocr

"""Reading the image,Grayscaling,Blurrring the image"""

img = cv2.imread('4.jpeg') #Reading the image
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Grayscaling the image
plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB)) # Plotting the image

"""Applying the Filters and edge localization....
Filters is used to reduce the noise
"""

bfilter = cv2.bilateralFilter(gray,11,17,17) # Applying filter for noise reduction
edged = cv2.Canny(bfilter,40,200) # Edge detection
plt.imshow(cv2.cvtColor(edged,cv2.COLOR_BGR2RGB))

"""Find contours and apply masks"""

keypoint = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # Finding the shapes,returned a tree so as to traverse different levels of contour,chain approx returns a simplified version of the contour
contours = imutils.grab_contours(keypoint) # grabbing the contours from the keypoints
contours = sorted(contours,key = cv2.contourArea,reverse=True)[:10] # return the top 10 contours based on their area

location = None
for contour in contours: #looping theough the contours to get the location
  approx = cv2.approxPolyDP(contour,15,True) #Using the approxPolyDP to approxiamte the polygon form the contour
  if len(approx) == 4:
    location = approx
    break

location

mask = np.zeros(gray.shape,np.uint8) # created a blank mask, filling is done wiht blank 0's
new_img = cv2.drawContours(mask,[location],0,255,-1) # drawn the contour based on th location
new_img = cv2.bitwise_and(img,img,mask=mask) # Overlaying the mask on the original image and return the segment pf the imsge that has the number plate

plt.imshow(cv2.cvtColor(new_img,cv2.COLOR_BGR2RGB))

(x,y) = np.where(mask==255) # storing the location where the img isn't black
(x1,y1) = (np.min(x),np.min(y)) # getting the min x and y value
(x2,y2) = (np.max(x),np.max(y)) # getting the maximum x and y value
cropped_img = gray[x1:x2+1,y1:y2+1] # cropped the image to absed on the above coordinates

plt.imshow(cv2.cvtColor(cropped_img,cv2.COLOR_BGR2RGB))

"""Yse EasyOCR to read the text"""

reader = easyocr.Reader(['en']) # Chosen the language english
result = reader.readtext(cropped_img) # reading the textform the cropped image 
result

result[0][-2]

"""Rendering the result to the img"""

text = result[0][-2]
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=text, org=(approx[0][0][0],approx[1][0][1]+80), fontFace = font, fontScale=1,color=(0,255,0),thickness=2, lineType=cv2.LINE_AA)
res  = cv2.rectangle(img,tuple(approx[0][0]),tuple(approx[2][0]),(0,255,0),3)
plt.imshow(cv2.cvtColor(res,cv2.COLOR_BGR2RGB))

