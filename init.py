import sqlite3

db=None
cursor=None
def connect(bdd):
	db=sqlite3.connect(bdd)
	cursor=db.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
	db.commit()

def insertDep(table, lhs, rhs):
	if(rhs.count(" ")==0):
		cursor.execute(""" INSERT INTO FuncDep(table, lhs, rhs) 
			VALUES(?, ?, ?) """, (table, lhs, rhs) )
		db.commit()
	else:
		#TODO
		print("error")

def removeDep(table, lhs, rhs):
	cursor.execute("""DELETE FROM FuncDep WHERE table=?, lhs=?, rhs=?""", (table, lhs, rhs) )
	db.commit()


def editTableDep(tableData, lhsData, rhsData, newData):
	cursor.execute(""" UPDATE FuncDep SET table=? where table=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
	db.commit()

def ediLhsDep(tableData, lhsData, rhsData, newData):
	cursor.execute(""" UPDATE FuncDep SET lhs=? where table=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
	db.commit()

def editRhsDep(tableData, lhsData, rhsData, newData):
	cursor.execute(""" UPDATE FuncDep SET rhs=? where table=? AND lhs=? AND rhs=?""", (newData, tableData, lhsData, rhsData))
	db.commit()

def getTableName():
	db=sqlite3.connect('tests')
	cursor=db.cursor()
	cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
	retour=[]
	for data in cursor.fetchone():
		retour.append(data)
	return retour

def getTableAttribute(tableName):
	retour=[]
	cursor.execute("""PRAGMA table_info(unif)""");
	for rows in cursor:
		retour.append(rows[1])
	return retour

def getDep(relation):
	db=sqlite3.connect('tests')
	cursor=db.cursor()
	cursor.execute(""" SELECT * FROM FuncDep """)
	retour=[]
	for tuples in cursor:
		if tuples[0]==relation:
			line=[]
			for item in line:
				line.append(item)
			retour.append(line)
		

	return retour
def getAllDep():
	db=sqlite3.connect('tests')
	cursor=db.cursor()
	retour=[]
	rels=getTableName()
	for tables in rels:
		deps=getDep(tables)
		for lines in deps:
			retour.append(lines)

	return retour
