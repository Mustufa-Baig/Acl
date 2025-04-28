import sys
import subprocess
import pyautogui,time

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
    total=""
    for s in sys.argv[1:]:
        total+=s+" "
        
    with open("Luts/config.txt",'w') as file:
        file.write(total[:-1])
    total=total[:-1].split(' ')
    print("<Updated Config.txt>")
    
except:
    with open("Luts/config.txt",'r') as file:
        s=file.read().replace("\n"," ")
        settings=s.split(" ")
        size=[int(settings[0]),int(settings[1])]
        f_size=int(settings[2])
        filename=settings[3]
        
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
    pyautogui.keyDown('alt')
    pyautogui.press('Tab')
    time.sleep(0.1)
    pyautogui.keyUp('alt')
    
def f_up(key,total=total):
    t.config(font=("Segoe UI",int(update_config(2,1))))

def f_down(key,total=total):
    t.config(font=("Segoe UI",int(update_config(2,-1))))

    
def save_quit():
    if len(t.get("1.0",tk_end))>1:
        with open(filename,'w') as file:
            file.write(t.get("1.0",tk_end))
    root.destroy()


# Words to highlight in yellow
word_list = ["int","float","string","if","else","end","goto","~","^","print","printl"]

def highlight_words(event=None):
    t.tag_remove("yellow", "1.0", "end")
    t.tag_remove("red", "1.0", "end")
    t.tag_remove("green", "1.0", "end")
    t.tag_remove("gray", "1.0", "end")

    l=0
    for line in t.get("1.0",END).split("\n"):
        l+=1
        if "^" in line:
            s=-1
            e=0
            i=0
            for c in line:
                if c=="^":
                    if s==-1:
                        s=i
                    else:
                        e=i+1
                        t.tag_add("green", str(l)+"."+str(s), str(l)+"."+str(e))
                        s=-1
                        
                i+=1
                
    #content=t.get(f"{line}.0", f"{line}.end").replace("\t",' ')
    
    for word in word_list:
        start = "1.0"
        while True:
            start = t.search(word, start, stopindex="end", nocase=False)
            if not start:
                break
            end = f"{start}+{len(word)}c"
            next_char = t.get(end, f"{end}+1c")
            try:
                prev_char = t.get(f"{start}-1c",start)
            except:
                prev_char = ' '
                
            if prev_char in [""," ","\n","\t"]:
                if next_char in [""," ","\n","\t"] and not(word in ["~","^"]):
                    t.tag_add("yellow", start, end)
                elif word=="~":
                    if ' ' in t.get(start.split('.')[0]+".0",start.split('.')[0]+".end").split("~")[1]:
                        t.tag_add("gray", start, str(end.split(".")[0])+".end")
                        
                    else:
                        t.tag_add("red", start, str(end.split(".")[0])+".end")

            start = end

ifc=[0]
def tab_manager(event=None,ifc=ifc):
    # Get current cursor index
    index = t.index("insert")
    line, col = map(int, index.split('.'))
    if col>0:
        content=t.get(f"{line}.0", f"{line}.end").replace("\t",' ')
        if "if" in content:
            valid=False
            if len(content.split("if")[0])==0:
                valid=True
            elif content.split("if")[0][-1] == ' ':
                valid=True
                
            if len(content.split("if")[1])>0:
                if content.split("if")[1][0] == ' ':
                    valid=True
                else:
                    valid=False
            else:
                valid=False

            if valid:
                if col==len(content):
                    t.insert("insert","\n\t")
                    ifc[0]+=1
                    return "break"
        elif ifc[0]>0:            
            if "end" in content:
                if len(content.replace(" ",""))==3:
                    ifc[0]-=1
            if ifc[0]>0:
                t.insert("insert","\n\t")
                return "break"
        

windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title("ACL Ide - "+filename)
root.configure(bg="grey10")
root.geometry(str(size[0])+"x"+str(size[1]))
#root.minsize(*size)
#root.maxsize(*size)

t = Text(root,width=75,height=40,font=("Segoe UI",f_size),bg="grey10",fg="white",insertbackground="white",highlightthickness=0,borderwidth=0,undo=True,maxundo=100)

with open(filename,'r') as file:
    f=file.read()
    if len(f)>0:
        if f[-1]=="\n":
            f=f[:-1]
    t.insert("1.0",f)
    
t.pack(padx=5,side='top',fill='both',expand=True)                    
t.tag_configure("yellow", foreground="yellow")
t.tag_configure("green", foreground="green")
t.tag_configure("gray", foreground="grey60")
t.tag_configure("red", foreground="red")

highlight_words()
t.bind("<KeyRelease>",highlight_words)
#t.bind("<Return>",tab_manager)

root.bind("<F5>",run)
root.bind("<F3>",f_up)
root.bind("<F2>",f_down)

root.protocol("WM_DELETE_WINDOW", save_quit)

root.mainloop()
