from DataBaseHandler import DataBaseHandler
import logging
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
			lhsTab=lhs[0].split()
			for attribute in allAttributs:
				if attribute not in lhsTab:
					if not self.isLogicConsequence(table, lhs, attribute):

						return False
		return True

	def getAllTableInFuncDep(self):
		"""
		retourne tous les noms de tables presentes dans la table FuncDep
		"""
		return self.dbh.getAllTableInFuncDep()

	def is3nf(self, table):
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
				cle = tableCle[j]
				for h in range(0:len(cle)):
					indice = cle[h]
					if indice == attr:
						i += 1
					else:
						j += 1
				j += 1
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

	def __getAttributeNeverInRhs(self, table):
		attribute=self.dbh.getTableAttribute(table)
		allRhs=self.dbh.getAllRhs(table)
		never=[]
		for item in attribute:
			if item not in allRhs:
				never.append(item)
		return never


	def __iterIsFinish(self, ligne, nbrAttribute):
		for tab in ligne:
			if('\n' not in tab or len(tab)==nbrAttribute ):#condition d'arret
				return False
		return True

	def __exept(self,A,B):
		"""
		return A\B
		"""

		for item in B:
			if(item in A):
				A.remove(item)
		return A

	def __recurseCle(self, attribute, cles, table):
		
		if self.__iterIsFinish(cles, len(attribute)):
			return cles
		if len(cles)==0:
			cles.append(attribute[0])
		else:
			newLine=[]
			for item in cles:
				if '\n' in item or len(item)==len(attribute):
					newLine.append(item)
				#verifier que la branche ne contient pas le caractere de fin
				#attribut sauf item
				else:
					rajout=self.__exept(attribute, item)
					for itemToAdd in rajout:
						new=[itemToAdd]
						new.extend(item)
						newLine.append(new)

			for item in newLine:
				if '\n' not in item and len(item)!= len(attribute):
					lhs=''
					for lhsMember in item:
						lhs+=lhsMember
						lhs+=' '
					lhs=lhs[0:len(lhs)-1]
					isCle=True
					for att in attribute:
						if not self.isLogicConsequence(table, lhs, att):
							isCle=False
							break
					if isCle:
						item.append('\n')

			self.__recurseCle(attribute, newLine, table)


	def getCle(self, table):
		inCle=self.__getAttributeNeverInRhs(table)
		attribute=self.dbh.getTableAttribute(table)
		print(attribute)
		print(inCle)
		print(table)
		return self.__recurseCle(attribute, inCle, table)



	def getSuperCle(self):
		pass
	def getDecomposition3nf(self):
		pass
	def getDecompositionBcnf(self):
		pass
	def satisfaitPasDF(self, table, lhs, rhs):
		if self.__depExist(table, lhs, rhs):
			return self.dbh.DFisOk(table, lhs, rhs)
		else:
			return None
		
	def getInutileDF(self):
		pass
	

	def isLogicConsequence(self,table, lhs, rhs):

		if self.__depExist(table,lhs,rhs):
			ens=self.dbh.getDepByRelation(table)
			ens.remove([table,lhs,rhs])
			result=self.__doFermeture(ens,lhs.split())

			return rhs in result
		else:
			return None

	def __doFermeture(self, dFs, x):
		"""
		retourne la fermeture de l'ensemble x d'attribut par rapport a un ensemble dfs de DFs
		"""
		reste=dFs#ensemble de tuple ( DF )
		fermeture=x #ensemble d'attributs
		for couple in reste:

			w=couple[1]
			z=couple[2]
			if self.__isIn(w.split(),fermeture):
				reste.remove(couple)
				fermeture.append(z)
		return fermeture

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
