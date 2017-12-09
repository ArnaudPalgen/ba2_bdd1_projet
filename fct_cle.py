def tablenamecle()

    t=[]
    i=0
    for i in FuncDep:
        if FuncDep[i][0] in t:
            i+=1
        else:
            t.append(FuncDep[i][0])
            i+=1
    c=tuple(t)
    a = input("quelle table voulez-vous choisir : "+ c)
    getcle(a)



def getcle(table)

    tAttribut=[]
    tRhs=[]
    i=0
    
    aCle=[]
    
    for i in FuncDep:
        if table != FuncDep[i][0]:
            i+=1
        else:
            if FuncDep[i][2] in tAttribut:
                if FuncDep[i][2] in tRhs == False:
                    tRhs.append(FuncDep[i][2])
            else:
                tAttribut.append(FuncDep[i][2])

            j = 0

            for j in FuncDep[i][1]:
                if FuncDep[i][1][j] in tAttribut:
                    j+=1
                else:
                    tAttribut.append(FuncDep[i][1][j])
                    j+=1
            i+=1
    h=0
    for h in tAttribut:
        if tAttribut[h] in tRhs == False:
            aCle.append(tAttribut[h])
            h+=1
        else:
            h+=1