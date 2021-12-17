import cv2
import numpy as np
import math
from object_detection import ObjectDetection
od=ObjectDetection()
cap = cv2.VideoCapture("los_angeles.mp4")
#Initialize Count
Count = 0
centre_points_prev_frame=[]
tracking_objects={}
track_id=0

while True :
    ret, frame = cap.read()
    Count +=1
    if not ret:
        break
    # point current frame
    centre_curr_points = []


    #detect objects on frame
    (class_ids,scores,boxes)=od.detect(frame)
    for box in boxes:
        print(box)
        (x,y,w,h)=box
        cx = int((x+x+w)/2)
        cy = int((y+y+h)/2)
        centre_curr_points.append((cx,cy))
        #print("FRAME NO",Count," ",x,y,w,h)
        #cv2.circle(frame,(cx,cy) , 5 , (0,0,255), -1)
        cv2.rectangle(frame,(x,y),(x+w ,y+h),(0,255,0),2)
        #only at the beginning we compare the current and previous frame
    if Count<=2:
        
        for pt in centre_curr_points:
         for pt2 in  centre_points_prev_frame:
            distance=math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
            if distance<20:
                tracking_objects[track_id]=pt
                track_id += 1
    else:

        tracking_objects_copy=tracking_objects.copy()
        centre_curr_points_copy=centre_curr_points.copy()
        for object_id, pt2 in tracking_objects_copy.items():
            object_exists=False
            for pt in centre_curr_points:
                distance=math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                #Update Ids Position
                if distance<20:
                    tracking_objects[object_id]=pt
                    object_exists=True
                    if pt in centre_curr_points:
                     centre_curr_points.remove(pt)
                    continue
            #Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)
    #Add New IDs found
    for pt in centre_curr_points :
         tracking_objects[track_id]=pt
         track_id +=1


    for object_id,pt in  tracking_objects.items():
        cv2.circle(frame,pt , 5 , (0,0,255),-1)
        cv2.putText(frame , str(object_id),(int(abs(pt[0])),int(abs(pt[1]))-7),0,1,(0,0,255),2)

    print("Tracking objects")
    print(tracking_objects)

    print("CURR POINTS LEFT")
    print(centre_curr_points)
    print("PREV FRAME")
    print(centre_points_prev_frame)

    cv2.imshow("Frame",frame)
    #Make a copy of the frame
    centre_points_prev_frame=centre_curr_points.copy()
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()