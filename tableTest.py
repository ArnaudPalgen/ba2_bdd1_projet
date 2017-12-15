import sqlite3
from dfHandler import *

db=sqlite3.connect("tableTest")
cursor=db.cursor()

var=False

if var:
	cursor.execute("""CREATE TABLE IF NOT EXISTS lettre(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D TEXT NOT NULL, E TEXT NOT NULL)""")

	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aa", "bb", "cc", "dd", "ee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaa", "bbb", "ccc", "ddd", "eee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaa", "bbbb", "cccc", "dddd", "eeee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee") )
	cursor.execute(""" INSERT INTO lettre(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaaaaa", "bbbbbb", "cccccc", "dddddd", "eeeeee") )
	db.commit()
	db.close()
else:
	print("nothing to do")
	db.close()

handler=DfHandler("tableTest")

r=handler.getCle('lettre')
print(r)