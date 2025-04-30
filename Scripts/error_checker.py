keywords=["int","float","list","string","if","else","end","goto","~","print","printl"]
dtypes=["int","float","list","string"]

def check_syntax_errors(code,keywords=keywords,dtypes=dtypes):
    errors=[]
    line_no=0
    if_count=[]
    for instruction in code:
        key=instruction[0]
        #non-existing instructions
        if not(instruction[0] in keywords):
            if not(instruction[0][0]=="~"):
                errors.append(["Invalid Keyword",line_no,instruction,instruction[0]])

        #invalid amount of arguments
        if key in dtypes:
            if len(instruction)<4:
                errors.append(["Invalid Syntax",line_no,instruction,instruction[-1]])
        elif key=='if':
            if len(instruction)==1:
                errors.append(["Invalid Syntax",line_no,instruction,instruction[0]])
            else:
                if_count.append(line_no)
        elif key=='end':
            if not(len(instruction)==1):
                errors.append(["Invalid Syntax",line_no,instruction,instruction[1:]])
            else:
                if_count.pop()
        elif key=='goto':
            if len(instruction)>2:
                errors.append(["Invalid Syntax",line_no,instruction,instruction[2:]])
            elif len(instruction)<2:
                errors.append(["Invalid Syntax",line_no,instruction,instruction[0]])
            else:
                #find the jump position
                found=False
                for i in code:
                    if len(i)==1:
                        if i[0]=="~"+instruction[1]:
                            found=True
                if not(found):
                    errors.append(["Invalid Syntax",line_no,instruction,instruction[1]])
        
        line_no+=1
        
    if not(len(if_count)==0):
        for i in if_count:
            errors.append(["Invalid Syntax",i,code[i],"missing end"])
        
    return errors


def check_type_errors(code,v,dtypes=dtypes):
    errors=[]
    i=0
    for instruction in code:
        if instruction[0] in dtypes:
            if len(instruction)==4:
                if instruction[3]=='input' or "[" in instruction[3] or instruction[3][0]=="#":
                    continue
                
                if instruction[0]=='int':
                    try:
                        n=float(instruction[3])
                    except:
                        if not(instruction[3] in v):
                            errors.append(["int",i,instruction[3]])
                            
                elif instruction[0]=='float':
                    try:
                        n=float(instruction[3])
                    except:
                        if not(instruction[3] in v):
                            errors.append(["float",i,instruction[3]])
                elif instruction[0]=='string':
                    if not(instruction[3] in v):
                        if len(instruction[3])>2:
                            if not(instruction[3][0]=='"' and instruction[3][-1]=='"'):
                                errors.append(["string",i,instruction[3]])
                        elif len(instruction[3])==2:
                            if not(instruction[3]=='""'):
                                errors.append(["string",i,instruction[3]])
                        else:
                            errors.append(["string",i,instruction[3]])
                        
                
        i+=1
    return errors

