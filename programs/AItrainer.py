import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose=mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

count = 0
dir = 0
pTime = 0

def findPose(image):
    image.flags.writeable = False
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    image.flags.writeable = True
    return results


def findPosition(results):
    List=[]    
    if results.pose_landmarks:
        for id, pos in enumerate(results.pose_landmarks.landmark):
            h,w,_=image.shape
            cx,cy=int(pos.x*w), int(pos.y*h)
            List.append([id, cx, cy])
    return List
    

def calAngleDraw(image, List, i1, i2, i3):
    x1,y1=List[i1][1:]
    x2,y2=List[i2][1:]
    x3,y3=List[i3][1:]

    angle=math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
    if angle<0: angle+=360

    cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(image, (x3, y3), (x2, y2), (255, 255, 255), 3)
    cv2.circle(image, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(image, (x1, y1), 15, (0, 0, 255), 2)
    cv2.circle(image, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, (0, 0, 255), 2)
    cv2.circle(image, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(image, (x3, y3), 15, (0, 0, 255), 2)
    cv2.putText(image, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    return angle

    
while True:
    success, image = cap.read()
    
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    image = cv2.resize(image, (1280, 980))
    results = findPose(image)
    List = findPosition(results)
    
    if len(List) != 0:
        # Right Arm
        angle=calAngleDraw(image, List, 12, 14, 16)
        
        # Left Arm
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
 
        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
 
        # Draw Bar
        cv2.rectangle(image, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(image, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(image, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
 
        # Draw Curl Count
        cv2.rectangle(image, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)
        
    # 키보드 조작
    if cv2.waitKey(1) & 0xFF == ord('q'): break  # q: 종료
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
 
    cv2.imshow("Image", image)
    
cv2.destroyAllWindows()
