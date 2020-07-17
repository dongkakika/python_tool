from tkinter import *
from tkinter import messagebox

# Global variables
xpos = 20
ypos = 60

## func.
def func_open():
    messagebox.showinfo("message", "Wait...it is being developed. : )")

def func_quit():
    window.quit()
    window.destroy()

#def func_check_int():
#def func_check_char():

def func_gen():
    #messagebox.showinfo("a", str1.get())
    filename = str1.get() + '.txt'
    file = open(filename,'w')
    file.write("<tag x> " + str2.get() + " </tag x>"+'\n')
    file.write("<tag y> " + str3.get() + " </tag y>")


## main
window = Tk()

label_name = Label(window, text = "파일이름 입력:")
label_name.place(x=xpos, y=ypos-40)
str1 = StringVar()
textbox = Entry(window, width=30, textvariable=str1)
textbox.place(x=xpos+100, y=ypos-40)

label_x = Label(window, text = "x값 입력:")
label_x.place(x=xpos, y=ypos)
str2 = StringVar()
textbox = Entry(window, width=15, textvariable=str2)
textbox.place(x=xpos, y=ypos+20)
button1 = Button(window, text="입력 검사")
button1.place(x=xpos+120, y=ypos+17)

label_y = Label(window, text = "y값 입력:")
label_y.place(x=xpos, y=ypos*2)
str3 = StringVar()
textbox = Entry(window, width=15, textvariable=str3)
textbox.place(x=xpos, y=ypos*2 + 20)
button2 = Button(window, text="입력 검사")
button2.place(x=xpos+120, y=ypos*2 +17)

generate_button = Button(window, text = "파일 생성", fg= "white", bg="green", command = func_gen)
generate_button.place(x=xpos+220, y=ypos+10, width=95, height=40)

check_button = Button(window, text = "생성 확인", fg= "white", bg="blue")
check_button.place(x=xpos+220, y=ypos*2+10, width=95, height=40)

mainMenu = Menu(window)
window.config(menu = mainMenu)
window.title("XML_generator.ver.1.1")
window.geometry("600x300")

fileMenu = Menu(mainMenu, tearoff=0) # tearoff -> 자동 점선 제거
mainMenu.add_cascade(label = "파일", menu = fileMenu) # 메뉴 확장
fileMenu.add_command(label = "nod.xml", command = func_open)
fileMenu.add_command(label = "edg.xml", command = func_open)
fileMenu.add_command(label = "net.xml", command = func_open)
fileMenu.add_command(label = "rou.xml", command = func_open)
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = func_quit)

window.mainloop()


