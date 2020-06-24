import numpy as np
import cv2
import time

def nothing(x):
    pass

#Open the Camera
cap=cv2.VideoCapture(0)
#Time for the camera to warm-up a bit
time.sleep(3)

background=0
#Storing the background
for i in range(30):
    ret,background=cap.read()

#Laterally Inverting/Flipping the background
background=np.flip(background,axis=1)      
  
cv2.namedWindow("colour")
#Creating the trackbars
cv2.createTrackbar('LowHue','colour',0,179,nothing)
cv2.createTrackbar('HighHue','colour',179,179,nothing)
cv2.createTrackbar('LowSaturation','colour',0,255,nothing)
cv2.createTrackbar('HighSaturation','colour',255,255,nothing)
cv2.createTrackbar('LowValue','colour',0,255,nothing)
cv2.createTrackbar('HighValue','colour',255,255,nothing)

#Capturing the live feed
while(True):
    ret2,frame=cap.read()
    
    frame=np.flip(frame,axis=1)
    
    
    #get current position of trackbars 
    H_low=cv2.getTrackbarPos('LowHue','colour')
    S_low=cv2.getTrackbarPos('LowSaturation','colour')
    V_low=cv2.getTrackbarPos('LowValue','colour')
    H_high=cv2.getTrackbarPos('HighHue','colour')
    S_high=cv2.getTrackbarPos('HighSaturation','colour')
    V_high=cv2.getTrackbarPos('HighValue','colour')
    
    #convert to hsv colourspace
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_hsv=np.array((H_low,S_low,V_low))
    higher_hsv=np.array((H_high,S_high,V_high))
  
    #Applying the inRange method to create a mask
    mask=cv2.inRange(hsv, lower_hsv, higher_hsv)
    
    #Performing Morphological Operations on the Mask
    mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask=cv2.morphologyEx(mask, cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    
    #Creating an iverted mask to segment out the cloth from the frame
    mask1=cv2.bitwise_not(mask)
    #Segmenting the cloth out of the frame using bitwise and with the inverted mask
    result1=cv2.bitwise_and(frame,frame,mask=mask1)
    #Creating image showing static background frame pixels only for the masked region
    result2=cv2.bitwise_and(background,background,mask=mask)
    #Calculating the final image
    final_result=cv2.addWeighted(result1,1,result2,1,0)
    cv2.imshow("Bah Gawd", final_result)
    #Press esc to close
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break
    
    
cap.release()      
cv2.destroyAllWindows()
    