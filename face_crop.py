#!/usr/bin/env python

import cv2 as cv 
import numpy as np 
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import time 
import threading
import queue

# constants 
SCALE_FACTOR = 0.05 # Scales image by scale_factor
HORIZ_STRETCH = 0.75 # The extra factor that is added onto the face bounding box to
                     # expand it for the real picture
TOP_STRETCH = 0.3 # Extra factor that is added to the top of the face bounding box
BOT_STRETCH = 1.2 # Extra factpr added to bottom of face bounding box

NUM_THREADS = 4

# shows dialog box and prompts user to select folder
def get_file_path():
    return askdirectory(title='Select Folder') # shows dialog box and return the path
    
# Downsizes image, easier for the facial detection to process fewer pixels
# Shrinks image by factof SCALE_FACTOR
def image_preprocessing(img):
    height, width, _ = img.shape
    h = int(height * SCALE_FACTOR)
    w = int(width * SCALE_FACTOR)

    top = 0
    bot = int(h*0.7)
    left = int(w*0.15)
    right = int(w*0.85)

    img = cv.resize(img, (w, h)) # returns resized image 


    return img[top:bot, left:right], left # left is the left point that is cropped, 
                                          # it is added on later when translating the image

# uses haar cascade to find face in image
# param: cv image 
def find_faces(img):
    # HAAR CASCADE MACHINE LEARNING ADVANCED ALGORITHM 
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    height, width, _ = img.shape
    faces = face_cascade.detectMultiScale(
                    imgray,
                    scaleFactor=1.1, # scale factor is the amount the haar cascade scales
                    minNeighbors=2, # neighbours is the number of repeated faces it needs to capture for it to be considered a face
                    minSize=(int(width*0.15),int(height*0.15))) # min size is the min feature size of face

    # print(int(width*0.1), int(height*0.1))
    #print(faces)
    face_pts = []
    if len(faces) != 0:
        face_pts = faces[0] # pretty jank, only take the first face in list, will work on finding best face
        x,y,w,h = face_pts
        # print(w, h)

    return face_pts # returns location of top left coordinate and height/width of bounding box 

# Maps corners of face bounding box of the shrunk image to points on the large image
# param: pts - coordinate of top left corner of bounding box, width, height as a list
#        left_pt - the point at which the preprocessed image was cropped
#        height, width - height and width of original image
def translate_pts(pts, left_pt, height, width):
    x,y,w,h = pts # x and y are coordinates of top left corner of bounding box, w&h are width and height
    half_w = x + int(w/2) # finds halfway point of bounding box 

    length = w if w > h else h # makes sure the image is a square, takes the largest of w or h

    # expands the face bounding box
    # If points are outside bounds, set it to bounds
    top = int((y - TOP_STRETCH*length) / SCALE_FACTOR)
    if top < 0:
        top = 0

    bot = int((y + BOT_STRETCH*length) / SCALE_FACTOR)
    if bot > height:
        bot = height

    left = int((left_pt + half_w - length * HORIZ_STRETCH) / SCALE_FACTOR)
    # if left < 0:
    #     left = 0
    #     print('left')

    right = int((left_pt + half_w + length * HORIZ_STRETCH) / SCALE_FACTOR)
    # if right > width:
    #     right = width
    #     print('right')
    
    # print(left,right,top,bot)
    return left, right, top, bot # new points for the large image

# function that each thread runs
# takes in destination and each thread's portion of the total files
# each thread has a fraction of the files to iterate through
def iterate_files(files, dest_folder, uncropped_files):

    for file in files:
        print(file)
        img = cv.imread(path + '/'+ file)

        height, width, _ = img.shape
        img_cropped, left_pt = image_preprocessing(img)

        face = find_faces(img_cropped)

        # print(face)
        # if no face in frame, continue and add it to list of uncropped photos
        if len(face) == 0:
            uncropped_files.append(file)
            continue
        
        left, right, top, bot = translate_pts(face, left_pt, height, width)
        face_img = img[top:bot, left:right] # crops photo from points found using translate_pts
        cv.imwrite(dest_folder +'/'+ file, face_img) # saves photo in destination folder

# main function
def main(dest_folder):
    start = time.time()

    num_photos = len(files)
    files_split = [[]] * NUM_THREADS # file_split splits up total files into several smaller lists for each thread
    uncropped = [[]] * NUM_THREADS # uncropped images for each thread
    threads = [] 

    # initializes threads
    for i in range(NUM_THREADS):
        files_split[i] = files[i*num_photos//NUM_THREADS:(i+1)*num_photos//NUM_THREADS]
        threads.append(threading.Thread(target=iterate_files, args=(files_split[i], dest_folder, uncropped[i])))
        threads[i].start()

    # join threads at the end when they are done their processes
    for i in range(NUM_THREADS):
        threads[i].join()

    # prints file names for all uncropped files
    uncrop = []
    for files_uncropped in uncropped:
        if files_uncropped:
            uncrop.extend(files_uncropped)
    if uncrop:
        print("Files that were uncropped: ")
        print(uncrop)

    # time indicator
    end = time.time()
    print('Time elapsed: '+ str(end - start)+ ' s')

if __name__ == '__main__':
    # user interface, prompt user to select folders
    print("Please select the source folder with the pictures")
    path = get_file_path()
    files = os.listdir(path)

    print("Please select the folder destination")
    print("Warning! If the images have the same name as any file in the \
           desination folder, they WILL be overwritten!")
    
    dest_folder = get_file_path()
    
    print("Destination folder:" + dest_folder)

    # iterates through all files in folder
    print("Note: There may or may not be photos that do not get cropped, \
            a list of file names will be printed at the end if this happens ")
    
    main(dest_folder)