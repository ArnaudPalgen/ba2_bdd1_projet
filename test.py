import sqlite3

db=sqlite3.connect("tests")
cursor=db.cursor()

#creer la table
cursor.execute("""CREATE TABLE IF NOT EXISTS unif(
	prof TEXT NOT NULL, cours TEXT NOT NULL, heure INTEGER NOT NULL )""")
#cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep(
#	'table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")

#inserer les donnees
name='arnaud'
cours='info'
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, (name, cours, 123) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("arnaud", "math", 124) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("guillaume", "physique", 123) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("guillaume", "math2", 678) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("jean", "francais", 999) )

db.commit()

#afficher tous les elements 
cursor.execute("""SELECT * from unif""" )
for rows in cursor:
	print(rows)

#modifier une entree
#cursor.execute("""UPDATE unif SET prof=? where prof=? AND cours=? AND heure=? """, ("toto", "jean", "francais", 999))
#db.commit()

#afficher les elements
#finding=cursor.execute("""SELECT prof, cours, heure from unif""" )
#for rows in finding:
#	print(rows)

#afficher les tables
#cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
#data=cursor.fetchone()
#print(cursor.description)
#for item in data:
#	print(item)
print("-------------------------------------------------------------------------------------------")
#cursor.execute("""SELECT .u1, prof.u2 FROM unif u1, unif u2 """)
#s="""select """
#for item in lhs:
#	chaine=item+""".z, """
#	s+=chaine
#s=s[0:len(s)-2]
#s+=""" """
#s+=""" rhs1.tableName From unif z, unif t WHERE"""
for item in cursor:
	print(item)
print("-------------------------------------------------------------------------------------------")
cursor.execute("""PRAGMA table_info(unif)""");
for rows in cursor:
	
	print(rows[1])

db.close()