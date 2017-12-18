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


def getDecomp3NF(self, table):
	#entre un tableau de tableau ou chaque tableau est une df
	#gerer dernier elem 
	tabcle = self.getcle(table)
	tabcle.sort(key=len)
	tablecouv = self.getCouvertureMinimale(table)
	cleanTable= self.cleanDep(tablecouv)
	cleantable.sort()
	newtable = []
	tableprov = []
	
	tableprov.append(cleanTable[0])
	cleanTable.remove(0)
	for df in cleanTable:
		if df[0] == tableprov[0][0]:
			tableprov.append(df)
		else:
			newtable.append(tableprov)
			tableprov = []
			tableprov.append(df)
	newtable.append(tableprov)
	print("newTable: "+str(newtable))
	
	tablefus = []
	tableprov = []
	for groupe in newtable:
		tableprov.append(groupe[0][0])
		tableprov.append("/")
		for df in groupe:
			tableprov.append(df[1])
		tablefus.append(tableprov)
	print("tableau fusion : "+str(tablefus))
	
	

	for rel in tablefus:
		tabtestcle = []
		i = 0
		while rel[i] != "/":
			tabtestcle.append(rel[i])
		for cle in tabcle:
			if cle == tabtestcle:
				return tablefus
	tableprov =[]
	tableprov.append(tabcle[len(tabcle-1)].pop(0))
	tableprov.append("/")
	tableprov.extend(tabcle[len(tabcle-1)])
	tablefus.append(tableprov)
	print("table final: "+str(tablefus))
	return tablefus

	
increment = 1
print("ces df ne sont pas respectees car : ")
print("la table ou les attributs n'existent plus : ")
for line in getInutileDf()[0]:
	print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
			increment  += 1
print("-----------------------------------------------")
print("ces df sont des consequences logique : ")
for line in getInutileDf()[0]:
	print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
			increment  += 1









def cleanDep(self, table):
	newtable = []
	for df in table:
		newtable.append(df[1])
		newtable.append(df[2])
	return newtable






print("que voulez-vous faire?")
print("1. afficher et supprimer les df ayant la table ou un argument qui n'est plus existant")
print("2. afficher et supprimer les df qui sont des consequences logiques")
print("3. afficher et supprimer les df qui ne sont pas respectees")
print("4. suppression de toutes les df inutiles")
print("5. retour au menu analyse")

try:
	nbre = input("entrez le nbre: ")
	option = int(nbre)
		
		if option <=3:
			increment = 1
			
			for line in getInutileDf()[option-1]:
				print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
				increment  += 1
			print("quelle(s) lignes voulez-vous supprimer?")
			nbre = input("numero de la ligne si plusieurs separez les nombre par des espaces) : ")
			
			for i in nbre.split()		
				
				if i != " ":
					i = int(i)
					dbh.removeDep(getInutileDf()[option-1][i -1][0],getInutileDf()[option-1][i -1][1],getInutileDf()[option-1][i -1][2]):
					#retour remove verif

		elif option = 4:
			print("les df suivantes vont etre supprimees")
			increment = 1
			h = 0
			while h <=2:
				for line in getInutileDf()[h]:
					print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
					increment += 1
				h += 1

			choice = input("voulez-vous continuer? (Y/N) : ")
			
			if choice == "Y" or choice == "y":
				i = 0
				
				while i <=2:
					
					for j in range(0,len(getInutileDf()[i])-1):
						dbh.removeDep(getInutileDf()[i][j][0],getInutileDf()[i][j][1],getInutileDf()[i][j][2]):
					i+=1
			
			elif choice == "N" or choice == "n":
				analyse()

			else:
				error = input("error integer")
				analyse()
	elif option == 5:
		analyse()
	else:
		error=input("error integer")
		analyse()

except ValueError:
	except_error=input("invalid syntax, try again")
	analyse()


def getDecomposition3nf(self, table): #pour l honneur

		tabcle = self.getCle(table)
		tabcle.sort(key=len)
		#print(str(tabcle))
		tablecouv = self.getCouvertureMinimale(table)
		#print("base :"+str(tablecouv))
		cleanTable= self.cleanDep(tablecouv)
		#print("clean :"+str(tablecouv))
		cleanTable.sort()

		newtable = []
		tableprov = []
		#print("trie: "+str(tablecouv))
		
		tableprov.append(cleanTable[0])
		cleanTable.pop(0)
		for df in cleanTable:
			if df[0] == tableprov[0][0]:
				tableprov.append(df)
			else:
				newtable.append(tableprov)
				tableprov = []
				tableprov.append(df)
		newtable.append(tableprov)
		#print("newTable: "+str(newtable))
		
		tablefus = []
		tableprov = []
		for groupe in newtable:
			tableprov.append(groupe[0][0])
			tableprov.append("-->")
			for df in groupe:
				tableprov.append(df[1])
			tablefus.append(tableprov)
			tableprov = []

		#print("tableau fusion : "+str(tablefus))
		
		

		for rel in tablefus:
			tabtestcle = []
			#print(str(rel)+"ggggggggg")
			for elem in rel:
				#print(str(elem)+"hhhhhhhhh")
				if elem != '-->':
					tabtestcle.append(elem)
					print(str(tabtestcle)+"test")
					for cle in tabcle:
						print(cle)
						if cle[0] == tabtestcle:
							print(tablefus)
							return tablefus
				else:
					break
				tabtestcle =[]
			
		

		tableprov =[]
		relcle =tabcle[len(tabcle)-1]
		if len(relcle) == 1:
			tablefus.append(relcle)
			print("table finals: "+str(tablefus))
			return tablefus
		else:
			tableprov.append(relcle[0])
			relcle.pop(0)

			tableprov.append("-->")
			tableprov.extend(relcle)
			tablefus.append(tableprov)
			print("table final: "+str(tablefus))
			return tablefus

















