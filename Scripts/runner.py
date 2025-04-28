import sys
import pyautogui,time

# variables of the program
v={}
sym=['+','-','*','/','%']
ts=[False]

def terminate(ts=ts):
    if not(ts[0]):
        time.sleep(1)
        pyautogui.keyDown('alt')
        pyautogui.press('Tab')
        time.sleep(0.1)
        pyautogui.keyUp('alt')
        ts[0]=True
    sys.exit()

def ev_num(expr,sym=sym,v=v):
    end=""
    for e in expr:
        end+=e+' '
    stack=[]
    ans=0
    for ele in expr:
        if ele in sym:
            try:
                b=stack.pop()
                a=stack.pop()
                #print('[',a,':',b,':',ele,']',stack)
            except:
                print("Expression error: invalid expression [ ",end,"]")
                
                terminate()
                
            if type(a)==str or type(b)==str:                
                if ele=='+':
                    ans=str(a)+str(b)
                elif ele=='*' and (type(a)==int or type(b)==int):
                    ans=a*b
                else:
                    print("Type error: cannot perform ",end="")
                    if ele=='*':
                        print("multiplication ",end="")
                    elif ele=='-':
                        print("subtraction ",end="")
                    elif ele=='/':
                        print("division ",end="")
                    elif ele=='%':
                        print("modulus ",end="")
                    elif ele=='+':
                        print("addition ",end="")
                    print("with strings [",end,"]")
                    
                    terminate()
            else:
                if ele=='+':
                    ans=a+b
                elif ele=='-':
                    ans=a-b
                elif ele=='*':
                    ans=a*b
                elif ele=='/':
                    try:
                        ans=a/b
                    except:
                        print("Expression error: cannot divide the expression [ ",end,"]")
                        
                        terminate()
                elif ele=='%':
                    try:
                        ans=a%b
                    except:
                        print("Expression error: cannot find modulo in expression [ ",end,"]")
                        
                        terminate()
                    
            stack.append(ans)
        else:
            if ele == 'input':
                inp=input()
                try:
                    if '.' in inp:
                        stack.append(float(inp))
                    else:
                        stack.append(int(inp))
                except:
                    stack.append(inp)
            else:
                if ele in v:
                    stack.append(v[ele])
                else:
                    if '.' in ele:
                        try:
                            stack.append(float(ele))
                        except:
                            print("Expression Error: invalid input {",ele,"} in [",end,"]")
                            
                            terminate()
                    elif '"' in ele:
                        stack.append(ele.replace('"',''))
                    else:
                        try:
                            stack.append(int(ele))
                        except:
                            print("Expression Error: invalid input {",ele,"} in [",end,"]")
                            
                            terminate()
                        
    if len(stack)!=0:
        #print(stack)
        ans=stack[0]
    return ans


dtypes=['int','float','string']
def var_maker(words,dtypes=dtypes,v=v,sym=sym):
    expr=words[3:]
    end=''
    for e in words:
        end+=e+' '
    if words[0]=='int':
        try:
            v[words[1]]=int(ev_num(expr))
        except:
            print("Type error: cannot convert expression to int [ ",end,"]")
            
            terminate()
            
    elif words[0]=='float':
        try:
            v[words[1]]=float(ev_num(expr))
        except:
            print("Type error: cannot convert expression to float [",end,"]")
            
            terminate()
            
    elif words[0]=='string':
        try:
            v[words[1]]=str(ev_num(expr))
        except:
            print("Type error: cannot evaluate expression [",end,"]")
            
            terminate()
    



def run(lines,gt,cond,dtypes=dtypes,v=v):
    ifc=[]
    i=0
    pc=0
    while pc<len(lines):
        words=lines[pc]
        pc+=1

        if words[0][0]=="~":
            continue
        
        if words[0].lower() in dtypes:
            var_maker(words)
        elif words[0].lower() == 'goto':
            tc=gt[pc-1][0][0]
            for _ in range(gt[pc-1][0][1]):
                ifc.pop()
            for i in gt[pc-1][1]:
                ifc.append(i)
            pc=tc
            
        elif words[0].lower()[:5] == 'print' and len(words[0])<=6:
            expr=[]
            is_ex=False
            for w in words[1:]:
                if '^' in w:
                    if w[0] == '^' and w[-1] == '^' and len(w)>1:
                        if w.replace('^','') in v:
                            print(v[w.replace('^','')],end=" ")
                        else:
                            print(w,end=" ")
                    else:
                        is_ex=not(is_ex)
                        if not(is_ex):
                            expr.append(w.replace('^',''))
                            expr=[e for e in expr if len(e)>0]
                            print(ev_num(expr),end=" ")
                            expr=[]
                else:
                    if not(is_ex):
                        print(w,end=" ")
                if is_ex:
                    expr.append(w.replace('^',''))

                    
            if not('l' in words[0]):        
                print()
            
        elif words[0].lower() == 'if':
            skp=False

            splt=0
            for w in words:
                if w in ['=','!=','<','<=','>','>=']:
                    break
                splt+=1
                        
            if words[splt] == '=':
                if not(ev_num(words[1:splt])==ev_num(words[splt+1:])):
                    skp=True
            if words[splt] == '!=':
                if ev_num(words[1:splt])==ev_num(words[splt+1:]):
                    skp=True
            if words[splt] == '>':
                if ev_num(words[1:splt])<=ev_num(words[splt+1:]):
                    skp=True
            if words[splt] == '<':
                if ev_num(words[1:splt])>=ev_num(words[splt+1:]):
                    skp=True
            if words[splt] == '<=':
                if ev_num(words[1:splt])>ev_num(words[splt+1:]):
                    skp=True
            if words[splt] == '>=':
                if ev_num(words[1:splt])<ev_num(words[splt+1:]):
                    skp=True

            ifc.append(pc-1)
            if skp:
                if len(cond[pc-1])==2:
                    pc=cond[pc-1][0]+1
                elif len(cond[pc-1])==1:
                    pc=cond[pc-1][0]
                else:
                    print("SYNTAX ERROR: invalid conditional , at line",pc)
                    
                    terminate()
                
        elif words[0].lower() == 'else':
            pc=cond[ifc[-1]][1]
        elif words[0].lower() == 'end':
            try:
                ifc.pop()
            except:
                print("SYNTAX ERROR: cannot evaluate conditional , at line",pc)
                
                terminate()
            
        else:
            print("SYNTAX ERROR: invalid syntax , at line",pc,"  [",line,"]")
            
            terminate()

            
