#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv

from video import create_capture
import os
import sys
from common import mosaic, clock, draw_str

from digits import *

from common import clock, draw_str

minsize_occhi = 100

'''
def rotateImage(image, angle):
    row,col = image.shape
    center=tuple(np.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image
'''    
    
    
    
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4, minSize=(minsize_occhi, minsize_occhi), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def set_res(cap, x,y):
    cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    
def main():
    import sys, getopt
    try: src = sys.argv[1]
    except: src = 0
    
    cap = cv2.VideoCapture('1.avi')
    while(cap.isOpened()):
        #cap = create_capture(src)
        
        classifier_fn = 'digits_svm.dat'
        if not os.path.exists(classifier_fn):
            print '"%s" not found, run digits.py first' % classifier_fn
            return
        model = SVM()
        model.load(classifier_fn)
        
        args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
        
        args = dict(args)
        #cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_frontalface_alt.xml")
        #nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")
        cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_eye.xml")
        #nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")
    
        cascade = cv2.CascadeClassifier(cascade_fn)
        #nested = cv2.CascadeClassifier(nested_fn)
    
    
        cascade = cv2.CascadeClassifier("../../data/haarcascades/haarcascade_eye.xml")
    
        

        
        #set_res(cap,160,120)
        #set_res(cap,176,144)
        #set_res(cap,320,240)
        #set_res(cap,352,288)
        #set_res(cap,640,480)
        #set_res(cap,1024,768)
        #set_res(cap,1280,1024)
        

        ret, frame = cap.read()
        
        
        #gray = frame[1:300,1:300]
        gray = frame
        
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        # CV

        gray = cv2.equalizeHist(gray)
        rects = detect(gray, cascade)

        t = clock()
        #rects = detect(gray, cascade)
        vis = gray.copy()
        
        
        #draw_rects(vis, rects, (0, 255, 0))
        #print "rettangolo " + str(len(rects))
        for x1, y1, x2, y2 in rects:
            #roi = gray[y1:y2, x1:x2]
            #vis_roi = vis[y1:y2, x1:x2]
            
            #larghezza = x2-x1
            #altezza = y2-y1
            larghezza = 150
            altezza = 150
            
            
        
            sx = cv2.getRectSubPix(vis, (larghezza, altezza),(x1+larghezza/2,y1+altezza/2))
            cv2.imshow('sx', sx)
            # fine CV  
            bin = cv2.adaptiveThreshold(sx, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 10)
            #bin = cv2.adaptiveThreshold(sx, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 10)
            bin = cv2.medianBlur(bin, 3)
            
            cv2.imshow('bin', bin)
            contours, heirs = cv2.findContours( bin.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            try: heirs = heirs[0]
            except: heirs = []

            for cnt, heir in zip(contours, heirs):
                _, _, _, outer_i = heir
                if outer_i >= 0:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                #if not (56 <= h <= 150  and w <= 1.2*h):
                if not (40 <= h <= 350):
                    continue
                pad = max(h-w, 0)
                x, w = x-pad/2, w+pad
                cv2.rectangle(sx, (x, y), (x+w, y+h), (0, 255, 0))

                bin_roi = bin[y:,x:][:h,:w]
                #gray_roi = sx[y:,x:][:h,:w]

                m = bin_roi != 0
                #if not 0.1 < m.mean() < 0.4:
                if not 0.1 < m.mean() < 0.4:
                    continue
                
                #v_in, v_out = gray_roi[m], gray_roi[~m]
                #if v_out.std() > 10.0:
                #    continue
                #s = "%f, %f" % (abs(v_in.mean() - v_out.mean()), v_out.std())
                #cv2.putText(frame, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (200, 0, 0), thickness = 1)
                

                s = 1.5*float(h)/SZ
                m = cv2.moments(bin_roi)
                c1 = np.float32([m['m10'], m['m01']]) / m['m00']
                c0 = np.float32([SZ/2, SZ/2])
                t = c1 - s*c0
                A = np.zeros((2, 3), np.float32)
                A[:,:2] = np.eye(2)*s
                A[:,2] = t
                bin_norm = cv2.warpAffine(bin_roi, A, (SZ, SZ), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
                bin_norm = deskew(bin_norm)
                #if x+w+SZ < frame.shape[1] and y+SZ < frame.shape[0]:
                #    frame[y:,x+w:][:SZ, :SZ] = bin_norm[...,np.newaxis]

                sample = preprocess_hog([bin_norm])
                digit = model.predict(sample)[0]
                print str(digit)
                if str(digit) == "0.0":
                    print "centro"
                if str(digit) == "1.0":
                    print "sinistra"
                if str(digit) == "2.0":
                    print "destra"
                    
                    

                #cv2.putText(frame, '%d'%digit, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (200, 0, 0), thickness = 1)


            #cv2.imshow('frame', frame)
                    
                    
                    
                        
                        
                        
                            
                #dt = clock() - t
    
                #draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
                
                #cv2.imshow('facedetect', vis)
    
            #if 0xFF & cv2.waitKey(5) == 27:
            #    break
            #gray = cv2.getRectSubPix(vis, (larghezza, altezza),(pos_x1+larghezza/2,pos_y1+altezza/2))
            
            
            #cv2.imshow('bin', bin)
            ch = cv2.waitKey(1)
            if ch == 27:
                break

if __name__ == '__main__':
    main()
