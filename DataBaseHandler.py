# coding: utf-8
import sqlite3

class DataBaseHandler:
	"""Gestionnaire de la base de donnees"""
	
	def __init__(self, dataBase):
		""" Constructeur de DataBaseHandler """

		self.db=sqlite3.connect(dataBase)
		self.cursor=self.db.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.db.commit()

	def __dataOK(*param):
		"""
		raise TypeError si un des parametres n'est pas du type str
		"""
		for item in param:
			if(type(item)!=str):
				raise TypeError("Le type du parametre n'est pas str")


	def insertDep(self,table, lhs, rhs):
		DataBaseHandler.__dataOK(table, lhs, rhs)
		""" 
		Insere une DF dans la table FuncDep

			Param: 
					table: la table a laquelle appartient la DF
					lhs: le membre de gauche de la DF
					rhs: lemembre de droite de la DF 
			Return: la DF inseree

		"""
		self.cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES(?, ?, ?) """, (table, lhs, rhs) )
		self.db.commit()
		self.cursor.execute("""SELECT * FROM FuncDep WHERE Funcdep.'table'=? AND lhs=? AND rhs=? """, (table, lhs, rhs))
		tab=[]
		retour=self.cursor.fetchone()
		for item in retour:
			tab.append(item)
		return tab


	def removeDep(self,table, lhs, rhs):
		DataBaseHandler.__dataOK(table, lhs, rhs)

		""" 
		Supprime une DF dans la table FuncDep

			Param: 
					table: la table a laquelle appartient la DF
					lhs: le membre de gauche de la DF
					rhs: lemembre de droite de la DF 


		"""

		self.cursor.execute("""DELETE FROM FuncDep WHERE FuncDep.'table'=? AND lhs=? AND rhs=?""", (table, lhs, rhs) )
		self.db.commit()


	def editTableDep(self,table, lhs, rhs, newTable):
		DataBaseHandler.__dataOK(table, lhs, rhs, newTable)

		""" 
		Modifie la table d'une DF dans la table FuncDep

			Param: 
					table: la table a laquelle appartient la DF
					lhs:  le membre de gauche de la DF
					rhs:  lemembre de droite de la DF
					newTable: le nom de la nouvelle table 
			Return: la DF modifiee TODO


		"""
		self.cursor.execute(""" UPDATE FuncDep SET Funcdep.'table'=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newTable, table, lhs, rhs))
		self.db.commit()

	def ediLhsDep(self,table, lhs, rhs, newLhs):
		DataBaseHandler.__dataOK(table, lhs, rhs, newLhs)

		""" 
		Modifie la partie de gauche d'une DF dans la table FuncDep

			Param: 
					table: la table a laquelle appartient la DF
					lhs: le membre de gauche de la DF
					rhs: lemembre de droite de la DF
					newLhs, le nom de la nouvelle partie de gauche de la DF 
			Return: la DF modifiee TODO


		"""
		self.cursor.execute(""" UPDATE FuncDep SET lhs=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newLhs, table, lhs, rhs))
		self.db.commit()

	def editRhsDep(self,table, lhs, rhs, newRhs):
		DataBaseHandler.__dataOK(table, lhs, rhs, newRhs)

		""" 
		Modifie la partie de droite d'une DF dans la table FuncDep

			Param: 
					table: la table a laquelle appartient la DF
					lhs: le membre de gauche de la DF
					rhs: lemembre de droite de la DF
					newRhs, le nom de la nouvelle partie de droite de la DF 
			Return: la DF modifiee TODO


		"""
		self.cursor.execute(""" UPDATE FuncDep SET rhs=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newRhs, table, lhs, rhs))
		self.db.commit()

	def getTableName(self):
		""" 
		Retourne le nom de toutes les tables de la base de donnees 

			Return: Un tableau contenant les noms de toutes les tables de la base de donee
		"""
		self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' """)
		retour=[]
		for data in self.cursor:
			retour.append(data[0])
		return retour

	def getTableAttribute(self,tableName):
		DataBaseHandler.__dataOK(tableName)
		""" 
		Retourne les attributs d'une table de la base de donnee

			Param: tableName: le nom de la table
			Return: Un tableau contenant le noms des attributs de la table TableName

		"""
		retour=[]
		s="""PRAGMA table_info("""
		s+=tableName
		s+=""")"""
		self.cursor.execute(s);
		for rows in self.cursor:
			retour.append(rows[1])
		return retour

	def getOneDep(self, table, lhs, rhs):
		DataBaseHandler.__dataOK(table, lhs, rhs)
		"""
		Retourne une DF si elle existe. Si non retourne un tableau vide

			Param: 
					table: la table a laquelle appartient la DF
					lhs: le membre de gauche de la DF
					rhs: lemembre de droite de la DF

			Return: un tableau contenant la DF. Si elle n'existe pas, le tableau est vide
		"""
		self.cursor.execute("""SELECT * FROM FuncDep WHERE FuncDep.'table'=? AND lhs=? AND rhs=? """, (table, lhs, rhs))
		retour=[]
		result = self.cursor.fetchone()
		if result==None:
			return None
		else:
			for item in result:
				retour.append(item)
			return retour

	def getDepByRelation(self,relation):
		DataBaseHandler.__dataOK(relation)
		""" 
		Retourne toutes les DF d'une table

			Param: relation un nom d'une table de la base de donnee
			Return: un tableau contenant toutes les DFs associees a la table relation

		"""
		self.cursor.execute("""SELECT * FROM FuncDep WHERE FuncDep.'table'=?  """, (relation,))	
		retour=[]
		for tuples in self.cursor:
			l=[]
			for item in tuples:
				l.append(item)
			retour.append(l)

			
		return retour
	def closeDataBase(self):
		"""
		Ferme la base de donnee
		"""
		self.db.close()
		cursor=None

	def getAllDep(self):
		""" 
		Retourne toutes les DF de la table FuncDep

			Return: Un tableau a deux dimensions ou chaque ligne est une DF

		"""
		retour=[]

		self.cursor.execute(""" SELECT * FROM FuncDep""")

		for items in self.cursor:
			l=[]
			for element in items:
				l.append(element)
			retour.append(l)

		return retour
	def DFisOk(self,table, lhs, rhs):
		DataBaseHandler.__dataOK(table, lhs, rhs)
		"""
		retoune les tuples de la table table qui ne respectent pas la df lhs--> rhs
		lhs est un tuple d'attributs et rhs un str ne contenant qu'un attribut
		Param: 
			table: la table a laquelle appartient la DF
			lhs: le membre de gauche de la DF
			rhs: lemembre de droite de la DF
		"""
		
		if type(lhs)==str:
			lhsTab=lhs.split()

		s="SELECT t1.*, t2."+rhs+" FROM "+table+" t1, "+table+" t2 WHERE "
		for attribute in lhsTab:
			s+="t1."+attribute+" == t2."+attribute+" AND "
		s+="t1."+rhs+" != t2."+rhs
		self.cursor.execute(s)

		retour=[]
		for tuples in self.cursor:
			line=[]
			for item in tuples:
				line.append(item)
			line.pop()
			retour.append(line)
		return retour

	def getAllLhs(self, table):
		DataBaseHandler.__dataOK(table)
		"""
		retourne tous les lhs pour une table donnee
		Param:
			table: la table pour laquelle les lhs seront retournes
		"""

		self.cursor.execute(""" SELECT lhs FROM FuncDep WHERE FuncDep.'table' == ? """ ,(table,))
		retour=[]

		for item in self.cursor:
			retour.append(item[0])
		return retour

	def getAllRhs(self, table):
		DataBaseHandler.__dataOK(table)
		"""
		retourne tous les lhs pour une table donnee
		Param:
			table: la table pour laquelle tous les rhs seront retournes
		"""

		self.cursor.execute(""" SELECT rhs FROM FuncDep WHERE FuncDep.'table' == ? """ ,(table,))
		retour=[]

		for item in self.cursor:
			retour.append(item[0])
		return retour

	def getAllTableInFuncDep(self):
		"""
		retourne tous les noms de tables presentes dans la table FuncDep
		"""
		self.cursor.execute(""" SELECT DISTINCT FuncDep.'table' FROM FuncDep""")
		retour=[]
		for item in self.cursor:
			retour.append(item[0])
		return retour
	def metadataOfAttribute(self, table, attributeName):
		"""
		Rretourne les caracteristiques (cid, tableName, type, not null, default value, primary key ) d'un attribut donne d'une table donnee
		Param:
			table: la table qui contient l'attribut
			attributeName: l'attribut pour lequel on souhaite obtenir les caracteristiques
		"""
		s="""PRAGMA table_info("""+table+""")"""
		caracts=self.cursor.execute(s)
		for caract in self.cursor:
			if caract[1]==attributeName:
				return caract
		return None
	def createTable(self, tableName, attribute, oldTableName):
		"""
		Cree un nouvelle table et y insere les donnees des attributs correspondants
		Param:
			tableName: le nom de la nouvelle table
			attribute: tableau des attributs de la nouvelle table
			oldTableName: le nom de l'ancienne table pour chaque attributs de attribute
		"""
		dataToAdd=None#tableau contenant les lignes (tuples) a ajouter a la table
		s="CREATE TABLE "+tableName+"( "#s est une str pour la requete sql de creation de table
		for index in range(0,len(attribute)):
			oldTableNameI=oldTableName[index]
			attributeName=attribute[index]

			#on selectionne les donnees a ajouter et on l'ajoute a dataToAdd
			if oldTableNameI != 'FuncDep':
				select="SELECT "+attributeName+" FROM "+oldTableNameI
				self.cursor.execute(select)
				resultSelect=self.cursor.fetchall()
				if dataToAdd==None:
					dataToAdd=resultSelect
				else:
					for i in range(0,len(dataToAdd)):
						dataToAdd[i]=dataToAdd[i]+resultSelect[i]
			
			#finalisation de la str s
			info=self.metadataOfAttribute(oldTableNameI, attributeName)# infos sur l'attribut ( type, not null, valeur par defaut)
			s=s+attributeName+" "+info[2]+" "
			if info[3]==1:
				s=s+"NOT NULL"+" "
			if info[4] != None:
				s=s+"DEFAULT "+str(info[4])+" "
			s+=", "
		s=s[0:len(s)-2]
		s+=")"
		self.cursor.execute(s)#creation de la table
		values=""# chaine pour inserer les donnees
		s2="INSERT INTO "+tableName+"( "
		for att in attribute:
			s2=s2+att+", "
			values=values+"?, "
		s2=s2[0:len(s2)-2]
		values=values[0:len(values)-2]
		s2+=") VALUES("+values+")"

		for ligne in dataToAdd:#on insere chaque ligne
			self.cursor.execute(s2,ligne)
	def removeOldTable(self,oldTableName):
		"""
		Supprime les tables de la liste oldTableName
		Param: 
				oldTableName: tableau de noms des tables a supprimer
		"""
		for oldTable in oldTableName:
			self.dropTable(oldTable)
	def dropTable(self, table):
		"""
		Supprime la table table de la base de donnes
		Param:
			table: le nom de la table a supprimer
		"""
		sRemove="DROP TABLE IF EXISTS "+table
		self.cursor.execute(sRemove)