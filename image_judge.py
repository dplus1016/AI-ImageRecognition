from tkinter import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
from Judge import *
import os


def f_open():
    tLabel.configure(text="")
    
    filename=askopenfilename(parent=window, filetypes=(("JPG 파일", "*.jpg"),("모든 파일","*.*")))
    img2=ImageTk.PhotoImage(Image.open(filename))
    pLabel.configure(image=img2)
    pLabel.image=img2

    global m_filename, l_filename
    s=judge(filename,m_filename,l_filename)
    tLabel.configure(text="[판정결과]\n\n"+s)



def m_open():
    global m_filename
    m_filename=askopenfilename(parent=window, filetypes=(("h5 파일", "*.h5"),("모든 파일","*.*")))
    pLabel.configure(text="")
    mLabel.configure(text="\n    1) 모델 파일: "+m_filename)
    print(m_filename)



def l_open():
    global l_filename
    l_filename=askopenfilename(parent=window, filetypes=(("labels 파일", "*.txt"),("모든 파일","*.*")))
    pLabel.configure(text="")
    lLabel.configure(text="    2) 레이블 파일: "+l_filename+"\n\n")
    print(l_filename)

    



window=Tk()
window.geometry("600x600")
window.title("인공지능 이미지 인식기")

mLabel=Label(window,text="",font=("맑은고딕",10,"bold"))
mLabel.pack(anchor=W)

lLabel=Label(window,text="",font=("맑은고딕",10,"bold"))
lLabel.pack(anchor=W)

pLabel=Label(window,text="\n\n먼저 모델을 선택한 후에 테스트 이미지를 선택하십시오.",font=("맑은고딕",15,"bold"))
pLabel.pack(anchor=CENTER)

tLabel=Label(window,text="",font=("맑은고딕",20,"bold"))
tLabel.pack(anchor=CENTER)


mainMenu = Menu(window)
window.config(menu=mainMenu)
test_fileMenu=Menu(mainMenu)
model_fileMenu=Menu(mainMenu)

mainMenu.add_cascade(label="[1]모델",menu=model_fileMenu)
mainMenu.add_cascade(label="[2]테스트 이미지",menu=test_fileMenu)

test_fileMenu.add_command(label="파일 열기",command=f_open)
model_fileMenu.add_command(label="1) 모델 파일 열기",command=m_open)
model_fileMenu.add_command(label="2) 레이블 파일 열기",command=l_open)



window.mainloop()

