import sqlite3

db=sqlite3.connect("tests")
cursor=db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS unif(
	prof TEXT NOT NULL, cours TEXT NOT NULL, heure INTEGER NOT NULL )""")

cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("arnaud", "info", 123) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("arnaud", "math", 124) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("guillaume", "physique", 123) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("guillaume", "math2", 678) )
cursor.execute(""" INSERT INTO unif(prof, cours, heure) VALUES(?, ?, ?) """, ("jean", "francais", 999) )

db.commit()


finding=cursor.execute("""SELECT prof, cours, heure from unif""" )
for rows in finding:
	print(rows)

#cursor.execute(""" UPDATE FuncDep SET table=? where table=?, lhs=?, rhs=?)
cursor.execute("""UPDATE unif SET prof=? where prof=? AND cours=? AND heure=? """, ("toto", "jean", "francais", 999))
db.commit()

finding=cursor.execute("""SELECT prof, cours, heure from unif""" )
for rows in finding:
	print(rows)

db.close()
