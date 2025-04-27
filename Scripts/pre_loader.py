def cache_conditional_jumps(lines):
    ifc=[]
    cond={}
    i=0
    for line in lines:
        if line[0]=='if':
            ifc.append(i)
            cond[i]=[]
        elif line[0]=='else':
            cond[ifc[-1]].append(i)
        elif line[0]=='end':
            cond[ifc.pop()].append(i)
        i+=1
    return cond

def cache_goto_jumps(lines,cond):
    i=0
    gt={}
    ifc=[]
    for line in lines:
        if line[0]=='if':
            ifc.append(i)
        elif line[0]=='end':
            ifc.pop()
            
        elif line[0]=='goto':
            tc=0
            while tc<len(lines):
                if len(lines[tc])==1:
                    if lines[tc][0]=="~"+line[1]:
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
    return gt
