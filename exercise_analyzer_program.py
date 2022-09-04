import cv2
from mediapipe import *
from math import *

class exercise_analyzer:
    def __init__(self,static_image_mode=False,model_complexity=1,
                 smooth_landmarks=True,min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode=static_image_mode
        self.model_complexity=model_complexity
        self.smooth_landmarks=smooth_landmarks
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        self.mp_drawing = python.solutions.drawing_utils
        self.mppose = python.solutions.pose.Pose(self.static_image_mode,
                                                 self.model_complexity,
                                                 self.smooth_landmarks,
                                                 self.min_detection_confidence,
                                                 self.min_tracking_confidence)
        
    def detect_pose(self,img,draw=True):
        # the BGR image to RGB.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        self.results = self.mppose.process(img)
        # Draw the pose annotations on the image.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if(self.results.pose_landmarks):
            self.h=1
            if(draw):
                self.mp_drawing.draw_landmarks(img,self.results.pose_landmarks,python.solutions.pose.POSE_CONNECTIONS)
        else:
            self.h=0
            print('woman is not detected')
        return img
    
    def exercise(self,img):
        if(self.results.pose_landmarks):
            for index_no_lm,location_lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, no_channels = img.shape
                if(index_no_lm==17): # 17 : left pinky
                    xc1=int(location_lm.x*w)
                    yc1=int(location_lm.y*h)
                if(index_no_lm==18): # 18 : right pinky
                    xc2=int(location_lm.x*w)
                    yc2=int(location_lm.y*h)
                if(index_no_lm==23): # 23 : left hip
                    x_c1=int(location_lm.x*w)
                    y_c1=int(location_lm.y*h)
                if(index_no_lm==25): # 25 : left knee
                    x_c2=int(location_lm.x*w)
                    y_c2=int(location_lm.y*h)
                if(index_no_lm==24): # 24 : right hip
                  c1_x=int(location_lm.x*w)
                  c1_y=int(location_lm.y*h)
                if(index_no_lm==26): # 26 : right knee
                  c2_x=int(location_lm.x*w)
                  c2_y=int(location_lm.y*h)
            c_x1,c_y1=(x_c1+x_c2)//2,(y_c1+y_c2)//2
            c_x2,c_y2=(c1_x+c2_x)//2,(c1_y+c2_y)//2
            if(y_c2<c_y2):
                hln=True
            else:
                hln=False
            if(c2_y<c_y1):
                hrn=True
            else:
                hrn=False
            if(yc1>c2_y):
                rtt=1
            else:
                rtt=0
            if(yc2>y_c2):
                ltt=1
            else:
                ltt=0
        return hln,hrn,rtt,ltt       
    
def main():
    ea=exercise_analyzer()
    vc = cv2.VideoCapture('toe touch exercise.mp4')
    while(True):
        retval,img=vc.read()
        if(not retval):
          break
        img=ea.detect_pose(img,draw=False)
        hln,hrn,rtt,ltt=ea.exercise(img)
        if(hln):
            img=cv2.putText(img,'LEFT KNEE UP',(5,30),0,1,(0,0,255),2)
        else:
            img=cv2.putText(img,'LEFT KNEE DOWN',(5,30),0,1,(0,0,255),2)
        if(hrn):
            img=cv2.putText(img,'RIGHT KNEE UP',(5,60),0,1,(0,0,255),2)
        else:
            img=cv2.putText(img,'RIGHT KNEE DOWN',(5,60),0,1,(0,0,255),2)
        if(rtt):
            img=cv2.putText(img,'RIGHT TOE TOUCH',(5,90),0,1,(0,0,255),2)
        else:
            img=cv2.putText(img,'NO RIGHT TOE TOUCH',(5,90),0,1,(0,0,255),2)
        if(ltt):
            img=cv2.putText(img,'LEFT TOE TOUCH',(5,120),0,1,(0,0,255),2)
        else:
            img=cv2.putText(img,'NO LEFT TOE TOUCH',(5,120),0,1,(0,0,255),2)
        cv2.imshow('MediaPipe Hands', img)
        k=cv2.waitKey(1)
        if(k==ord('q')): # press 'q' key to quit
            break
    vc.release()
    cv2.destroyAllWindows()
if(__name__=='__main__'):
    main()
