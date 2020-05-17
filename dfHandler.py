# coding: utf-8
from DataBaseHandler import DataBaseHandler
import logging
import shutil
import copy

class DfHandler():
	"""docstring for DfHandler"""
	TABLE='table'
	LHS='lhs'
	RHS='rhs'
	def __init__(self, dataBase):
		
		"""
		Parametre: une dataBase
		"""
		self.dbh=DataBaseHandler(dataBase)
		self.dataBaseName=dataBase

	def __isDep(self,table, lhs, rhs):
		"""
		Parametres: lhs et rhs str nettoyés !!
		Return True si la table existe, lhs et rhs sont des attributs de la table
		"""
		
		listeTable=self.getTableName()
		
		if table not in listeTable:
			return False
		listeAttributs=self.dbh.getTableAttribute(table)# liste des attributs de la table
		

		#verifie que les noms dans lhs sont des attributs de la table
		sLhs=lhs.split()
		
		for item in sLhs:
			if item not in listeAttributs:
				return False


		#verifie que rhs ne contient qu'un element 
		if rhs.count(' ') !=0:
			return False
		

		#verifie que rhs est un attribut de la table
		if rhs not in listeAttributs:
			return False
		return True
		
	def __depExist(self, table, lhs, rhs):

		"""
		Parametres: une certaine df
		Return True si la df existe, False sinon
		"""

		r=self.dbh.getOneDep(table, lhs, rhs)
		return r != None and len(r) == 3

	def removeDep(self, table, lhs, rhs):
		
		"""
		Parametres: une certaine df
		Return True si la df a bien ete supprimee, False sinon
		"""
		#verifie que la df a bien ete supprimee
		if self.__depExist(table, lhs, rhs):
			self.dbh.removeDep(table, lhs, rhs)
			return True	
		else:
			return False
		
	def getAllDep(self):

		"""
		Return toutes les dependances de FuncDep
		"""
		return self.dbh.getAllDep()

	def insertDep(self, table, lhs, rhs):

		"""
		Parametres: une certaine df
		Return True si la df a pu etre ajoutee, False sinon
		"""
		if self.__isDep(table, lhs, rhs) and not self.__depExist(table, lhs, rhs):
			r=self.dbh.insertDep(table, lhs, rhs)
			if r != None:
				return True
			else:
				return False

		else:
			return False

	def editDep(self, table, lhs, rhs, newData,whatModif):
		
		"""
		Parametre : une certaine df, la nouvelle donnee, ce qui doit etre modifie
		Return True si la df a pu etre modifiee, False sinon
		"""

		#on verifie que la df existe
		if not self.__depExist(table, lhs, rhs):#on verifie que la df existe deja
			return False
		
		#pour la modif de la table
		if whatModif==DfHandler.TABLE:
			if not self.__isDep(newData, lhs, rhs) or self.__depExist(newData, lhs, rhs):
				return False
			else:
				self.dbh.editTableDep(table, lhs, rhs, newData)
				return True
		
		#pour la modif du Rhs 
		elif whatModif==DfHandler.RHS:
			if not self.__isDep(table, lhs, newData) or self.__depExist(table, lhs, newData):#on verifie que la nouvelle df est bien une df
				return False
			else:#si c'est pas une df
				self.dbh.editRhsDep(table, lhs, rhs, newData)
				return True
		
		#pour modif Lhs
		elif whatModif==DfHandler.LHS:
			if not self.__isDep(table, newData, rhs) or self.__depExist(table, newData, rhs):
				return False
			else:
				self.dbh.ediLhsDep(table, lhs, rhs, newData)
				return True
		
		#Modif inconnu
		else:
			return False

	def isBcnf(self, table):
		"""
		je selectionne tous les lhs je les split en un tableau 
		il faut qu'une df lhs --> a avec a notIn lhs
		Return True si c'est en BCNF, False sinon
		"""
		allLhs=self.dbh.getAllLhs(table)
		allAttributs=self.dbh.getTableAttribute(table)
		for lhs in allLhs:
			lhsTab=lhs.split()
			for attribute in allAttributs:
				if attribute not in lhsTab:
					if not self.isLogicConsequence(table, lhs, attribute,False):
						return False
		return True

	def getAllTableInFuncDep(self):
		"""
		Return tous les noms de tables presentes dans la table FuncDep
		"""
		return self.dbh.getAllTableInFuncDep()
	
	def getTableName(self):

		"""
		Return tous les noms de table present dans la base de donnee
		"""

		return self.dbh.getTableName()

	def getDepByRelation(self,table):

		"""
		Parametre: une table
		Return toutes les dependances concernant cette table
		"""

		return self.dbh.getDepByRelation(relation)

	def is3nf(self, table):

		"""
		Parametre: une table
		Return True si c'est en 3NF, False sinon
		"""
				
		if self.prem3NF(table) or self.lhs3NF(table):
			return True
		else:
			return False

	def prem3NF(self,table):
		
		"""
		Parametre: une table
		Return True si tous les attributs sont dans au moins une cle, False sinon
		"""
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

		"""
		Parametre: une table
		Return True si tous les Lhs sont des cles, False sinon
		"""
		
		tabLhs = self.dbh.getAllLhs(table)
		tabCle = self.getCle(table)
			
		for i in range(0,len(tabLhs)):
			lhs=tabLhs[i]
			
			if lhs.split() not in tabCle:
				return False
		return True

	def __getAttributeNeverInRhs(self, table):
		
		"""
		Parametre: une table
		Return tous les attributs de cette table n'etant pas dans les Rhs des df associees a la table
		"""
		attribute=self.dbh.getTableAttribute(table)
		allRhs=self.dbh.getAllRhs(table)
		never=[]
		for item in attribute:
			if item not in allRhs:
				never.append(item)
		return never

	def __canContinue(self, ligne, nbrAttribute):

		"""
		Parametre: ligne -> ligne courante de la cle, nbrAttribute -> nombre total d'attribut
		Return True si on peut continuer, False sinon
		"""
		
		if len(ligne)==0:
			return True
		for cle in ligne:

			if len(cle)>=nbrAttribute:
				return False

		return True

	def __exept(self,A,B):
		
		"""
		Parametre: 2 arguments
		Return A\B
		"""
		retour=[]
		for item in A:
			if(item not in B):
				retour.append(item)
		return retour
	
	def isAKey(self, futureKey, attribute, table):

		"""
		Parametre: une possible cle, un attribut, une table
		Return True si c'est une cle, False sinon
		"""

		att=copy.deepcopy(attribute)
		possibleKey=copy.deepcopy(futureKey)
		result=self.__doFermeture(self.dbh.getDepByRelation(table), possibleKey)
		result.sort()
		att.sort()

		return result == att
	
	def sansBacN(self, s):
		
		"""
		Parametre : un nom
		Return le nom sans \n
		"""
		s2=copy.deepcopy(s)
		if '\n' in s2:
			s2.remove('\n')
		return s2
	
	def canAddToCle(self, cles, item):
		
		"""
		Parametre : une cle, un tableau
		Return True si la cle peut etre ajoutee, False sinon
		"""

		for cle in cles:
			if self.__isIn(cle, item):
				return False
		return True

	def __recurseCle(self, attribute, cles, supercle, table):
		
		"""
		Parametre: un attribut, une cle, une supercle et une table
		Return les cles et supercles
		"""		
		if (not self.__canContinue(cles, len(attribute))) or (not self.__canContinue(supercle, len(attribute))):
			return cles, supercle

		
		if len(cles)==0 and len(supercle)==0:
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
			return self.__recurseCle(attribute, cles, supercle, table)
		

		else:
			newSuperCle=[]
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
				if self.isAKey(item, attribute, table) and item not in newSuperCle:
					newSuperCle.append(item)
			return self.__recurseCle(attribute, cles, newSuperCle, table)

	def getCle(self, table):
		
		"""
		Parametre : une table
		Return les cles de la table
		"""
		cles,supercle=self.__recurseCle(self.dbh.getTableAttribute(table), [], [], table)
		return cles

	def getSuperCle(self, table):
		
		"""
		Parametre: une table
		Return les supercles
		"""

		cles,supercle=self.__recurseCle(self.dbh.getTableAttribute(table), [], [], table)
		return supercle

	def getCouvertureMinimale(self, table):
		
		"""
		Parametre: une table
		Return la couverture minimale ('ensemble irreductible de df')
		"""
		deps=self.dbh.getDepByRelation(table)
		newDeps=[]
		
		#pour chaque df fermeture( toute les df, et une partie du lhs de la df)
		#si femeture == lhs (selectionnee) on peut la reduire a ça
		#si non on essaye une autre partie du lhs 
		#si tout essayé on ne peut pas reduire

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

		deps=newDeps
		newDeps=[]
		for dep in deps:
			if not self.isLogicConsequence(dep[0], dep[1], dep[2],True):# si elle n'est pas redondante
				newDeps.append(dep)#on l'ajoute a la couverture minimale
		return newDeps

	def createNewDataBase(self,newDataBaseName, data):
		
		"""
		Parametre : un nom de DataBase, des donnees
		Cree une nouvelle base de donnee avec les tables issues de la decomposition en 3NF
		"""

		if self.dataBaseName==newDataBaseName:
			newDataBaseName+='2'
		shutil.copyfile(self.dataBaseName, newDataBaseName)

		dbhIn=DataBaseHandler(newDataBaseName)
		dbhIn.dropTable('FuncDep')
		dbhIn.closeDataBase()
		dbhIn=DataBaseHandler(newDataBaseName)
		rep={}
		tables=self.getTableName()
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

			dbhIn.createTable(newTableName, attributes, oldTableName)#cree la table et y insere les donnees
			dep=table[2]
			if len(dep)==3:
				dbhIn.insertDep(dep[0], dep[1], dep[2])
		dbhIn.removeOldTable(oldTableName)

	def getDecomposition3nf(self,table):

		"""
		Parametre: une table
		Return la decomposition en 3NF de la table
		"""
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

		"""
		Parametre : une table
		Return les df de cette table sans le parametre table dedans
		"""
		
		for df in table:
			df.pop(0)
		return table

	def closeDataBase(self):
		
		"""
		ferme la base de donnee
		"""
		self.dbh.closeDataBase()

	def satisfaitPasDF(self, table, lhs, rhs):
		
		"""
		Parametre: une certaine df
		Return les lignes qui ne satisfont pas la df (table, lhs, rhs)
		"""

		if self.__depExist(table, lhs, rhs):
			return self.dbh.DFisOk(table, lhs, rhs)
		else:
			return None

	def getInutileDF(self, table=None, lhs=None, rhs=None):
		
		"""
		Parametre: une certaine df
		Return les df qui sont inutiles (celles dont des arguments n'existent plus, les conséq logiques et celle qi ne respectent pas la table)
		"""
		#si table et lhs et rhs valent None, regarde pour une df
		notDf=[]
		isConsequenceLogic=[]
		pasRespectee=[]#[[table, lhs, rhs, [ligne qui ne respenctent pas la df]], [], [], ..., []]
		if table==None and lhs==None and rhs == None:
			allDf=self.dbh.getAllDep()
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

		return notDf, isConsequenceLogic, pasRespectee
			
	def isLogicConsequence(self,table, lhs, rhs, remove):

		"""
		Parametre: une certaine df et un booleen
		retourn True si elle est une conséq logique, False sinon
		"""
		if self.__depExist(table,lhs,rhs):
			ens=self.dbh.getDepByRelation(table)
			if remove:
				ens.remove([table,lhs,rhs])
			result=self.__doFermeture(ens,lhs.split())

			return rhs in result
		else:
			return None
	
	def __doFermeture(self, dFs, x):
		
		"""
		Parametre : une df et un attribut
		Return la fermeture de l'ensemble d attribut par rapport a l'ensemble de df
		"""

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
		Parametre: 1 element inclus dans un autre
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