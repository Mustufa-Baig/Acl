import sys
code=""

# Read the code into memory
try:
    with open(sys.argv[1],'r') as file:
        code=file.read()
    with open("last.txt",'w') as l:        
        l.write(sys.argv[1])
        
except:
    with open("last.txt",'r') as l:        
        with open(l.readlines()[0],'r') as file:
            code=file.read()

# seperate each lines , and remove empty ones
lines=[line for line in code.split("\n") if len(line.replace(" ",""))>0]

# variables of the program
v={}

# helper functions
def read(line):
    #returns a list of words of a line
    words=[""]
    i=0
    for char in line:
        if char==" ":
            i+=1
            words.append("")
        else:
            words[i]+=char

    words=[word.replace('\t','') for word in words if len(word)>0]
    return words

sym=['+','-','*','/','%']
def ev_num(expr,sym=sym,v=v):
    stack=[]
    ans=0
    for c in expr:
        if c in sym:
            b=stack.pop()
            a=stack.pop()
            
            if c=='+':
                ans=a+b
            elif c=='-':
                ans=a-b
            elif c=='*':
                ans=a*b
            elif c=='/':
                ans=a/b
            elif c=='%':
                ans=a%b

            stack.append(ans)
        else:
            try:
                if '.' in c:
                    stack.append(float(c))
                else:
                    stack.append(int(c))
            except:
                if c == 'input':
                    inp=input()
                    if '.' in inp:
                        stack.append(float(inp))
                    else:
                        stack.append(int(inp))
                else:
                    stack.append(v[c])
                
    if len(stack)!=0:
        ans=stack[0]
    return ans

dtypes=['int','float']
def var_maker(words,dtypes=dtypes,v=v):
    expr=words[3:]
    v[words[1]]=ev_num(expr)
            



# cache conditional jump positions
ifc=[]
cond={}
i=0
for l in lines:
    line=read(l)
    if line[0]=='if':
        ifc.append(i)
        cond[i]=[]
    if line[0]=='else':
        cond[ifc[-1]].append(i)
    if line[0]=='end':
        cond[ifc.pop()].append(i)
    i+=1
#print(cond)

ifc=[]
i=0
pc=0
while pc<len(lines):
    line=lines[pc]
    #print(line)
    pc+=1

    
    if line[0]=="~":
        continue
    words=read(line)
    
    if words[0].lower() in dtypes:
        var_maker(words)
    elif words[0].lower() == 'goto':
        tc=0
        while tc<len(lines):
            if lines[tc]=="~"+words[1]:
                pc=tc
                break
            tc+=1

        
    elif words[0].lower()[:5] == 'print' and len(words[0])<=6:
        for w in words[1:]:
            if w.replace('/','') in v and '/' in w:
                print(v[w.replace('/','')],end=" ")
            else:
                print(w,end=" ")
                
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
            if len(cond[pc-1])==1:
                ifc.pop()
            pc=cond[pc-1][0]+1
            
            
    elif words[0].lower() == 'else':
        pc=cond[ifc[-1]][1]
    elif words[0].lower() == 'end':
        ifc.pop()
    else:
        pass
    
#print(v)
end=input("\n<Program executed>\n<Press 'Enter' to exit>")
