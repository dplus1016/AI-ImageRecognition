import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

tips=[4,8,12,16,20]  # 추가-1

with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    flag=0  # 추가-2
    if results.multi_hand_landmarks:
      #--추가-3---
      flag=1
      posList=[]
      cnt=0
      direction=0
      #--추가-3---

      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        
        #--추가-4------------------------------------------------------------------------------
        pos=hand_landmarks.landmark
        if pos[tips[0]].x*(1-direction*0.5) < pos[tips[4]].x*(1-(1-direction)*0.1): direction=1
        
        # 엄지
        if pos[tips[0]-direction].x > pos[tips[0]-(1-direction)].x: cnt+=1

        # 나머지 손가락
        for i in range(1,5):
            if pos[tips[i]].y < pos[tips[i]-2].y: cnt+=1
        
    image = cv2.flip(image, 1)

    if flag: cv2.putText(image, str(cnt), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (140, 65, 217), 20)
        #--추가-4------------------------------------------------------------------------------
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands',image)  # 변형
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
