import sqlite3

dataBase = sqlite3.connect('chinook.db')
cursor=dataBase.cursor()

finding=cursor.execute("""SELECT Name, Composer from tracks""" )
for rows in finding:
	print(rows)
dataBase.close()

