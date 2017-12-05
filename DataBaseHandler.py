import sqlite3
import time

class DataBaseHandler:
	"""Gestionnaire de la base de donnees"""
	
	def __init__(self, dataBase):
		""" Constructeur de DataBaseHandler """

		self.db=sqlite3.connect(dataBase)
		self.cursor=self.db.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.db.commit()

	def insertDep(self,table, lhs, rhs):
		""" Insere une DF dans la table FuncDep

			Param: la table a laquelle appartient la DF: table
					lhs, le membre de gauche de la DF
					rhs, lemembre de droite de la DF 
			Return: la DF inseree

			Error: ValueError is rhs contient plus qu'un element

		"""

		if(rhs.count(" ")==0):
			self.cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES(?, ?, ?) """, (table, lhs, rhs) )
			self.db.commit()
			self.cursor.execute("""SELECT * FROM FuncDep WHERE Funcdep.'table'=? AND lhs=? AND rhs=? """, (table, lhs, rhs))
			tab=[]
			retour=self.cursor.fetchone()
			for item in retour:
				tab.append(item)
			return tab
		else:
			raise ValueError("rhs ne peut contenir qu'un element")


	def removeDep(self,table, lhs, rhs):
		""" 
		Supprime une DF dans la table FuncDep

			Param: la table a laquelle appartient la DF: table
					lhs, le membre de gauche de la DF
					rhs, lemembre de droite de la DF 

			Error: TODO

		"""
		self.cursor.execute("""DELETE FROM FuncDep WHERE Funcdep.'table'=?, lhs=?, rhs=?""", (table, lhs, rhs) )
		self.db.commit()


	def editTableDep(self,table, lhs, rhs, newTable):
		""" 
		Modifie la table d'une DF dans la table FuncDep

			Param: la table a laquelle appartient la DF: table
					lhs, le membre de gauche de la DF
					rhs, lemembre de droite de la DF
					newTable, le nom de la nouvelle table 
			Return: la DF modifiee TODO

			Error: TODO

		"""
		self.cursor.execute(""" UPDATE FuncDep SET Funcdep.'table'=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newTable, table, lhs, rhs))
		self.db.commit()

	def ediLhsDep(self,tabl, lhs, rhs, newLhs):
		""" 
		Modifie la partie de gauche d'une DF dans la table FuncDep

			Param: la table a laquelle appartient la DF: table
					lhs, le membre de gauche de la DF
					rhs, lemembre de droite de la DF
					newLhs, le nom de la nouvelle partie de gauche de la DF 
			Return: la DF modifiee TODO

			Error: TODO

		"""
		self.cursor.execute(""" UPDATE FuncDep SET lhs=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newLhs, table, lhs, rhs))
		self.db.commit()

	def editRhsDep(self,table, lhs, rhs, newRhs):
		""" 
		Modifie la partie de droite d'une DF dans la table FuncDep

			Param: la table a laquelle appartient la DF: table
					lhs, le membre de gauche de la DF
					rhs, lemembre de droite de la DF
					newRhs, le nom de la nouvelle partie de droite de la DF 
			Return: la DF modifiee TODO

			Error: TODO

		"""
		self.cursor.execute(""" UPDATE FuncDep SET rhs=? where Funcdep.'table'=? AND lhs=? AND rhs=?""", (newRhs, table, lhs, rhs))
		self.db.commit()

	def getTableName(self):
		""" 
		Retourne le nom de toutes les tables de la base de donnees 

			Return: Un tableau contenant les noms de toutes les tables de la base de donee
			Error: TODO
		"""
		self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' """)
		retour=[]
		for data in self.cursor.fetchone():
			retour.append(data)
		return retour

	def getTableAttribute(self,tableName):
		""" 
		Retourne les attributs d'une table de la base de donnee

			Param: tableName le nom de la table
			Return: Un tableau contenant le noms des attributs de la table TableName
			Error: TODO

		"""
		retour=[]
		self.cursor.execute("""PRAGMA table_info(unif)""");
		for rows in self.cursor:
			retour.append(rows[1])
		return retour

	#def getDep(self, table, lhs, rhs):
	#	self.cursor.execute("""SELECT * FROM FuncDep WHERE 'table'=? AND lhs=? AND rhs=? """, (table, lhs, rhs))
	#	retour=[]
	#	for item in self.cursor.fetchone():
	#		retour.append(item)
	#	return retour

	def getDepByRelation(self,relation):
		""" 
		Retourne toutes les DF d'une table

			Param: relation un nom d'une table de la base de donnee ??diff de funcDep ????
			Return: un tableau contenant toutes les DFs associees a la table relation
			Error: TODO

		"""
		self.cursor.execute(""" SELECT lhs, rhs FROM FuncDep WHERE FuncDep.'table'=?  """, relation)
		retour=[]
		for tuples in self.cursor:
			#if tuples[0]==relation:
			#	line=[]
			#	for item in line:
			#		line.append(item)
			#	retour.append(line)
			retour.append(tuples)
			
		return retour
	
	def getAllDep(self):
		""" 
		Retourne toutes les DF de la table FuncDep

			Return: Un tableau a deux dimensions ou chaque ligne est une DF
			Error: TODO

		"""
		retour=[]
		#rels=getTableName()
		#for tables in rels:
		#	deps=getDep(tables)
		#	for lines in deps:
		#		retour.append(lines)

		self.cursor.execute(""" SELECT * FROM FuncDep""")

		for items in self.cursor:
			l=[]
			for element in item:
				l.append(element)
			retour.apppend(l)

		return retour
