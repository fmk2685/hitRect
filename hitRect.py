#coding=utf-8
import cv2
import random as rr

'''
方塊錨點：左上方
方塊照光判定點：方塊中心
'''
cap = cv2.VideoCapture(0) #使用0號攝像頭(也就是內建攝像頭)，想要使用外接攝像頭可以改成1或更高的數字，接幾個攝像頭就多幾個可選數字
print '您預設的攝像頭預設解析度為：', (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #設定影像解析度為640 x 480，可自行調整，若刪除這兩行就是使用攝像頭預設解析度 (解析度低一點會比較快)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#若攝像頭不支持640 x 480解析度則會保持預設解析度，也能玩
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print '解析度已更改為：', (height, width)
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
while True:
    size = input('請輸入為「正整數及偶數」的正方形方塊的邊長(建議20～30之間)：')
    if size>0 and size==int(size) and int(size)%2==0:
        size = int(size) #強迫症，讓型別一定為int，XDDD
        break
n_max = min(height, width) / size #在 height x width 的解析度下，比較短的一軸最多只能以size為步進單位(避免方塊彼此重疊)隨機取n_max個座標
#其實要避免方塊彼此重疊有更好的方法，不過這是最簡單方便的
while True:
    n = input('請輸入1～'+str(n_max)+'的方塊出現個數初始值(正整數)：')
    if n>0 and n<=n_max and n==int(n):
        n = int(n) #強迫症
        break
while True:
    rect_time = input('請輸入正整數的方塊出現間隔時間初始值(微秒)：') #方塊接連出現的間隔時間，例如輸入500代表500微秒(0.5秒)，實際速度可能依不同電腦有不同結果
    if rect_time>0 and rect_time==int(rect_time):
        rect_time = int(rect_time) #強迫症
        rect_time_0 = rect_time #rect_time_0用來記錄rect_time的初始值，很後面會用到
        break
light_thr = 245 #照光亮度判定閥值，預設245(亮度範圍為0~255，越高越亮)
T = 0 #記錄答題正確次數
F = 0 #記錄答題錯誤次數
F_key = 0 #答題錯誤會暫時變為1，用於判斷式
end_key = 0 #選擇退出會變為1，用於break出多重迴圈
ret, frame = cap.read() #讀取攝像頭影像
frame = cv2.flip(frame, 1, dst=None) #實際手的移動方向會和影像中相反，cv2.flip()將影像水平反轉以達到螢幕鏡像效果
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #frame是用來顯示的彩色圖，frame_gray是用來計算的灰階圖(灰階圖計算較快)
print '\n遊戲視窗可調整大小，遊戲中可用「p q a w s e d」七個按鍵來調整參數及退出' #按鍵功能請看尾段註釋或README.md  #遊戲視窗可調整大小，但建議不要拉太大，電腦畫圖會變吃力，影像會變比較卡
print '照亮中間的方塊開始遊戲'
while (frame_gray[height/2][width/2] <= light_thr):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1, dst=None)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(frame, ((width/2)-(size/2),(height/2)-(size/2)), ((width/2)+(size/2),(height/2)+(size/2)), (255,255,255), 4) #在螢幕中央畫個空心方塊，對它照光即開始遊戲
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
for i in range(3, 0, -1):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1, dst=None)
    cv2.putText(frame, str(i), ((width/2)-20, (height/2)+20), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 255), 10, cv2.LINE_AA)
    cv2.imshow('Video', frame)
    cv2.waitKey(1000)

print '亮度判定閥值='+str(light_thr), ', 方塊出現個數='+str(n), ', 方塊出現間隔時間='+str(rect_time)+'微秒'
print 'True :', str(T), ', False :', str(F) #print出答題正確和錯誤的次數

while True: #以下直到下個while前，為方塊接連出現階段
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1, dst=None)
    rect_ij = zip(rr.sample(range(0,height-size+1,size),n), rr.sample(range(0,width-size+1,size),n)) #rect_ij用來記錄所有方塊的「左上角點」的座標，以size為步進單位(避免方塊彼此重疊)隨機取n個i和j座標並放在一起。
    #rect_ij示意：[(i1,j1), (i2,j2), (i3,j3), ...]，i座標相當於y座標(向下為正)，j座標相當於x座標(向右為正)
    #記錄方塊「左上角點」只是為了方便操作矩陣，照光判定點是在方塊的正中央
    for rect in rect_ij: #將實心方塊接連畫出來
        frame[rect[0]:rect[0]+size, rect[1]:rect[1]+size] = [255,255,255]
        cv2.imshow('Video', frame)
        cv2.waitKey(rect_time) #此行關係到方塊接連出現的間隔時間
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1, dst=None)
    for rect in rect_ij: #畫完後把全部方塊變為空心，空心代表「等待照光」
        cv2.rectangle(frame, (rect[1],rect[0]), (rect[1]+size,rect[0]+size), (255,255,255), 4)
    cv2.imshow('Video', frame)
    cv2.waitKey(1)
    rect_ij_true = [] #rect_ij_true用來記錄已經在正確順序下照光過的方塊座標
    while True: #以下while為方塊出現完後的照光階段
        if not rect_ij:
            T += 1
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1, dst=None)
            cv2.circle(frame, (width/2,height/2), 160, (255,255,255), thickness=15) #答題正確畫出圈圈
            cv2.imshow('Video', frame)
            cv2.waitKey(500) #圈圈出現時間
            break
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1, dst=None)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for rect in rect_ij[1:]: #檢查照光順序是否錯誤，該照的是rect_ij[0]的座標，照其他的都是錯
            if frame_gray[rect[0]+(size/2)][rect[1]+(size/2)] > light_thr:
                F += 1
                F_key =1
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1, dst=None)
                cv2.line(frame, ((width/2)-150, (height/2)-150), ((width/2)+150, (height/2)+150), (255,255,255), 15) #以下兩行為：答題錯誤畫出叉叉
                cv2.line(frame, ((width/2)+150, (height/2)-150), ((width/2)-150, (height/2)+150), (255,255,255), 15)
                cv2.imshow('Video', frame)
                cv2.waitKey(500) #叉叉出現時間
                break
        if F_key:
            F_key = 0
            break
        if frame_gray[rect_ij[0][0]+(size/2)][rect_ij[0][1]+(size/2)] > light_thr: #檢查該照光的rect_ij[0]的座標是否照光，若有照光則執行以下兩行
            rect_ij_true.append(rect_ij[0]) #在rect_ij_true加入此時rect_ij[0]的座標
            del rect_ij[0] #刪除rect_ij[0]，rect_ij[1]遞補上來成為rect_ij[0]
        for rect in rect_ij: #將rect_ij中紀錄的，也就是還未照光的方塊以空心方塊的圖形畫出
            cv2.rectangle(frame, (rect[1],rect[0]), (rect[1]+size,rect[0]+size), (255,255,255), 4) #畫空心方塊
        for rect in rect_ij_true: #將rect_ij_true中紀錄的，也就是已經以正確順序照光的方塊以實心方塊的圖形畫出
            frame[rect[0]:rect[0]+size, rect[1]:rect[1]+size] = 255 #畫實心方塊
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF #在所有方塊都已經出現並等待你照光時，會讀取鍵盤按下的按鍵
        #以下為調整參數及退出用的按鍵，可自行設定 (注意：有分大小寫且一定要英文輸入法、接收按鍵的是遊戲視窗而不是Terminal等等的東西)
        if key == ord('p'): #按下「p」會結束程序
            end_key = 1
            break
        elif key == ord('q'):  #按下「w」會提升照光亮度判定閥值，照光反應更不靈敏
            light_thr += 1
            if light_thr > 254: light_thr = 254
            print '亮度判定閥值='+str(light_thr)
        elif key == ord('a'): #按下「s」會降低照光亮度判定閥值，照光反應更靈敏
            light_thr -= 1
            if light_thr < 1: light_thr = 1
            print '亮度判定閥值='+str(light_thr)
        elif key == ord('w'): #按下「w」會增加方塊出現個數，在下一輪出現的方塊才會改變數量
            n += 1
            if n > n_max: n = n_max
            print '方塊出現個數='+str(n)
        elif key == ord('s'): #按下「s」會減少方塊出現個數，在下一輪出現的方塊才會改變數量
            n -= 1
            if n <1: n = 1
            print '方塊出現個數='+str(n)
        elif key == ord('e'): #按下「e」會增加方塊出現間隔時間
            if rect_time != 1:
                rect_time += 20
            else:
                rect_time = ((rect_time_0-1)%20)+1
            print '方塊出現間隔時間='+str(rect_time)+'微秒'
        elif key == ord('d'): #按下「d」會減少方塊出現間隔時間
            rect_time -= 20
            if rect_time < 1: rect_time = 1
            print '方塊出現間隔時間='+str(rect_time)+'微秒'
    if end_key:
        break
    print 'True :', str(T), ', False :', str(F)
cap.release()
cv2.destroyAllWindows()