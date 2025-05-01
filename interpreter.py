import sys,os
import pyautogui
from Scripts import error_checker
from Scripts import pre_loader
from Scripts import runner
from Scripts import parser

code=""

# Read the code into memory
try:
    # Load file from cli input
    with open(sys.argv[1],'r') as file:
        code=file.read()

    with open("Luts/config.txt",'r') as l:
        total=l.read()
    t=total.split(" ")[:-1]
    total=""
    for i in t:
        total+=i+" "
    total+=sys.argv[1]
    
    with open("Luts/config.txt",'w') as l:
        l.write(total)
    print("<Running ",sys.argv[1],">")
    
except:
    try:
        # try to Load last read file
        with open("Luts/config.txt",'r') as l:
            fname=l.readlines()[0].split(" ")
            if len(fname[-1])>0:
                fname=fname[-1]
            else:
                fname=fname[-2]
                
            with open(fname,'r') as file:
                code=file.read()
            print("< Running ",fname,">")
    except:
        # return an error
        print("Error: No input file given")
        print("\n<Program execution terminated>")
        sys.exit()


code,v_temp=parser.extract_code(code)
syn_err=error_checker.check_syntax_errors(code)
typ_err=error_checker.check_type_errors(code,v_temp)
if len(syn_err)>0:
    print("SYNTAX ERROR")
    print(syn_err)
    
if len(typ_err)>0:
    print("TYPE ERROR")
    print(typ_err)

if len(syn_err)==0 and len(typ_err)==0:
    conditionals=pre_loader.cache_conditional_jumps(code)
    gt_positions=pre_loader.cache_goto_jumps(code,conditionals)

    runner.run(code,gt_positions,conditionals)


    
end=input("\n<Program executed>\n<Press 'Enter' to exit>")
os.system('cls')
pyautogui.hotkey(['alt','tab'])
