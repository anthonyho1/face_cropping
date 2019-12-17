#!/usr/bin/env python3

import cv2 as cv 
import numpy as np 
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import time

SCALE_FACTOR = 0.05

def get_file_path():
    path = askdirectory(title='Select Folder') # shows dialog box and return the path
    return path
    
def image_preprocessing(img):
    height, width, _ = img.shape
    h = int(height * SCALE_FACTOR)
    w = int(width * SCALE_FACTOR)
    img_resized = cv.resize(img, (w, h))

    # top = 0
    # bot = h#int(h*0.7)
    # left = 0#int(w*0.2)
    # right = w#int(w*0.8)

    # img_crop = img_resized[top:bot, left:right]
    return img_resized 

def find_faces(img):
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    height, width, _ = img.shape
    
    faces = face_cascade.detectMultiScale(imgray, scaleFactor=2, minNeighbors=1, minSize=(int(width*0.002),int(height*0.002)))

    face_pts = []
    if faces.any():
        face_pts = faces[0]
        x,y,w,h = face_pts

    return face_pts

def translate_pts(pts):
    x,y,w,h = pts
    half_w = x + int(w/2)

    length = w if w > h else h

    top = int((y-0.3*length)/SCALE_FACTOR)
    bot = int((y+1.2*length)/SCALE_FACTOR)
    left = int((half_w - length*0.75)/SCALE_FACTOR)
    right = int((half_w + length*0.75)/SCALE_FACTOR)
    
    return left, right, top, bot

def main():
    print("Please select the source folder with the pictures")
    path = get_file_path()
    files = os.listdir(path)

    print("Please select the folder destination")
    folder = get_file_path()

    print(folder)

    for file in files:
        print(folder +'/'+ file)
        img = cv.imread(path + '/'+ file)

        img_cropped = image_preprocessing(img)

        start = time.time()
        face = find_faces(img_cropped)
        end = time.time()
        left, right, top, bot = translate_pts(face)

        print(str(end - start))
        face_img = img[top:bot, left:right]
        cv.imwrite(folder +'/'+ file, face_img)

main()



