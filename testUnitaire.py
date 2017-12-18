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
		self.db.commit()
		self.dbh=DfHandler(self.dataBaseName)

		# nom, age --> matricule
		# age --> age

	def test_dfVerifiee(self):
		self.assertEqual(self.dbh.satisfaitPasDF(self.tableDfVerifiee, "nom age", "matricule"), [["157825", "jean", "18"], ["475624", "jean", "18"]])
	
	# def testBcnf(self):
	# 	pass

	# def test3nf(self):
	# 	pass
	# def testCle(self):
	# 	pass
	# def testSuperCle(self):
	# 	pass
	# def testDecomposition(self):
	# 	pass
	def tearDown(self):
		self.db.close()
if __name__ == '__main__':
    unittest.main()