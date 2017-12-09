from DataBaseHandler import DataBaseHandler
import logging
#TODO mettre un s a exist
#TODO verifier idDep et depExist
#TODO isLogicConsequence mauvais

logging.basicConfig(filename='logs/log1.log',level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
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
		
	def depExist(self, table, lhs, rhs):
		r=self.dbh.getOneDep(table, lhs, rhs)
		logging.debug("retour de getOneDep: "+str(r)+" "+str(type(r)))
		return self.isDep(table, lhs, rhs) and r != None and len(r) == 3

	def removeDep(self, table, lhs, rhs):
		if self.depExist(table, lhs, rhs):
			self.dbh.removeDep(table, lhs, rhs)
			return True	
		else:
			return False
		

	def getAllDep(self):
		return self.dbh.getAllDep()

	def insertDep(self, table, lhs, rhs):
		if self.isDep(table, lhs, rhs): #depExist ne retourne pas True ou False donc bug
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
			logging.debug("la dep n'existe pas")
			return False
		if whatModif==DfHandler.TABLE:
			logging.debug("appelle isDep 1: "+" "+newData+" "+lhs+" "+rhs)
			if not self.isDep(newData, lhs, rhs):
				logging.debug("nouvelle DF invalide 1")
				return False
			else:
				self.dbh.editTableDep(table, lhs, rhs, newData)
				return True
		elif whatModif==DfHandler.RHS:
			logging.debug("appelle isDep 2: "+" "+table+" "+lhs+" "+newData)
			if not self.isDep(table, lhs, newData):#on verifie que la nouvelle df est bien une df
				logging.debug("nouvelle DF invalide 2")
				return False
			else:#si c'est pas une df
				self.dbh.editRhsDep(table, lhs, rhs, newData)
				return True
		elif whatModif==DfHandler.LHS:
			logging.debug("appelle isDep 3: "+" "+table+" "+newData+" "+rhs)
			if not self.isDep(table, newData, rhs):
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
		il faut qu'une df lhs --> a avec a in table existe et a notIn lhs
		"""
		allLhs=self.dbh.getAllLhs(table)


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
		if depExist(table, lhs, rhs):
			return self.dbh.DFisOk(table, lhs, rhs)
		else:
			return None
		
	def getInutileDF(self):
		pass
	
	def isLogicConsequence(this,table, lhs, rhs):
		ens=self.dbh.getTableAttribute(table)
		result=self.doFermeture(ens,lhs)
		return rhs in result

	def doFermeture(dFs, x):
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

	def isIn(small, big):
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
