import sqlite3


db=sqlite3.connect("depData")
cursor=db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXITS FuncDep(
	table TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY(table, lhs, rhs))""")
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