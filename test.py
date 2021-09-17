import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import os

path = "png"
pngs = os.listdir(path)


cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

det = HandDetector(detectionCon=0.65)

class Import_images():
    def __init__(self, path, pos):
        self.pos = pos
        self.path = path
        self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        self.size = self.img.shape[:2]
    def update(self, pointer):
        x, y = self.pos
        h, w = self.size
        if x < pointer[0] < x+w and y < pointer[1] < y+h:
                self.pos = pointer[0] - w // 2, pointer[1] - h//2
        

images = []
for count, image_name in enumerate(pngs):
    images.append(Import_images(f'{path}/{image_name}', [600 + count*400,100]))
print(len(images))

while True:
    _, frame = cap.read()
    
    hand, frame = det.findHands(frame, flipType=False)
    seconds = time.time()
    current_time = time.ctime(seconds)
    cv2.rectangle(frame, (10,10), (1900, 90) ,(64, 64, 64), -1)
    cv2.putText(frame,"Virtual Dashboard", (20,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (51, 153, 255), 4)
    cv2.putText(frame,str(current_time), (1050,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (51, 153, 255), 4)

    cv2.rectangle(frame, (10,150), (350, 500) ,(64, 64, 64), -1)
    cv2.putText(frame,"Projects", (20,190), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 153, 255), 4)
    cv2.putText(frame,"-> Cascade", (20,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 153, 255), 4)
    cv2.putText(frame,"-> Mercury", (20,350), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 153, 255), 4)
    cv2.putText(frame,"-> Massive Monkey", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 153, 255), 4)
    
    cv2.rectangle(frame, (1550,150), (1900, 750) ,(64, 64, 64), -1)
    cv2.putText(frame,"Statistics", (1560,190), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 153, 255), 4)
    
    
    if hand:
        land_marks = hand[0]['lmList']
        
        length, info, img = det.findDistance(land_marks[8], land_marks[12], frame)
        #print(length)
        
        if length < 45:
            pointer = land_marks[8]
            for obj in images:
                obj.update(pointer)
            
    try:
        for obj in images:
            x, y = obj.pos
            h, w = obj.size
            frame = cvzone.overlayPNG(frame, obj.img, [x, y])
    except:
        pass
    
    cv2.imshow("Live Feed", frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
