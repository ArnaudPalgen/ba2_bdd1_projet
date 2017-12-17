# coding: utf-8
from DataBaseHandler import DataBaseHandler
import logging
import copy
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
			lhsTab=lhs.split()
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
			for cle in cles:
				if att in cle:
					# print(att)
					# print(cle)
					return True
		return False

	def lhs3NF(self,table):
		tabLhs = self.dbh.getAllLhs(table)
		tabCle = self.getCle(table)
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

	def getDecomposition3nf(self):
		pass

	def sortDep(self, table):
		df=self.dbh.getDepByRelation(table)
		for dep in df:
			dep.pop(0)
		df.sort()

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
			# print('in consequence')
			# print(result)
			# print(rhs)

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
		#print('dfs: '+str(df))
		#print('attributs: '+str(newDep))

		while oldDep != newDep:
			oldDep=copy.deepcopy(newDep)
			for item in df:
				w=item[1]
				z=item[2]
				# print('-----------------------------')
				# print('w |'+w+'|')
				# print('z '+ z)
				# print('newDep: '+str(newDep))
				# print('-----------------------------')
				if self.__isIn(w.split(), newDep):
					#print('w is in newDep')
					if z not in newDep:
						newDep.append(z)
		#print('fin '+str(newDep))
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