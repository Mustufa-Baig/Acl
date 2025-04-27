sym=['+','-','*','/','%']
def read(line,sym=sym):
    words=[""]
    is_str=False
    i=-1
    for char in line:
        i+=1
        if char=='"':
            is_str=not(is_str)
            if not(is_str):
                words[-1]+='"'
                words.append('')
            else:
                words.append('"')
            continue
        
        if not(is_str) and (char==" " or char in sym or char in ['=','!','<','>']):
            if char == ' ':
                words.append('')
            elif char in sym:
                if char=='-':
                    try:
                        n=int(line[i+1])
                        words[-1]+=char
                    except:
                        words.append(char)
                        words.append("")
                else:
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

    words=[word.replace('\t','') for word in words]
    ws=[]
    for w in words:
        if len(w)>0:
            ws.append(w)
    return ws

def extract_code(code):
    # seperate each lines , and remove empty ones
    lines=[]
    for line in code.split("\n"):
        if len(line.replace(" ",'').replace("\t",''))>0:
            lines.append(line.replace("\t"," "))


    code=[]
    v_temp=[]
    for line in lines:
        code.append(read(line))
        if code[-1][0] in ['int','float','string']:
            if not(code[-1][1] in v_temp):
                v_temp.append(code[-1][1])

    return code,v_temp
