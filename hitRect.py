#coding=utf-8
import cv2
import numpy
import random as rr

'''
設定影像尺寸：640 x 480
方塊尺寸：20 x 20
方塊錨點：左上方
錨點出現範圍：左上算起 [0:460, 0:620]
'''
cap = cv2.VideoCapture(0)
#print (cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)), '>>',
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#print (cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
n = input('請輸入1～24的方塊出現個數：')
rect_i = rr.sample(range(0,461,20),n)
rect_j = rr.sample(range(0,621,20),n)
rect_ij = [[rect_i[g], rect_j[g]]for g in range(n)]
T = 0
F = 0
F_key = 0
end_key = 0
ret, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame = cv2.flip(frame, 1, dst=None)
while (frame[240][320]<200):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1, dst=None)
    cv2.rectangle(frame, (320-10,240-10), (320+10,240+10), (255,255,255), 4)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
for i in range(3, 0, -1):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1, dst=None)
    cv2.putText(frame, str(i), (300, 260), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 10, cv2.LINE_AA)
    cv2.imshow('Video', frame)
    cv2.waitKey(1000)

print 'True :', str(T), ', False :', str(F)

while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1, dst=None)
    rect_i = rr.sample(range(0,461,20),n)
    rect_j = rr.sample(range(0,621,20),n)
    rect_ij = [[rect_i[g], rect_j[g]]for g in range(n)]
    for rect in rect_ij:
        frame[rect[0]:rect[0]+20, rect[1]:rect[1]+20] = 255
        cv2.imshow('Video', frame)
        cv2.waitKey(500)
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame, 1, dst=None)
    for rect in rect_ij:
        cv2.rectangle(frame, (rect[1],rect[0]), (rect[1]+20,rect[0]+20), (255,255,255), 4)
    cv2.imshow('Video', frame)
    cv2.waitKey(1)
    rect2_ij = [] #以下的While中，實心Rect，rect_ij則是空心
    while True:
        if not rect_ij:
            T += 1
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.flip(frame, 1, dst=None)
            cv2.circle(frame, (320,240), 160, (255,255,255), thickness=15)
            cv2.imshow('Video', frame)
            cv2.waitKey(500)
            break
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 1, dst=None)
        for rect in rect_ij[1:]:
            if frame[rect[0]][rect[1]] > 200:
                F += 1
                F_key =1
                ret, frame = cap.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.flip(frame, 1, dst=None)
                cv2.line(frame, (170, 90), (470, 390), (255,255,255), 15)
                cv2.line(frame, (470, 90), (170, 390), (255,255,255), 15)
                cv2.imshow('Video', frame)
                cv2.waitKey(500)

                break
        if F_key:
            F_key = 0
            break
        if frame[rect_ij[0][0]][rect_ij[0][1]] > 200:
            rect2_ij.append(rect_ij[0])
            del rect_ij[0]
        for rect in rect_ij: #畫空心Rect
            cv2.rectangle(frame, (rect[1],rect[0]), (rect[1]+20,rect[0]+20), (255,255,255), 4)
        for rect in rect2_ij: #畫實心Rect
            frame[rect[0]:rect[0]+20, rect[1]:rect[1]+20] = 255
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            end_key = 1
            break
    if end_key:
        break
    print 'True :', str(T), ', False :', str(F)
cap.release()
cv2.destroyAllWindows()