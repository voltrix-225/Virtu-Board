"""
Welcome To VirtuBoard, a Board for the future.
use your fingers to make your ideas into a reality.

code_author: Voltrix_04

"""

import cv2
import mediapipe as mp
import numpy as np
from math import *


mphands = mp.solutions.hands   #used to track hands

cap = cv2.VideoCapture(0)
cap.set(3, 1280)#SET WIDTH
cap.set(4, 720)#SET HEIGHT


hands = mphands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)


canvas = np.zeros((720,1280,3), dtype=np.uint8)
#canvas resizes to (1280,720)

pen_color = None
prev_x, prev_y = None, None

while True:  #all logic and lines, ie tracking hand movement under this
               
    data,image = cap.read()    #calls webcam func
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_RGB2BGR)
    #this will flip the img, ie give a selfie view
    results = hands.process(image)   #store the results

    cv2.putText(canvas,"Welcome to VirtuBoard | Glide Index Finger to Write",(0,650),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
    cv2.putText(canvas,"Select Pen Color | 'W': White | 'B' : Blue | 'R' : Red | 'G' : Green",(0,675),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
    cv2.putText(canvas,"Use Index and Middle Fingers to Move Cursor | Press 'C' to Clear Board | Press 'ESC' to Exit ",(0,700),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
    #(frame,txt,position,font,font_scale,color,thickness)




    if results.multi_hand_landmarks:  #checks if result has any landmark features and interconnect landmarks 
        for hand_landmarks  in results.multi_hand_landmarks:
            """mp_drawing.draw_landmarks(
                image,
                hand_landmarks,mphands.HAND_CONNECTIONS)  """ #this removes the landmark connection lines. reccomended to keep them in this code and remove in final
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True
        index_finger_tip = hand_landmarks.landmark[8]
        results = hands.process(image)
        image_height, image_width, _ = image.shape
        image.flags.writeable = True
    
        height, width, _ = image.shape
        ind_x = int(index_finger_tip.x * width)
        ind_y = int(index_finger_tip.y * height)
        

        middle_finger_tip = hand_landmarks.landmark[12] #posi of middle fingertip
        height, width, _ = image.shape
        mid_x = int(middle_finger_tip.x * width)
        mid_y = int(middle_finger_tip.y * height)
    
        cv2.circle(image, (ind_x,ind_y),10, (0,0,255), -1)
        cv2.circle(image, (mid_x,mid_y), 10, (0,255,0), -1)
       
        finger_dist = abs((sqrt(( mid_x - ind_x)**2)-((mid_y - ind_y)**2))) 
        
    
        
        if (finger_dist<=6000): #arbitary value telling dist between ind and mid finger
            prev_x, prev_y = None, None
        
        else:
            cv2.line(canvas, (prev_x, prev_y), (ind_x, ind_y), pen_color, 20)
                    #(canvas, prev_coords, curr_coords, pencolor, thickness)
        
        prev_x, prev_y = ind_x , ind_y

    
    image = cv2.addWeighted(image, 0.5, canvas, 1, 0)
                        #(CANVAS,ALPA(WT OF CANVAS),IMAGE,BETA(WT OF CAM FEED),CHANNELS)
    
    cv2.imshow('VirtuBoard-The Board of the Future',image)

    k = cv2.waitKey(10)
    if k == ord('c'):
        canvas=np.zeros((720,1280,3), dtype = np.uint8)
    
    elif k == ord('b') or k==ord('B'):
         pen_color = (255,0,0)
    
    elif k == ord('g') or k== ord('G'):
         pen_color = (0,255,0)
    
    elif k == ord('r') or k == ord('R'):
         pen_color = (0,0,255)

    elif k == ord('w') or k==ord('W'):
         pen_color = (255,255,255)

    elif k %256 == 27:
         break
    
cap.release()  #closes the camera

cv2.destroyAllWindows()   #closes the window, good practice
   



    