def tablenamecle():

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

def getcle(table):

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


for i in aLhs:
	if i ==',' and i+1 == ' ':
		aLhs.remove(i)
		i+2
	elif i ==',' and i+1 !=' ':
		aLhs.revome(i)
		aLhs.insert(i,' ')
		i+1
	else:
		i+1




def is3NF(self, table):
	if prem3NF(table) or lhs3NF(table):
		return True
	else:
		return False


def prem3NF(self,table)
	tabCle = getcle(table)
	tabAttr = getTableAttribute(table):
	for i in range(0:len(tabAttr)):
		attr= tabAttr[i]
		for j in range(0:len(tabCle)):
			cle = table[j]
			for h in range(0:len(cle)):
				indice = cle[h]
				if indice == attr:
					attr += 1
				else:
					indice += 1
			cle += 1
		return False
	return True

def lhs3Nf(self,table):

	tabLhs = getAllLhs(table)
	tabCle = getcle(table)
	for i in range(0:len(tabLhs)):
		lhs=tabLhs[i]
		if lhs.split() in tabCle:
			i += 1
		else:
			return False
	return True



def sortDep(self, table):
	df=self.dbh.getDepByRelation(table)
	for dep in df:
		dep.pop(0)
	df.sort()


def delinutile(self,table):
	df=self.dbh.getDepByRelation(table)
	for dep in df:
		if isLogicConsequence(table, dep[1],dep[2]) != None:
			removeDep(table,dep[1],dep[2])
		if satisfaitPasDF(self, table, dep[1], dep[2]) != None:
			removeDep(table,dep[1],dep[2])