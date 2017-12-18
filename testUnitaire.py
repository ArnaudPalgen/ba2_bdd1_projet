import unittest
import sqlite3
from dfHandler import *
import os

class DfTest(unittest.TestCase):

	def setUp(self):
		self.dataBaseName='Test'
		if os.path.exists(self.dataBaseName):
			os.system('rm '+self.dataBaseName)
		self.db=sqlite3.connect(self.dataBaseName)
		self.cursor=self.db.cursor()

		self.tableDfVerifiee='table1'
		self.cursor.execute("""CREATE TABLE table1(matricule TEXT NOT NULL, nom TEXT NOT NULL, age TEXT NOT NULL)""")#creation de la table
		self.cursor.execute(""" INSERT INTO table1(matricule, nom, age) VALUES(?,?,?)""",("157825", "jean", "18") )
		self.cursor.execute(""" INSERT INTO table1(matricule, nom, age) VALUES(?,?,?)""",("475624", "jean", "18") )
		
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""",(self.tableDfVerifiee, "nom age", "matricule") )
		self.cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""",(self.tableDfVerifiee, "age", "age") )
		

		# nom, age --> matricule
		# age --> age
		

		self.tableBCNF='table2'
		self.cursor.execute("""CREATE TABLE table2(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D text NOT NULL)""")
		self.cursor.execute(""" INSERT INTO table2(A,B,C,D) VALUES(?,?,?,?)""",("aa", "bb", "cc","dd") )
		self.cursor.execute(""" INSERT INTO table2(A,B,C,D) VALUES(?,?,?,?)""",("aaa", "bbb", "ccc","ddd") )

		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.tableBCNF,'A B','C'))
		self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.tableBCNF,'A B','D'))

		

		# self.table3NFPrem='table3'
		# self.cursor.execute("""CREATE TABLE table3(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D text NOT NULL, E text NOT NULL)""")
		# self.cursor.execute(""" INSERT INTO table3(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aa", "bb", "cc","dd","ee") )
		# self.cursor.execute(""" INSERT INTO table3(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaa", "bbb", "ccc","ddd","eee") )

		# self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		# self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFPrem,'A','B'))
		# self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFPrem,'A','C'))
		# self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFPrem,'C D','E'))
		# self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFPrem,'B','D'))


		
		self.table3NFLhs='table4'
		self.cursor.execute("""CREATE TABLE table4(A TEXT NOT NULL, B TEXT NOT NULL)""")
		self.cursor.execute(""" INSERT INTO table4(A,B) VALUES(?,?)""",("aa", "bb") )
		self.cursor.execute(""" INSERT INTO table4(A,B) VALUES(?,?)""",("aaa", "bbb") )

		self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
		self.cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFLhs,'A','B'))

		self.db.commit()
		self.dbh=DfHandler(self.dataBaseName)


	def testBcnf(self):
		self.assertTrue(self.dbh.isBcnf(self.tableBCNF))
		
	def dfVerifiee(self):
		self.assertEqual(self.dbh.satisfaitPasDF(self.tableDfVerifiee, "nom age", "matricule"), [["157825", "jean", "18"], ["475624", "jean", "18"]])
	def test3nf(self):
		self.assertTrue(self.dbh.is3nf(self.tableBCNF))
		self.assertTrue(self.dbh.is3nf(self.table3NFLhs))
	def testCle(self):
		self.assertEqual((self.dbh.getCle(self.table3NFLhs)),[[A]])
	def testSuperCle(self):
		self.assertEqual((self.dbh.getSuperCle(self.table3NFLhs)),[[A,B],[A]])
	def testDecomposition(self):
		sel.assertEqual((getDecomposition3nf(self)), )

	def tearDown(self):
		self.db.close()
if __name__ == '__main__':
    unittest.main()