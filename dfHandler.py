from DataBaseHandler import DataBaseHandler
class DfHandler():
	"""docstring for DfHandler"""
	TABLE='table'
	LHS='lhs'
	RHS='rhs'
	def __init__(self, dataBase):
		self.dbh=DataBaseHandler(dataBase)


	def isDep(self,table, lhs, rhs):
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
	def depExist(self, table, lhs, rhs):
		return isDep(table, lhs, rhs) and self.dbh.getOneDep(table, lhs, rhs)==1

	def removeDep(self, table, lhs, rhs):
		if isDep(table, lhs, rhs):
			self.dbh.removeDep(table, lhs, rhs)
			return 
		else:
			return True
		

	def insertDep(self, table, lhs, rhs):
		if depExist(table, lhs, rhs):
			return self.dbh.insertDep(table, lhs, rhs)
		else:
			return None
	def editDep(self, table, lhs, rhs, newData,whatModif):
		if  not depExist(table, lhs, rhs):
			return None
		#TODO verifier que newData est un attribut
		if whatModif==TABLE:
			
		elif whatModif==RHS:
			pass
		elif whatModif==LHS:
			pass
		else:
			return None

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
	def satisfaitDF(self, table, rhs, lhs):
		pass
	def getInutileDF(self):
		pass
	
	def isLogicConsequence(this,table, lhs, rhs):
		ens=self.dbh.getTableAttribute(table)
		result=doFermeture(ens,lhs)
		return rhs in result

	def __doFermeture(dFs, x):
		"""
		
		"""
		reste=dFs#ensemble de tuple ( DF )
		fermeture=x #ensemble d'attributs
		for couple in reste:
			w,z=couple
			if isIn(w,fermeture):
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