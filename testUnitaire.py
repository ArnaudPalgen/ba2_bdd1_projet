import unittest
import sqlite3
from dfHandler import *
import os

class DfTest(unittest.TestCase):

	def setUp(self):
		self.dataBaseName='Test'
		if os.path.exists(dataBaseName):
			os.system('rm '+dataBaseName)
		self.db=sqlite3.connect(dataBaseName)
		self.cursor=db.cursor()

		self.tableDfVerifiee='table1'
		cursor.execute("""CREATE TABLE table1(matricule TEXT NOT NULL, nom TEXT NOT NULL, age TEXT NOT NULL)""")#creation de la table
		cursor.execute(""" INSERT INTO table1(A,B,C) VALUES(?,?,?)""",("157825", "jean", "18") )
		# nom, age --> matricule
		# age --> age

		

		self.tableBCNF='table2'
		cursor.execute("""CREATE TABLE table2(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D text NOT NULL)""")
		cursor.execute(""" INSERT INTO table2(A,B,C,D) VALUES(?,?,?,?)""",("aa", "bb", "cc","dd") )
		cursor.execute(""" INSERT INTO table2(A,B,C,D) VALUES(?,?,?,?)""",("aaa", "bbb", "ccc","ddd") )

		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.tableBCNF,'A B','C'))
		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.tableBCNF,'A B','D'))

		

		self.table3NFPrem='table3'
		cursor.execute("""CREATE TABLE table3(A TEXT NOT NULL, B TEXT NOT NULL, C TEXT NOT NULL, D text NOT NULL, E text NOT NULL)""")
		cursor.execute(""" INSERT INTO table3(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aa", "bb", "cc","dd","ee") )
		cursor.execute(""" INSERT INTO table3(A,B,C,D,E) VALUES(?,?,?,?,?)""",("aaa", "bbb", "ccc","ddd","eee") )

		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table3NFPrem,'A','B'))
		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table3NFPrem,'A','C'))
		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table3NFPrem,'C D','E'))
		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (table3NFPrem,'B','D'))


		
		self.table3NFLhs='table3'
		cursor.execute("""CREATE TABLE table3(A TEXT NOT NULL, B TEXT NOT NULL)""")
		cursor.execute(""" INSERT INTO table3(A,B) VALUES(?,?)""",("aa", "bb") )
		cursor.execute(""" INSERT INTO table3(A,B) VALUES(?,?)""",("aaa", "bbb") )

		cursor.execute("""INSERT INTO FuncDep('table', lhs, rhs) VALUES(?,?,?)""", (self.table3NFLhs,'A','B'))


	def testBcnf(self):
		self.assertTrue(self.dbh.isBcnf(self.tableBCNF))
		
	def dfVerifiee(self):
		pass
	def test3nf(self):
		self.assertTrue(self.dbh.is3nf(self.table3NFPrem))
		self.assertTrue(self.dbh.is3nf(self.table3NFLhs))
	def testCle(self):
		self.assertEqual((self.dbh.getCle(self.table3NFLhs)),[[A]])
	def testSuperCle(self):
		self.assertEqual((self.dbh.getSuperCle(self.table3NFLhs)),[[A B],[A]])
	def testDecomposition(self):
		sel.assertEqual((getDecomposition3nf(self)), )
	def tearDown(self):
		self.db.close()