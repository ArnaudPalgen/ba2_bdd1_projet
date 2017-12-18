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

	def testBcnf(self):
		pass
	def dfVerifiee(self):
		pass
	def test3nf(self):
		pass
	def testCle(self):
		pass
	def testSuperCle(self):
		pass
	def testDecomposition(self):
		pass
	def tearDown(self):
		self.db.close()