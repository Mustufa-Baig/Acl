import sys
import subprocess

total=[]
filename="temp.acl"
def update_config(index,amount,total=total):
    if type(amount)==str:
        total[index]=amount
    else:
        total[index]=str(int(total[index])+amount)
        
    with open("Luts/config.txt",'w') as file:
        total[index]=str(int(total[index])+amount)
        text=""
        for i in total:
            text+=i+" "
        file.write(text)
        
    return total[index]


try:
    size=[int(sys.argv[1]),int(sys.argv[2])]
    f_size=int(sys.argv[3])
    filename=sys.argv[4]
    update_config(3,filename)

    
except:
    with open("Luts/config.txt",'r') as file:
        s=file.read().replace("\n"," ")
        settings=s.split(" ")
        size=[int(settings[0]),int(settings[1])]
        f_size=int(settings[2])
        
        for i in settings:
            total.append(i)


from tkinter import *
from tkinter import END as tk_end
from tkinter import ttk
from ctypes import windll


def run(key):
    with open(filename,'w') as file:
        file.write(t.get("1.0",tk_end))
    subprocess.Popen("python interpreter.py temp.acl")
    
def f_up(key,total=total):
    t.config(font=("Segoe UI",int(update_config(2,1))))

def f_down(key,total=total):
    t.config(font=("Segoe UI",int(update_config(2,-1))))

    
def save_quit():
    with open(filename,'w') as file:
        file.write(t.get("1.0",tk_end))
    root.destroy()

windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title("ACL Ide")
root.configure(bg="gray10")
root.geometry(str(size[0])+"x"+str(size[1]))
root.minsize(*size)
root.maxsize(*size)

t = Text(root,width=75,height=40,font=("Segoe UI",f_size),bg="gray10",fg="gray80")
with open(filename,'r') as file:
    t.insert("1.0",file.read())
t.pack()

root.bind("<F5>",run)
root.bind("<F3>",f_up)
root.bind("<F2>",f_down)


root.protocol("WM_DELETE_WINDOW", save_quit)

root.mainloop()
