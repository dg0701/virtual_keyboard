import cv2
from cvzone.HandTrackingModule import HandDetector 
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8) #0.8 is for index finger
keys = [['1','2','3','4','5','6','7','8','9','0',"<"],
        ["Q", "W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"],
        ["_"]]
finalText = ""
def drawAll(img,buttonList) :
    for button in buttonList : 
        x,y = button.pos
        w,h = button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,255),-1)
        cv2.putText(img,button.text,(x+15,y+55),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),5)
    return img

class Button() : 
    def __init__(self,pos,text,size=[80,80]) : 
        self.pos = pos
        self.text = text
        self.size=size
        
buttonList = []
for i in range (len(keys)) : 
        for x, key in enumerate(keys[i]) :
            buttonList.append(Button([100*x +50 , 100*i +50],key))
while True : 
    success, img = cap.read()
    hands, img = detector.findHands(img,draw=True)
    
    img = drawAll(img,buttonList)
    if hands : 
        lmList = hands[0]['lmList'] if hands else []
        if lmList : 
            for button in buttonList :
                x,y = button.pos
                w,h = button.size
                if x<=lmList[8][0]<x+w and y<=lmList[8][1]<y+h:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),-1)
                    cv2.putText(img,button.text,(x+15,y+55),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),5)
                    l,_,_ = detector.findDistance(lmList[8][:2],lmList[4][:2],img)
                    #when clicked
                    if l<30 :
                        if button.text == "<" :
                            finalText = finalText[:-1]
                        elif button.text == "_" :
                            finalText+=" "  
                        else :
                            cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),-1)
                            cv2.putText(img,button.text,(x+15,y+55),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),5)            
                            finalText += button.text
                        sleep(0.5)
    cv2.rectangle(img,(58,558),(788,658),(175,0,175),-1)
    cv2.putText(img,finalText,(68,638),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5)
               
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()