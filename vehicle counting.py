from typing import Counter
import cv2
import numpy as np
from numpy.core.fromnumeric import shape
#vid capture
cap = cv2.VideoCapture('video.mp4')
min_width_rect = 80 #min width
min_height_rect = 70 #min height

count_line_position = 550
# initialize subtractor
algo=cv2.createBackgroundSubtractorMOG2()
def centre_handel(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx,cy
detect = []    
offset = 6 #allowable error between pixel
Counter = 0





    

while True :
    ret, frame1 = cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    #Applying on each frame
    img_sub = algo.apply(blur)
    dilate = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatedata = cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)
    dilatedata = cv2.morphologyEx(dilatedata,cv2.MORPH_CLOSE,kernel)
    countershape,h = cv2.findContours(dilatedata,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)
    for (i,c) in enumerate(countershape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_rect) and (h>=min_height_rect)
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        centre = centre_handel(x,y,w,h)
        detect.append(centre)
        cv2.circle(frame1,centre,4,(0,0,255),-1)
        for (x,y) in detect:
            if y<(count_line_position + offset) and y>(count_line_position - offset):
                Counter +=1
            cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
            detect.remove((x,y))
            print ('Vehicle Counter:'+str(Counter))


    cv2.cv2.putText(frame1,'Vehicle Counter:'+str(Counter),(450,70),cv2.cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)        

    
    
    #cv2.imshow('Detector',dilatedata)

    cv2.imshow("video original",frame1)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()
