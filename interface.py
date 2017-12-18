from dfHandler import *
from DataBaseHandler import *
import os
import atexit
#TODO suppression des df inutiles (option 3)
#TODO retirer print dans getDecomposition3nf(dfHandler) apres le push

dbh = None


def add():

	"""
	fonction permettant l ajout de dependance fonctionelle
	"""

	cls()
	tableau = dbh.getAllDep()

	if len(tableau)== 0:
		empty_table=input("la table FuncDep ne contient aucun element actuelement")
		main_menu()
	
	else:
		print("la table FuncDep contient les dependances suivantes: ")
		
		for line in tableau:
			print("Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
	print("-----------------------------------------------")
	print("rentrer les elements suivants :")
	addTables = input("nom de la table : ")
	print("partie gauche de la dependance fonctionnelle :")
	addLhs = input("(si vous avez plusieurs elements separez les par des espaces et non des virgules) : ")
	addRhs = input("partie droite de la dependance fonctionnelle : ")

	dep=dbh.insertDep(addTables, addLhs, addRhs)

	if dep == False:
		error_add=input("votre dependance n'a pas pu etre ajoutee. Sorry :( (verifiez que la dependance n'existe pas deja ou a ete bien ecrite) ")
		main_menu()

	print_dep=input("Votre dependance a bien ete ajoutee : "+ addLhs + "-->" +addRhs)
	main_menu()





def edit():

	"""
	fonction permettant la modification de dependance fonctionelle
	"""

	cls()
	tableau = dbh.getAllDep()

	if len(tableau)== 0:
		empty_table=input("la table FuncDep ne contient aucun element a modifier")
		main_menu()
	
	else:
		print("quelle ligne voulez-vous modifier?")
		increment = 1
		
		for line in tableau:
			print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
			increment  += 1

		try:
			num = input("numero de la ligne : ")
			nbre = int(num)
			
			if nbre > (len(tableau)) or nbre <= 0:
				error_int=input("error integer")
				edit()
			
			else:
				cls()
				print("que voulez-vous modifier?")
				print("1. table")
				print("2. lhs")
				print("3. rhs")

				choice = input("entrez le nbre: ")
				newnbre = int(choice)
				new = input("rentrez les nouvelles donnees :")

				if newnbre == 1: 
					retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.TABLE)
					
					if retour:
						print("votre donnee a bien ete modifiee")
						print_dep=input("la nouvelle dependance est :"+ new +" "+ tableau[nbre -1][1] + "-->" + tableau[nbre -1][2])
						main_menu()
					
					else:
						error_edit=input("une erreur est apparue lors de la modification de votre dependance")
						main_menu()
				
				elif newnbre == 2:
					retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.LHS)
					
					if retour:
						print("votre donnee a bien ete modifiee")
						print_dep=input("la nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ new + "-->" + tableau[nbre -1][2])
						main_menu()
					
					else:
						error_edit=input("une erreur est apparue lors de la modification de votre dependance")
						main_menu()

				elif newnbre == 3:
					
					if new.count(" ") != 0:
						print("error syntax")
						edit()
					
					else:
						retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.RHS)

						if retour:
							print("votre donnee a bien ete modifiee")
							print_dep=input("la nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ tableau[nbre -1][1] + "-->" + new)
							main_menu()
						
						else:
							error_edit=input("une erreur est apparue lors de la modification de votre dependance")
							main_menu()

				else:
					error_int=input("error integer")
					edit()

		except ValueError:
			except_error=input("invalid syntax, try again")
			edit()





def delete():

	"""
	fonctionpermettant la suppression de dependance
	"""

	cls()
	tableau = dbh.getAllDep() 
	
	if len(tableau)== 0:
		empty_table=input("la table FuncDep ne contient aucun element a supprimer")
		main_menu()

	else:
		print("quelle ligne voulez-vous supprimer?")
		increment = 1
		
		for line in tableau:
			print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle :"+line[1]+" --> "+line[2])
			increment += 1

		try: 
			num = input("numero de la ligne : ")
			nbre = int(num)

			if nbre > (len(tableau)) or nbre <= 0:
				error_int=input("error integer")
				delete()

			else:
				cls()
				verif = input("la suppression est definitive voulez-vous vraiment continuer?(Y/N)")
				
				if verif == "Y" or verif == "y":
					
					if dbh.removeDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
						print_dep=input("la dependance "+ tableau[nbre -1][1]+"-->"+tableau[nbre -1][2]+" venant de la table "+tableau[nbre -1][0]+" a bien ete supprimee")
						main_menu()
					
					else:
						error_del=input("une erreur c est produite pendant l'operation")
						main_menu()
				
				elif verif == "N" or verif == "n":
					main_menu()
				
				else:
					error_synth=input("erreur synthaxe")
					delete()
		
		except ValueError:
			except_error=input("invalid syntax, try again")
			delete()





def analyse():
	
	"""
	fonction contenant les differentes option d analyse de df/ de tables
	"""
	
	cls()
	tableau = dbh.getAllDep() #ajout de getAllDep à dfHandler
	
	if len(tableau)== 0:
		empty_table=input("option analyse temporairement indisponible car la table FuncDep est vide")
		main_menu()
	
	else:
		
		try:
			print("que voulez-vous faire?")
			print("1. determiner les cles et supercles d'un schema")
			print("2. determiner les consequences logiques")
			print("3. DF non satisfaite(s)")
			print("4. BCNF ou 3NF")
			print("5. retour au menu principal")
			nbre = input("entrez le nbre: ")
			option = int(nbre)

			if option ==1:
				
				try:
					cls()
					print("quelle table voulez-vous determiner?")
					print("-----------------------------------------------")
					t= dbh.getAllTableInFuncDep()
					
					for i in t:
						print(i)
					print("-----------------------------------------------")
					table_name=input("entrez le nom de la table: ")
					
					if table_name in t == False:
						table_name = input("erreur de synthaxe veuillez reecrire le nom de la table : ")
					
					else:
						choice=input("voulez vous les cles(1) ou les supercles(2)? : ")
						cle=int(choice)
						
						if cle ==1:
							cls()
							cle=input("les cles de la table "+table_name+" sont : "+str(dbh.getCle(table_name)))
							main_menu()
						
						elif cle == 2:
							cls()
							supercle=input("les supercles de la table "+table_name+" sont : "+str(dbh.getSuperCle(table_name)))
							main_menu()
						
						else:
							error_int=input("error integer")
							analyse()
				
				except ValueError:
					except_error = input("invalid syntax")
					analyse()





			elif option == 2:
				cls()
				increment =1
				
				for line in tableau:
					print(str(increment)+".  Table: "+line[0]+" dependance fonctionnelle :"+line[1]+" --> "+line[2])
					increment +=1
				
				try:
					num= input("numero de la dependance a analyser :")
					nbre = int(num)

					if nbre > (len(tableau)) or nbre <= 0:
						error_int=input("error integer")
						analyse()
					
					else:
						
						if dbh.isLogicConsequence(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
							print_LC_OK = input(tableau[nbre -1][0]+" -->"+tableau[nbre -1][2]+ " est bien une consequence logique")
							analyse()
						
						else:
							print_LC_NOT = input("votre dependance n'est pas une consequence logique")
							analyse()
				
				except ValueError:
					except_error=input("invalid syntax, try again")
					analyse()





			elif option == 3:
				cls()
				print("que voulez-vous faire?")
				print("1. afficher et supprimer les df ayant la table ou un argument qui n'est plus existant")
				print("2. afficher et supprimer les df qui sont des consequences logiques")
				print("3. afficher et supprimer les df qui ne sont pas respectees")
				print("4. suppression de toutes les df inutiles")
				print("5. retour au menu analyse")

				try:
					nbre = input("entrez le nbre: ")
					option = int(nbre)
						
					if option <=3:
						increment = 1
						
						if len(dbh.getInutileDF()[option-1]) == 0:
							void = input("FuncDep ne contient aucune dependances inutiles")
							analyse()

						else:
							for line in dbh.getInutileDF()[option-1]:
								print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
								increment  += 1
							print("quelle(s) lignes voulez-vous supprimer?")
							nbre = input("numero de la ligne si plusieurs separez les nombre par des espaces) : ")
							
							for i in nbre.split():		
								
								if i != " ":
									i = int(i)
									dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2])
									if not dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2]):
										print("une erreur c'est produite lors de la suppression de la dependance : "+dbh.getInutileDF()[option-1][i -1][1]+" --> "+ dbh.getInutileDF()[option-1][i -1][2])
										error=input("verifiez que cette dependance soit bien dans FuncDep")
										analyse()
							Good = input("vos df inutiles ont bien ete supprimees")
							analyse()
								

					elif option == 4:
						
						if len(dbh.getInutileDF()[0]) == 0 and len(dbh.getInutileDF()[1]) == 0 and len(dbh.getInutileDF()[2]) == 0:
							void = input("FuncDep ne contient aucune dependances inutiles")
							analyse()
						
						else:
							print("les df suivantes vont etre supprimees")
							increment = 1
							h = 0
							
							while h <=2:
								
								for line in dbh.getInutileDF()[h]:
									print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
									increment += 1
								h += 1

							choice = input("voulez-vous continuer? (Y/N) : ")
							
							if choice == "Y" or choice == "y":
								i = 0
								
								while i <=2:
									
									for j in range(0,len(dbh.getInutileDF()[i])-1):
										dbh.removeDep(dbh.getInutileDF()[i][j][0],dbh.getInutileDF()[i][j][1],dbh.getInutileDF()[i][j][2])

										if not dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2]):
											print("une erreur c'est produite lors de la suppression de la dependance : "+dbh.getInutileDF()[option-1][i -1][1]+" --> "+ dbh.getInutileDF()[option-1][i -1][2])
											error=input("verifiez que cette dependance soit bien dans FuncDep")
											analyse()
									i+=1
								Good = input("vos df inutiles ont bien ete supprimees")
								analyse()

							elif choice == "N" or choice == "n":
								analyse()

							else:
								error = input("error integer")
								analyse()

					elif option == 5:
						analyse()

					else:
						error=input("error integer")
						analyse()

				except ValueError:
					except_error=input("invalid syntax, try again")
					analyse()





			elif option == 4: 
				cls()
				print("quelle table voulez-vous determiner?")
				print("-----------------------------------------------")
				tableall= dbh.getTableName()
				
				for table in tableall:
					print(table)
				print("-----------------------------------------------")
				table_name=input("entrez le nom de la table: ")
				
				if table_name in tableall == False:
					table_name = input("erreur de synthaxe veuillez reecrire le nom de la table :")
				
				else:

					if dbh.is3nf(table_name) == False:
						not3NF = input("votre schema n est pas en 3nf donc ne sera pas en BCNF voulez vous faire une decomposition 3NF de votre table? (Y/N) : ")
						
						if not3NF == "Y" or not3NF == "y":
							decomp=input("la decomposition en 3nf serait : "+ str(dbh.getDecomposition3nf(table_name)))

							DataBase=input("voulez-vous creer une nouvelle base de donnee avec les decompositions? Y/N : ")

							if DataBase == "N" or DataBase =="n":
								notcreate = input("la nouvelle base de donnee n'as pas ete cree")
								main_menu()

							elif DataBase == "Y" or DataBase == "y":
								cls()
								name_DataBase = input("Veuillez entrer le nom de la nouvelle base de donnee : ")
								print("voila les decompositions:")
								print("-----------------------------------------------")
								newDataBase =dbh.getDecomposition3nf(table_name)

								for newtable in newDataBase:
									print("nom provisoire de la table : "+str(newtable[0])+" qui a comme attribut : "+str(newtable[1])+" et comme df : "+str(newtable[2]))
								print("-----------------------------------------------")
								
								print("attention de ne pas mettre un mot cle de sqlite3 en nom de table")
								for i in range(0, len(newDataBase)):
									
									newTableName=input("veuillez modifier le nom provisoire de la table "+str(newDataBase[i][0])+" par celui de votre choix : ")
									
									if not newTableName == '':
										newDataBase[i][0] = newTableName
										newDataBase[i][2][0] = newTableName
								
								try:
									dbh.createNewData(name_DataBase,newDataBase):

									print("la nouvelle base de donnee a bien ete cree")
									decomp = input("attention l'application continue a tourner sur l'ancienne base de donnee")
									main_menu()
								
								except Exception:
									decomp_not= input("une erreur c'est produite lors de la creation de la nouvelle base de donnee\n Veuillez verifier les donnees que vous avez rentre")
									main_menu()
							
							else:
								print("erreur synthaxe")
								analyse()
						
						elif not3NF == "N" or not3NF == "n":
							analyse()
						
						else:
							print("erreur synthaxe")
							analyse()

					else:
						
						if dbh.isBcnf(table_name):
							bcnf = input("votre schema est en BCNF")
							main_menu()
						
						else:
							not_bcnf = input("votre schema est en 3nf mais n est pas en BCNF")
							analyse()
							




			elif option == 5:
				main_menu()





			else:
				error_int=input("le nombre n est pas valide")
				analyse()





		except ValueError:
			except_error=input("invalid syntax, try again")





def main_menu():

	"""
	fonction contenant le menu principal de l'application
	"""

	cls()
	print("Veuillez choisir votre fonctionnalite :")
	print("1. ajouter une dependance")
	print("2. modifier une dependance")
	print("3. supprimer une dependance")
	print("4. analyser des dependances")
	print("5. changer de base de donnee")
	print("6. visionner vos dependances fonctionnelles")
	print("7. quitter l'application")

	try:
		choice = input("entrez le nombre : ")
		fonctio = int(choice)

		if fonctio == 1:
			add()
		
		elif fonctio == 2:
			edit()
		
		elif fonctio == 3:
			delete()
		
		elif fonctio == 4:
			analyse()
		
		elif fonctio == 5:
			cls()
			init()
		
		elif fonctio == 6:
			cls()
			tableau = dbh.getAllDep()
			
			if len(tableau) == 0:
				empty_table=input("vous n'avez pas encore de dependances fonctionnelles")
				main_menu()

			else:
				increment = 1

				for line in tableau:
					print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle : "+line[1]+"-->"+line[2])
					increment += 1
				back=input("retour au menu principal")
				main_menu()

		elif fonctio == 7:
			exit()

		else:
			error_int=input("invalid number, try again")
			main_menu()

	except ValueError:
		except_error=input("invalid syntax, try again")
		main_menu()





def init():

	"""
	fonction initiale permettant de choisir la base de donnee
	"""


	bdd=input("inserer la base de donnee:")
	global dbh
	dbh = DfHandler(bdd)
	main_menu()





def cls():

	""" 
	fonction de nettoyage d ecran
	"""

	os.system('cls' if os.name =='nt' else 'clear')





def onclose():
	"""
	fonction de fermeture d application
	"""
	dbh.closeDataBase()
	#os.system('cls' if os.name =='nt' else 'clear')
	print("###############################################")
	print("###############################################")
	print("##### #####  #####  ####   ####   #    #  #####")
	print("#     #   #  #   #  #   #  #   #   #  #   #    ")
	print("#  ## #   #  #   #  #   #  ####     ##    #####")
	print("#  #  #   #  #   #  #   #  #   #    ##    #    ")
	print("####  #####  #####  ####   ####     ##    #####")
	print("###############################################")
	print("###############################################")





atexit.register(onclose)

os.system('cls' if os.name =='nt' else 'clear')
print("##################################")
print("##################################")
print("#    #  #####  #      #      #####")
print("#    #  #      #      #      #   #")
print("######  #####  #      #      #   #")
print("#    #  #      #      #      #   #")
print("#    #  #####  #####  #####  #####")
print("##################################")
print("##################################")
init()

