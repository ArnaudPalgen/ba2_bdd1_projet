from DataBaseHandler import DataBaseHandler
#TODO mettre un s a exist
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
			return False
		
		listeAttributs=self.dbh.getTableAttribute(table)# liste des attributs de la table
		
		#verifie que les noms dans lhs sont des attributs de la tabe
		sLhs=lhs.split(' ')
		correct=False
		for item in sLhs:
			if item != ' ' and item not in listeAttributs:
				return False

		#verifie que rhs ne contient qu'un element 
		if rhs.count(' ') !=0:
			return False
		
		#verifie que rhs est un attribut de la table
		if rhs not in listeAttributs:
			return False

		return True
		
def __depExist(self, table, lhs, rhs):
		return self.isDep(table, lhs, rhs) and len(self.dbh.getOneDep(table, lhs, rhs)) == 1

	def removeDep(self, table, lhs, rhs):
		if self.depExist(table, lhs, rhs):
			self.dbh.removeDep(table, lhs, rhs)
			return True	
		else:
			return False
		

	def getAllDep(self):
		return self.dbh.getAllDep()

	def insertDep(self, table, lhs, rhs):
		if self.depExist(table, lhs, rhs): #depExist ne retourne pas True ou False donc bug
			r=self.dbh.insertDep(table, lhs, rhs)
			if r != None:#TODO verifier que r contient quelque chose
				return True
			else:
				return False

		else:
			return False

	def editDep(self, table, lhs, rhs, newData,whatModif):
		#TODO retourner la nouvelle df
		if not self.depExist(table, lhs, rhs):#on verifie que la df existe deja
			return False
		if whatModif==TABLE:
			if not self.isDep(newData, lhs, rhs):
				return False
			else:
				self.dbh.editTableDep(table, lhs, rhs, newData)
				return True
		elif whatModif==RHS:
			if not self.isDep(table, lhs, newData):#on verifie que la nouvelle df est bien une df
				return False
			else:#si c'est pas une df
				self.dbh.editRhsDep(table, lhs, rhs)
				return True
		elif whatModif==LHS:
			if not self.isDep(table, newData, rhs):
				return False
			else:
				self.dbh.ediLhsDep(table, lhs, rhs, newData)
				return True
		else:
			return False

	def isBcnf(self, table, lhs, rhs):
		pass
	def is3nf(self, table, lhs, rhs):
		pass
	def getCle(self):
		pass
	def getSuperCle(self):
		pass
	def getDecomposition3nf(self):
		pass
	def getDecompositionBcnf(self):
		pass
	def satisfaitDF(self, table, lhs, rhs):
		
		pass
	def getInutileDF(self):
		pass
	
	def isLogicConsequence(this,table, lhs, rhs):
		ens=self.dbh.getTableAttribute(table)
		result=self.doFermeture(ens,lhs)
		return rhs in result

	def __doFermeture(dFs, x):
		"""
		
		"""
		reste=dFs#ensemble de tuple ( DF )
		fermeture=x #ensemble d'attributs
		for couple in reste:
			w,z=couple
			if self.isIn(w,fermeture):
				reste.remove(couple)
				fermeture.append(z)
		return fermeture

	def __isIn(small, big):
		"""
		Return True if small is in big else return False
		"""
		for sItem in small:
			sItemIsInBig=False
			for bItem in big:
				if sItem==bItem:
					sItemIsInBig=True
					break
			if sItemIsInBig==False:
				return False
		return True
