import sys
code=""

# Read the code into memory
try:
    with open(sys.argv[1],'r') as file:
        code=file.read()
    with open("last.txt",'w') as l:        
        l.write(sys.argv[1])
    print("<Running ",sys.argv[1],">")
    
except:
    with open("last.txt",'r') as l:
        fname=l.readlines()[0]
        with open(fname,'r') as file:
            code=file.read()
        print("< Running ",fname,">")
    

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


halt=[False]
def terminate(halt=halt):
    halt[0]=True
    

def ev_num(expr,sym=sym,v=v):
    stack=[]
    ans=0
    for ele in expr:
        if ele in sym:
            b=stack.pop()
            a=stack.pop()

            if type(a)==str or type(b)==str:                
                if ele=='+':
                    ans=str(a)+str(b)
                elif ele=='*' and (type(a)==int or type(b)==int):
                    ans=a*b
                else:
                    terminate()
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
                    print("with strings")
            else:
                if ele=='+':
                    ans=a+b
                elif ele=='-':
                    ans=a-b
                elif ele=='*':
                    ans=a*b
                elif ele=='/':
                    ans=a/b
                elif ele=='%':
                    ans=a%b
                    
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
                        stack.append(float(ele))
                    elif "'" in ele:
                        stack.append(ele.replace("'",''))
                    else:
                        try:
                            stack.append(int(ele))
                        except:
                            print("Expression Error: invalid input {",ele,"}")
                            terminate()
                        
    if len(stack)!=0:
        ans=stack[0]
    return ans


dtypes=['int','float','string']
def var_maker(words,dtypes=dtypes,v=v,sym=sym):
    expr=words[3:]
    if words[0]=='int':
        v[words[1]]=int(ev_num(expr))
    elif words[0]=='float':
        v[words[1]]=float(ev_num(expr))
    elif words[0]=='string':
        v[words[1]]=str(ev_num(expr))
    



# cache jump positions
ifc=[]
cond={}
gt={}
i=0
for l in lines:
    line=read(l)
    #print(cond)
    if line[0]=='if':
        ifc.append(i)
        cond[i]=[]
    if line[0]=='else':
        cond[ifc[-1]].append(i)
    if line[0]=='end':
        cond[ifc.pop()].append(i)
    i+=1

i=0
ifc=[]
for l in lines:
    line=read(l)

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
while pc<len(lines):
    #print("->",ifc)
    line=lines[pc]
    #print(line)
    pc+=1

    
    if line[0]=="~":
        continue
    words=read(line)
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
                print("SYNTAX ERROR: invalid conditional")
                terminate()
            
            
            
    elif words[0].lower() == 'else':
        pc=cond[ifc[-1]][1]
    elif words[0].lower() == 'end':
        #print(pc)
        ifc.pop()
    else:
        pass

    if halt[0]:
        break

end=input("\n<Program executed>\n<Press 'Enter' to exit>")
