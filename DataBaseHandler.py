import sqlite3
import time

class DataBaseHandler:
	"""docstring for DataBaseHandler"""
	def __init__(self, dataBase):
		self.db=sqlite3.connect(dataBase)
		self.cursor=self.db.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.db.commit()

	def insertDep(self,table, lhs, rhs):
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
			#TODO
			print("error")
			return None


	def removeDep(self,table, lhs, rhs):
		self.cursor.execute("""DELETE FROM FuncDep WHERE 'table'=?, lhs=?, rhs=?""", (table, lhs, rhs) )
		self.db.commit()


	def editTableDep(self,tableData, lhsData, rhsData, newData):
		self.cursor.execute(""" UPDATE FuncDep SET 'table'=? where 'table'=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
		self.db.commit()

	def ediLhsDep(self,tableData, lhsData, rhsData, newData):
		self.cursor.execute(""" UPDATE FuncDep SET lhs=? where 'table'=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
		self.db.commit()

	def editRhsDep(self,tableData, lhsData, rhsData, newData):
		self.cursor.execute(""" UPDATE FuncDep SET rhs=? where 'table'=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
		self.db.commit()

	def getTableName(self):
		self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' """)
		retour=[]
		for data in self.cursor.fetchone():
			retour.append(data)
		return retour

	def getTableAttribute(self,tableName):
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
		self.cursor.execute(""" SELECT * FROM FuncDep """)
		retour=[]
		for tuples in self.cursor:
			if tuples[0]==relation:
				line=[]
				for item in line:
					line.append(item)
				retour.append(line)
			

		return retour
	def getAllDep(self):
		retour=[]
		rels=getTableName()
		for tables in rels:
			deps=getDep(tables)
			for lines in deps:
				retour.append(lines)

		return retour
