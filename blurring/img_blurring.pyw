from tkinter import *
import tkinter.messagebox as msg
import os
import numpy as np
import cv2

temp = "" # 전역 변수
path = "./" # 최초 폴더내 파일 읽기를 위한 경로
count = 0 # blurred_[count]_이름
name = ''

# Blurring 함수
def blur(num):
    global count, name
    li = os.listdir(path)
    if count == 0:
        count += 1
        for l in li:
            if not ".py" in l:
                img = cv2.imread(l)
                kernel = np.ones((5,5),np.float32)/25
                dst = cv2.filter2D(img, -1, kernel)
                cv2.imwrite('blurred_'+str(count)+'_'+l, dst)
                name = l
    
    else:
        img = cv2.imread('blurred_'+str(count)+'_'+name)
        count += 1
        kernel = np.ones((5,5),np.float32)/25
        dst = cv2.filter2D(img, -1, kernel)
        cv2.imwrite('blurred_'+str(count)+'_'+name, dst)

# 아래는 tkinter

win = Tk()
win.title("Blurring")
win.geometry("250x80")
win.resizable(False, False)

# 입력 지시문 라벨 설정
lab = Label(win)
lab['text'] = '블러링할 수치를 입력'
lab.pack()


# 입력창 설정
ent = Entry(win)
ent.pack()

# 버튼 클릭시 실행할 함수
def click():
    global temp
    temp = int(ent.get())
    for i in range(temp):
        blur(temp)

    # 1. 완료 알림
    msg.showinfo("Alarm", "정상 완료")
    
    # 2. 그리고 tkinter 종료
    win.destroy()

# <입력> 버튼 생성
btn = Button(win, text="입력", command=click)
btn.pack() # 한번에 ~Button(win, text="입력", command=click).pack()~으로 가능

# tkinter main 루프
win.mainloop()
