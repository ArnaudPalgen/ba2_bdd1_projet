# coding: utf-8
from DataBaseHandler import DataBaseHandler
import logging
import shutil
#TODO verifier isLogicConsequence
#TODO mettre un s a exist
#TODO demander consequence logique. tout sauf celle donee ?
#logging.basicConfig(filename='logs/log1.log',level=logging.DEBUG,\
#      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
class DfHandler():
	"""docstring for DfHandler"""
	TABLE='table'
	LHS='lhs'
	RHS='rhs'
	def __init__(self, dataBase):
		self.dbh=DataBaseHandler(dataBase)
		self.dataBaseName=dataBase


	def __isDep(self,table, lhs, rhs):
		"""
		Parametres: lhs et rhs str nettoyés !!
		Return True si la table existe, lhs et rhs sont des attributs de la table
		"""
		#TODO verifier rhs ne contient pas d'erreur
		
		#verifie que table est bien le nom d'une table
		listeTable=self.dbh.getTableName()
		if table not in listeTable:
			logging.debug("n'est pas une df 1: "+table+"-"+lhs+"-"+rhs)
			return False
		
		listeAttributs=self.dbh.getTableAttribute(table)# liste des attributs de la table
		
		#verifie que les noms dans lhs sont des attributs de la table
		sLhs=lhs.split(' ')
		logging.debug("slhs: "+str(sLhs))
		logging.debug("liste des attributs: "+str(listeAttributs))
		for item in sLhs:
			if item != ' ' and item not in listeAttributs:
				logging.debug("n'est pas une df 2: "+table+"-"+lhs+"-"+rhs)
				return False

		#verifie que rhs ne contient qu'un element 
		if rhs.count(' ') !=0:
			logging.debug("n'est pas une df 3: "+table+"-"+lhs+"-"+rhs)
			return False
		
		#verifie que rhs est un attribut de la table
		if rhs not in listeAttributs:
			logging.debug("n'est pas une df 4: "+table+"-"+lhs+"-"+rhs)
			return False
		logging.debug('est une DF: '+table+"-"+lhs+"-"+rhs)
		return True
		
	def __depExist(self, table, lhs, rhs):
		r=self.dbh.getOneDep(table, lhs, rhs)
		logging.debug("retour de getOneDep: "+str(r)+" "+str(type(r)))
		print('isDep '+str(self.__isDep(table, lhs, rhs)))
		print('result'+str(r))
		return self.__isDep(table, lhs, rhs) and r != None and len(r) == 3

	def removeDep(self, table, lhs, rhs):
		if self.__depExist(table, lhs, rhs):
			self.dbh.removeDep(table, lhs, rhs)
			return True	
		else:
			return False
		

	def getAllDep(self):
		return self.dbh.getAllDep()

	def insertDep(self, table, lhs, rhs):
		if self.__isDep(table, lhs, rhs) and not self.__depExist(table, lhs, rhs):
			r=self.dbh.insertDep(table, lhs, rhs)
			if r != None:#TODO verifier que r contient quelque chose
				return True
			else:
				return False

		else:
			return False

	def editDep(self, table, lhs, rhs, newData,whatModif):
		#TODO retourner la nouvelle df

		if not self.__depExist(table, lhs, rhs):#on verifie que la df existe deja
			logging.debug("la dep n'existe pas")
			return False
		
		if whatModif==DfHandler.TABLE:
			logging.debug("appelle __isDep 1: "+" "+newData+" "+lhs+" "+rhs)
			if not self.__isDep(newData, lhs, rhs) or self.__depExist(newData, lhs, rhs):
				logging.debug("nouvelle DF invalide 1")
				return False
			else:
				self.dbh.editTableDep(table, lhs, rhs, newData)
				return True
		
		elif whatModif==DfHandler.RHS:
			logging.debug("appelle __isDep 2: "+" "+table+" "+lhs+" "+newData)
			if not self.__isDep(table, lhs, newData) or self.__depExist(table, lhs, newData):#on verifie que la nouvelle df est bien une df
				logging.debug("nouvelle DF invalide 2")
				return False
			else:#si c'est pas une df
				self.dbh.editRhsDep(table, lhs, rhs, newData)
				return True
		
		elif whatModif==DfHandler.LHS:
			logging.debug("appelle __isDep 3: "+" "+table+" "+newData+" "+rhs)
			if not self.__isDep(table, newData, rhs) or self.__depExist(table, newData, rhs):
				logging.debug("nouvelle DF invalide 3")
				return False
			else:
				self.dbh.ediLhsDep(table, lhs, rhs, newData)
				return True
		
		else:
			logging.debug("whatModif inconnu")
			return False

	def isBcnf(self, table):
		"""
		je selectionne tous les lhs je les split en un tableau 
		il faut qu'une df lhs --> a avec a notIn lhs
		"""
		allLhs=self.dbh.getAllLhs(table)
		allAttributs=self.dbh.getTableAttribute(table)
		for lhs in allLhs:
			lhsTab=lhs.split()
			for attribute in allAttributs:
				if attribute not in lhsTab:
					if not self.isLogicConsequence(table, lhs, attribute,False):
						print(lhs+ " "+attribute)
						return False
		return True

	def getAllTableInFuncDep(self):
		"""
		retourne tous les noms de tables presentes dans la table FuncDep
		"""
		return self.dbh.getAllTableInFuncDep()

	def getDepByRelation(self,relation):

		return self.dbh.getDepByRelation(relation)

	def is3nf(self, table):
		#print("3nf premier: "+str(self.prem3NF(table)))
		#print("3NF lhs: "+str(self.lhs3NF(table)))
		if self.prem3NF(table) or self.lhs3NF(table):
			return True
		else:
			return False

	def prem3NF(self,table):
		# tabCle = self.getCle(table) #tableau de tableau
		# tabAttr = self.dbh.getTableAttribute(table) #tableau avec chaque attribut
		# for i in range(0,len(tabAttr)):
		# 	attr= tabAttr[i]  #un attribut en position i dans la table avec tous les attributs
		# 	for j in range(0,len(tabCle)):
		# 		cle = tabCle[j]  #une clé en position j dans la table contenant les clés
		# 		for h in range(0,len(cle)):
		# 			indice = cle[h]  #un elem de cle
		# 			if indice == attr:
		# 				i += 1
		# 			else:
		# 				j += 1
		# 		j += 1
		# 	return False
		# return True

		attribute = self.dbh.getTableAttribute(table)
		cles = self.getCle(table)
		for att in attribute:
			isInCle=False
			for cle in cles:
				if att in cle:
					isInCle=True
			if not isInCle:
				return False
		return True

	def lhs3NF(self,table):
		tabLhs = self.dbh.getAllLhs(table)
		tabCle = self.getCle(table)
		#print("LHS: "+str(tabLhs))
		#print("cle : "+str(tabCle))
		for i in range(0,len(tabLhs)):
			lhs=tabLhs[i]
			if lhs.split() not in tabCle:
				return False
		return True

	def __getAttributeNeverInRhs(self, table):
		attribute=self.dbh.getTableAttribute(table)
		allRhs=self.dbh.getAllRhs(table)
		never=[]
		for item in attribute:
			if item not in allRhs:
				never.append(item)
		return never


	def __canContinue(self, ligne, nbrAttribute):
		if len(ligne)==0:
			return True
		for cle in ligne:

			if len(cle)>=nbrAttribute:
				return False

		return True

	def __exept(self,A,B):
		"""
		return A\B
		"""
		retour=[]
		for item in A:
			if(item not in B):
				retour.append(item)
		return retour
	def isAKey(self, futureKey, attribute, table):

		att=copy.deepcopy(attribute)
		possibleKey=copy.deepcopy(futureKey)
		result=self.__doFermeture(self.dbh.getDepByRelation(table), possibleKey)
		result.sort()
		att.sort()

		return result == att
	def sansBacN(self, s):
		s2=copy.deepcopy(s)
		if '\n' in s2:
			s2.remove('\n')
		return s2
	def canAddToCle(self, cles, item):
		for cle in cles:
			if self.__isIn(cle, item):
				return False
		return True

	def __recurseCle(self, attribute, cles, supercle, table, debug):
		#print('-----------------------------v')
		#print('in: '+str(supercle))
		if (not self.__canContinue(cles, len(attribute))) or (not self.__canContinue(supercle, len(attribute))):
			return cles, supercle

		
		if len(cles)==0 and len(supercle)==0:
			#print('here1')
			newLine=self.__getAttributeNeverInRhs(table)
			newLine.sort()
			if len(newLine)==0 :
				for i in range(0, len(attribute)):
					it=[attribute[i]]
					it.sort()
					if self.isAKey(it,attribute, table) and self.canAddToCle(cles,[it]):
						if it not in supercle:
							cles.append(it)
					if newLine not in supercle:
						supercle.append(it)
			else:
				if self.isAKey(newLine,attribute, table) and self.canAddToCle(cles, [newLine]) and newLine not in cles:
					cles.append(newLine)
				if newLine not in supercle:
					supercle.append(newLine)
			return self.__recurseCle(attribute, cles, supercle, table, debug)
		

		else:
			newSuperCle=[]
			#print('here2')
			for item in supercle:
				rajout=self.__exept(attribute, item)
				for itemToAdd in rajout:
					new=[itemToAdd]
					new.extend(item)
					new.sort()
					if self.isAKey(new,attribute, table) and self.canAddToCle(cles, new) and new not in cles:
						cles.append(new)
					if new not in newSuperCle:
						newSuperCle.append(new)
				#print(item)
				if self.isAKey(item, attribute, table) and item not in newSuperCle:
					#print('remove')
					newSuperCle.append(item)
			return self.__recurseCle(attribute, cles, newSuperCle, table, debug)

		debug+=1
		if debug==100000000000000000000000000000000000000000000:
			exit()
		#print('out: '+str(supercle))
		#print('-------------------------------------------------------------------------------^')
		

	def getCle(self, table):
		#result=self.getSuperKeyAndKey(table)
		cles,supercle=self.__recurseCle(self.dbh.getTableAttribute(table), [], [], table, 0)
		return cles

	def getSuperCle(self, table):
		cles,supercle=self.__recurseCle(self.dbh.getTableAttribute(table), [], [], table, 0)
		return supercle

	# def cleanKey(self, keys):
	# 	for key in keys:
	# 		if '\n' in key:
	# 			key.remove('\n')

	# def getSuperKeyAndKey(self, table):
	# 	attribute=self.dbh.getTableAttribute(table)
	# 	keyAndSuperKey=self.__recurseCle(attribute, [],[], table, 0)
	# 	keyAndSuperKey.sort(key=len)
	# 	print(keyAndSuperKey)
	# 	keyAndSuperKey.append('XX')

	# 	key=[]
	# 	superKey=[]
	# 	while len(keyAndSuperKey)>1:
	# 		cle=keyAndSuperKey.pop(0)
	# 		key.append(cle)
	# 		index=0
	# 		item=keyAndSuperKey[index]
	# 		while item != 'XX' :
	# 			if self.__isIn(cle, item ):
	# 				keyAndSuperKey.remove(item)
	# 				superKey.append(item)
	# 				item=keyAndSuperKey[index]

	# 			else:
	# 				index+=1
	# 				item=keyAndSuperKey[index]

	# 	self.cleanKey(key)
	# 	self.cleanKey(superKey)
	# 	return key,superKey

	def getCouvertureMinimale(self, table):
		deps=self.dbh.getDepByRelation(table)
		newDeps=[]
		
		#2
		#pour chaque df fermeture( toute les df, et une partie du lhs de la df)
		#si femeture == lhs (selectionnee) on peut la reduire a ça
		# si non on essaye une autre partie du lhs 
		# si tout essayé on peut pas reduire

		for df in deps:
			lhs=df[1].split()
			if len(lhs)==1:
				newDeps.append(df)
			else:
				canReplace=None
				for att in lhs:
					fermeture=self.__doFermeture(deps,lhs)

					if fermeture==[att]:
						canReplace=att
						break
				if canReplace != None:
					newDeps.append([df[0], canReplace, df[2]])
				else:
					newDeps.append(df)

		#3
		deps=newDeps
		newDeps=[]
		for dep in deps:
			if not self.isLogicConsequence(dep[0], dep[1], dep[2],True):# si elle n'est pas redondante
				newDeps.append(dep)#on l'ajoute a la couverture minimale
		return newDeps

	# def getDecomposition3nf(self, table):

	# 	tabcle = self.getCle(table)
	# 	tabcle.sort(key=len)
	# 	#print(str(tabcle))
	# 	tablecouv = self.getCouvertureMinimale(table)
	# 	#print("base :"+str(tablecouv))
	# 	cleanTable= self.cleanDep(tablecouv)
	# 	#print("clean :"+str(tablecouv))
	# 	cleanTable.sort()

	# 	newtable = []
	# 	tableprov = []
	# 	#print("trie: "+str(tablecouv))
		
	# 	tableprov.append(cleanTable[0])
	# 	cleanTable.pop(0)
	# 	for df in cleanTable:
	# 		if df[0] == tableprov[0][0]:
	# 			tableprov.append(df)
	# 		else:
	# 			newtable.append(tableprov)
	# 			tableprov = []
	# 			tableprov.append(df)
	# 	newtable.append(tableprov)
	# 	#print("newTable: "+str(newtable))
		
	# 	tablefus = []
	# 	tableprov = []
	# 	for groupe in newtable:
	# 		tableprov.append(groupe[0][0])
	# 		tableprov.append("-->")
	# 		for df in groupe:
	# 			tableprov.append(df[1])
	# 		tablefus.append(tableprov)
	# 		tableprov = []

	# 	#print("tableau fusion : "+str(tablefus))
		
		

	# 	for rel in tablefus:
	# 		tabtestcle = []
	# 		#print(str(rel)+"ggggggggg")
	# 		for elem in rel:
	# 			#print(str(elem)+"hhhhhhhhh")
	# 			if elem != '-->':
	# 				tabtestcle.append(elem)
	# 				print(str(tabtestcle)+"test")
	# 				for cle in tabcle:
	# 					print(cle)
	# 					if cle[0] == tabtestcle:
	# 						print(tablefus)
	# 						return tablefus
	# 			else:
	# 				break
	# 			tabtestcle =[]
			
		

	# 	tableprov =[]
	# 	relcle =tabcle[len(tabcle)-1]
	# 	if len(relcle) == 1:
	# 		tablefus.append(relcle)
	# 		print("table finals: "+str(tablefus))
	# 		return tablefus
	# 	else:
	# 		tableprov.append(relcle[0])
	# 		relcle.pop(0)

	# 		tableprov.append("-->")
	# 		tableprov.extend(relcle)
	# 		tablefus.append(tableprov)
	# 		print("table final: "+str(tablefus))
	# 		return tablefus
	def createNewDataBase(self,newDataBaseName, data):
		if self.dataBaseName==newDataBase:
			newDataBaseName+='2'
		shutil.copyfile(self.dataBaseName, newDataBase)
		dbhIn=DataBaseHandler(newDataBaseName)
		#dico cle=attribut et value=table
		rep={}
		tables=self.dbh.getTableName()
		for item in tables:
			attributesList=self.dbh.getTableAttribute(item)
			for att in attributesList:
				if att not in rep:
					rep.update({att:item})

		for table in data:
			oldTableName=[]
			attributes=table[1]
			for at in attributes:
				oldTableName.append(rep[at])
			newTableName=table[0]
			if newTableName in tables:
				newTableName+='2'
			dbhIn.createTable(newTableName, attributes, oldTableName)#cree la table et y insere les donnes
			dep=table[2]
			dbhIn.insertDep(dep[0], dep[1], dep[2])


	def getDecomposition3nf(self,table):
		irreductible=self.getCouvertureMinimale(table)
		newDataBase=[]
		keys=self.getCle(table)
		tableid=1
		while len(irreductible)>0:
			table=[str(tableid)]# newDataBase[['numTable', [attributs], ['numTable', lhs, rhs]],[]]
			dep=irreductible.pop(0)
			lhs=dep[1].split()
			rhs=dep[2].split()
			
			attribute=[]
			attribute.extend(lhs)
			attribute.extend(rhs)
			table.append(attribute)
			
			df=[str(tableid), dep[1], dep[2]]
			table.append(df)

			newDataBase.append(table)
			tableid+=1;
		doBreak=False
		for cle in keys:
			for table in newDataBase:
				if not self.__isIn(cle, table[1]):
					newDataBase.append([str(tableid), cle, []])
					doBreak=True
					break
			if doBreak:
				break
		return newDataBase

	def cleanDep(self, table):
		
		for df in table:
			df.pop(0)
		return table














		# deps=self.dbh.getDepByRelation(table)
		# cles=self.getCle(table)
		# table=[]
		# newTable=[]
		# for dep in deps:
		# 	cleanDep=dep[1].split()
		# 	cleanDep.append(dep[2])
		# 	if cleanDep not in table:
		# 		table.append(cleanDep)
		# for cle in cles:
		# 	if cle not in table:
		# 		table.append(cle)
		# table.sort(key=len)
		# print(table)
		# while len(table)>0:
		# 	elem=table.pop(0)
		# 	isInclude=False
		# 	for item in table:
		# 		if len(item)>len(elem) and self.__isIn(elem, item):
		# 			isInclude=True
		# 			break
		# 	if not isInclude:
		# 		newTable.append(elem)


		print('Decomposition 3nf:'+str(newTable))

	def closeDataBase(self):
		self.dbh.closeDataBase()


	def satisfaitPasDF(self, table, lhs, rhs):
		"""
		retourne les lignes qui ne satisfont pas la df (table, lhs, rhs)
		"""

		if self.__depExist(table, lhs, rhs):
			return self.dbh.DFisOk(table, lhs, rhs)
		else:
			return None

	def getInutileDF(self, table, lhs, rhs):
		
		#si table et lhs et rhs valent None, regarde pour une df
		
		notDf=[]
		isConsequenceLogic=[]
		pasRespectee=[]#[[table, lhs, rhs, [ligne qui ne respenctent pas la df]], [], [], ..., []]
		if table==None and lhs==None and rhs == None:
			allDf=dbh.getAllDep()
			for dep in allDf:
				if not self.__isDep(dep[0], dep[1], dep[2]):
					notDf.append(dep)
				elif self.isLogicConsequence(dep[0], dep[1], dep[2], True):
					logic.append(dep)
				elif len(self.satisfaitPasDF(dep[0], dep[1], dep[2]))!=0:
					retour=self.satisfaitPasDF(dep[0], dep[1], dep[2])
					tab=[dep, retour]
					pasRespectee.append(tab)
		elif table!= None and lhs!= None and rhs!= None:
			if not self.__depExist(table, lhs, rhs):
				notDf.append([table, lhs, rhs])
			elif self.isLogicConsequence(table, lhs, rhs, True):
				isConsequenceLogic.append([table, lhs, rhs])
			elif len(self.satisfaitPasDF(table, lhs, rhs)) !=0:
				pasRespectee.append([table, lhs, rhs, self.satisfaitPasDF(table, lhs, rhs)])

		return notDf, isLogicConsequence, pasRespectee
			

	def isLogicConsequence(self,table, lhs, rhs, remove):

		if self.__depExist(table,lhs,rhs):
			ens=self.dbh.getDepByRelation(table)
			if remove:
				ens.remove([table,lhs,rhs])
			result=self.__doFermeture(ens,lhs.split())

			return rhs in result
		else:
			return None

	# def __doFermeture(self, dFs, x):
	# 	"""
	# 	retourne la fermeture de l'ensemble x d'attribut par rapport a un ensemble dfs de DFs
	# 	"""
	# 	print('IN FERMETURE ----------------------------------------------------------------------------')
	# 	reste=copy.deepcopy(dFs)#ensemble de tuple ( DF )
	# 	fermeture=copy.deepcopy(x) #ensemble d'attributs
	# 	print('receive reste: '+str(reste))
	# 	print('receive fermeture '+str(fermeture))
	# 	print('rentre boucle --------------------------------------------------------------------------------')
	# 	while len(reste)>0:
	# 		couple=reste[0]
	# 		w=couple[1]
	# 		z=couple[2]
	# 		print('w= '+w)
	# 		print('z= '+z)
	# 		print('fermeture: '+str(fermeture))
	# 		if self.__isIn(w.split(),fermeture):
	# 			print('w is in fermeture')
	# 			reste.remove(couple)
	# 			if z not in fermeture:
	# 				fermeture.append(z)
	# 		else:
	# 			break
	# 		print('fermeture apres '+str(fermeture))
		# 	return fermeture
	def __doFermeture(self, dFs, x):
		df=copy.deepcopy(dFs)
		newDep=copy.deepcopy(x)
		oldDep=None

		while oldDep != newDep:
			oldDep=copy.deepcopy(newDep)
			for item in df:
				w=item[1]
				z=item[2]

				if self.__isIn(w.split(), newDep):
					if z not in newDep:
						newDep.append(z)
		return newDep

	def __isIn(self,small, big):
		"""
		Return True if small is in big else return False
		"""
		for sItem in small:
			sItemIsInBig=False
			for bItem in big:
				if sItem==bItem:
					sItemIsInBig=True
			if sItemIsInBig==False:
				return False
		return True