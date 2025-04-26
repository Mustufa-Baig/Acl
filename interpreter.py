import sys
code=""

# Read the code into memory
try:
    # Load file from cli input
    with open(sys.argv[1],'r') as file:
        code=file.read()
    with open("last.txt",'w') as l:     
        l.write(sys.argv[1])
    print("<Running ",sys.argv[1],">")
    
except:
    try:
        # try to Load last read file
        with open("last.txt",'r') as l:
            fname=l.readlines()[0]
            with open(fname,'r') as file:
                code=file.read()
            print("< Running ",fname,">")
    except:
        # return an error
        print("Error: No input file given")
        print("\n<Program execution terminated>")
        sys.exit()


# seperate each lines , and remove empty ones
lines=[line for line in code.split("\n") if len(line.replace(" ",""))>0]

# variables of the program
v={}
sym=['+','-','*','/','%']

# helper functions
def read(line,sym=sym):
    #returns a list of words of a line
    words=[""]
    is_str=False
    for char in line:
        #print(words)
        if char=="'":
            is_str=not(is_str)
            if not(is_str):
                words[-1]+="'"
                words.append("")
            else:
                words.append("'")
            continue
        
        if not(is_str) and (char==" " or char in sym or char in ['=','!','<','>']):
            #print(char)
            if char == ' ':
                words.append('')
            elif char in sym:
                words.append(char)
                words.append("")
            elif char in ['!','<','>']:
                words.append(char)
                words.append("")
            elif char == '=':
                if words[-2] in ['!','<','>']:
                    words[-2]+='='
                else:
                    words.append('=')
                    words.append('')
        else:
            words[-1]+=char

    words=[word.replace('\t','') for word in words if len(word)>0]
    ws=[]
    for w in words:
        if len(w)>0:
            ws.append(w)
    return ws



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
            except:
                print("Expression error: invalid expression [ ",end,"]")
                end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                sys.exit()
                
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
                    end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                    sys.exit()
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
                        end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                        sys.exit()
                elif ele=='%':
                    try:
                        ans=a%b
                    except:
                        print("Expression error: cannot find modulo in expression [ ",end,"]")
                        end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                        sys.exit()
                    
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
                            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                            sys.exit()
                    elif "'" in ele:
                        stack.append(ele.replace("'",''))
                    else:
                        try:
                            stack.append(int(ele))
                        except:
                            print("Expression Error: invalid input {",ele,"} in [",end,"]")
                            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                            sys.exit()
                        
    if len(stack)!=0:
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
            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
            sys.exit()
            
    elif words[0]=='float':
        try:
            v[words[1]]=float(ev_num(expr))
        except:
            print("Type error: cannot convert expression to float [",end,"]")
            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
            sys.exit()
            
    elif words[0]=='string':
        try:
            v[words[1]]=str(ev_num(expr))
        except:
            print("Type error: cannot evaluate expression [",end,"]")
            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
            sys.exit()
    



# cache jump positions
ifc=[]
cond={}
gt={}
i=0
for l in lines:
    line=read(l)
    if len(line)==0:
        i+=1
        continue
    
    
    if line[0]=='if':
        ifc.append(i)
        cond[i]=[]
    if line[0]=='else':
        cond[ifc[-1]].append(i)
    if line[0]=='end':
        cond[ifc.pop()].append(i)
    i+=1
    #print(cond)

i=0
ifc=[]
for l in lines:
    line=read(l)
    if len(line)==0:
        i+=1
        continue
    
    if line[0]=='if':
        ifc.append(i)
    if line[0]=='end':
        ifc.pop()

            
    if line[0]=='goto':
        tc=0
        while tc<len(lines):
            if lines[tc]=="~"+line[1]:
                gt[i]=[[tc,0],[]]
                ifcs=len(ifc)
                for _ in range(ifcs):
                    if tc<ifc[-1] or tc>cond[ifc[-1]][-1]:
                        gt[i][0][1]+=1
                for ifs in cond:
                    if gt[i][0][0]>ifs and gt[i][0][0]<cond[ifs][-1]:
                        gt[i][1].append(ifs)
                gt[i][1].sort()
                break
            tc+=1
    i+=1
#print(gt)

ifc=[]
i=0
pc=0
#print(cond)
#print(gt)
while pc<len(lines):
    #print("->",ifc)
    line=lines[pc]
    #print(pc,line)
    pc+=1
    if len(line)==0:
        continue

    words=read(line)
    #print(words)
    if len(words)==0:
        continue

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
        #print(ifc)
        
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
                end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
                sys.exit()
            
    elif words[0].lower() == 'else':
        pc=cond[ifc[-1]][1]
    elif words[0].lower() == 'end':
        #print(pc)
        try:
            ifc.pop()
        except:
            print("SYNTAX ERROR: cannot evaluate conditional , at line",pc)
            end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
            sys.exit()
        
    else:
        print("SYNTAX ERROR: invalid syntax , at line",pc,"  [",line,"]")
        end=input("\n<Program execution terminated>\n<Press 'Enter' to exit>")
        sys.exit()
    

end=input("\n<Program executed>\n<Press 'Enter' to exit>")
