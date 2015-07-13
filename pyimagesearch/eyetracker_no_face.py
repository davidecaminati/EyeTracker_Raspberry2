# import the necessary packages
import cv2

class Eyetracker_no_face:
    def __init__(self, eyeCascadePath):
        # load the face and eye detector
        
        self.eyeCascade = cv2.CascadeClassifier(eyeCascadePath)
    
    def track(self, image, minSize = (50, 50)):
        # detect faces in the image and initialize the list of
        # rectangles containing the faces and eyes
        # detect eyes in the face ROI
        rects = []
        eyeRects = self.eyeCascade.detectMultiScale(image,
            scaleFactor = 1.2, minNeighbors = 10, minSize = minSize,
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    
        # loop over the eye bounding boxes
        for (eX, eY, eW, eH) in eyeRects:
            # update the list of boounding boxes
            rects.append(
                ( eX, eY,eX + eW, eY + eH))
    
        # return the rectangles representing bounding
        # boxes around the faces and eyes
        return rects