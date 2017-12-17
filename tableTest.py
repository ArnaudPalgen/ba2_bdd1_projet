# coding: utf-8
import sqlite3
from dfHandler import *

dataBase='tableTest'
var1=False
var2=True
#Table1---------------------------------------------------------------------------------------------------------------------------------------------------------------
table1='lettre'

if var1:
	db=sqlite3.connect(dataBase)
	cursor=db.cursor()
	#creation table lettre
	cursor.execute("""CREATE TABLE IF NOT EXISTS lettre(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D TEXT NOT NULL, E TEXT NOT NULL)""")
	#insertion des donnees dans la table
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aa", "bb", "cc", "dd", "ee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaa", "bbb", "ccc", "ddd", "eee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaa", "bbbb", "cccc", "dddd", "eeee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaaaa", "bbbbbb", "cccccc", "dddddd", "eeeeee") )

	#creation table FuncDep
	cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
	#insertion des DFs
	cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1,'A B','C'))
	cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1,'A B','D'))
	cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1,'C','A'))
	cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1,'C','E'))

	db.commit()
	db.close()
else:
	print('nothing to create for table1\n')

# handler=DfHandler(dataBase)

# cle1=handler.getCle(table1)
# superCle1=handler.getSuperCle(table1)
# troisNf1=handler.is3nf(table1)
# bcnf1=handler.isBcnf(table1)
# print('consequence logique c->a: '+str(handler.isLogicConsequence(table1, 'C', 'A')))
# handler.getDecomposition3nf(table1)
# print('-------------------------------------- Table 1 ( lettre): ----------------------------------------------------')
# print('cle: '+str(cle1))
# print('super cles: '+str(superCle1))
# print('3 nf: '+str(troisNf1))
# print('bcnf: '+(str(bcnf1)))
# print('----------------------------------------------------------------------------------------------------------------\n')

#Table2---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#question 104 p103
# en 3 nf mais pas en bcnf
table2='lettre104'

if var2:
	#creation de table lettre104
	db=sqlite3.connect(dataBase)
	cursor=db.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS lettre104(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D TEXT NOT NULL, E TEXT NOT NULL)""")#, F TEXT NOT NULL)""")
	#insertion de donnees
	#pass

	#creation FuncDep
	cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")

	#insertion des DFs
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A B C','E'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'B C D','F'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'E F','A'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'E F','B'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'E F','C'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'C E F','D'))
	#---
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A','B'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A','C'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A','D'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A','E'))
	#cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2,'A','F'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A','B'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'B C','D'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A C','B'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A C','D'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A C','E'))
	# cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'D','E'))
	cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A','B'))
	cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'A','C'))
	cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'C D','E'))
	cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table2,'B','D'))

	
	db.commit()
	db.close()

else:
	print('nothing to create for table2\n')

handler=DfHandler(dataBase)

# cle2=handler.getCle(table2)
# superCle2=handler.getSuperCle(table2)
# troisNf2=handler.is3nf(table2)
# bcnf2=handler.isBcnf(table2)

# print('-------------------------------------- Table 2 ( lettre104): -------------------------------------------------')
# print('cle: '+str(cle2))
# print('super cles: '+str(superCle2))
# print('\n3 nf: '+str(troisNf2))
# print('bcnf: '+(str(bcnf2)))
# print('----------------------------------------------------------------------------------------------------------------\n')
#handler.getCouvertureMinimale(table2)
#handler.getDecomposition3nf(table2)