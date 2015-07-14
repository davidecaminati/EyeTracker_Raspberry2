#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv

from multiprocessing.pool import ThreadPool
from video import create_capture
from common import clock, draw_str

from pyfirmata import Arduino, util

ArduinoPresent = False

if ArduinoPresent :
    board = Arduino('/dev/ttyACM0')
#board.digital[2].write(1)
#board.digital[4].write(1)


help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''
minsize_occhi = 60


def rotateImage(image, angle):
    row,col = image.shape
    center=tuple(np.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image
    
    
    
    
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4, minSize=(minsize_occhi, minsize_occhi), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt
    
    #print help_message
    

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    #cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_frontalface_alt.xml")
    #nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")
    cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_eye.xml")
    #nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    #nested = cv2.CascadeClassifier(nested_fn)

    cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
    numero = 0
    while True:
        ret, img = cam.read()
        #gray = img[200:400,100:400]
        #gray = img[100:300,100:300]
        gray = img[100:400,100:500]
        
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        

        t = clock()
        rects = detect(gray, cascade)
        vis = gray.copy()
       
        draw_rects(vis, rects, (0, 255, 0))
        if ArduinoPresent:
            board.digital[4].write(0)    
            board.digital[2].write(0)
        for x1, y1, x2, y2 in rects:
            #roi = gray[y1:y2, x1:x2]
            #vis_roi = vis[y1:y2, x1:x2]
            
            numero = numero + 1
            larghezza = x2-x1
            altezza = y2-y1
            '''
            if x1 >= 150: #dx
                if ArduinoPresent:
                    board.digital[2].write(1)
                dx = cv2.getRectSubPix(vis, (larghezza, altezza),(x1+larghezza/2,y1+altezza/2))
                cv2.imshow('dx', dx)
            '''

            if ArduinoPresent:
                board.digital[4].write(1)
            sx = cv2.getRectSubPix(vis, (larghezza, altezza),(x1+larghezza/2,y1+altezza/2))
            
            #edges = cv2.Canny(sx,100,300)
            #cv2.imshow('sx', edges)
            
            cv2.imshow('sx', sx)
            

            #file = "/home/pi/opencv-2.4.10/samples/python2/occhi/test_image" + str(numero) + ".png"
            
            
            # A nice feature of the imwrite method is that it will automatically choose the
            # correct format based on the file extension you provide. Convenient!
            #cv2.imwrite(file, sx)
            
            
            #subrects = detect(roi.copy(), nested)
            #draw_rects(vis_roi, subrects, (255, 0, 0))
            
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()
