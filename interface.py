from dfHandler import *
from DataBaseHandler import *
import os
import atexit


dbh = None


def add():

	"""
	fonction permettant l ajout de dependance fonctionelle
	"""

	cls()
	tableau = dbh.getAllDep()

	if len(tableau)== 0:
		empty_table=input("La table FuncDep ne contient aucun element actuellement")
		main_menu()
	
	else:
		print("la table FuncDep contient les dependances suivantes: ")
		
		for line in tableau:
			print("Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
	print("-----------------------------------------------")
	print("Entrez les elements suivants :")
	addTables = input("Nom de la table : ")
	print("Partie gauche de la dependance fonctionnelle :")
	addLhs = input("(si vous avez plusieurs elements, separez-les par des espaces et non des virgules) : ")
	addRhs = input("Partie droite de la dependance fonctionnelle : ")

	dep=dbh.insertDep(addTables, addLhs, addRhs)

	if dep == False:
		error_add=input("Votre dependance n'a pas pu etre ajoutee. Sorry :( (verifiez que la dependance n'existe pas deja ou a ete bien ecrite) ")
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
		empty_table=input("La table FuncDep ne contient aucun element a modifier")
		main_menu()
	
	else:
		print("Quelle ligne voulez-vous modifier?")
		increment = 1
		
		for line in tableau:
			print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
			increment  += 1

		try:
			num = input("Entrez le numero de la ligne : ")
			nbre = int(num)
			
			if nbre > (len(tableau)) or nbre <= 0:
				error_int=input("cette ligne n'existe pas")
				edit()
			
			else:
				cls()
				print("Que voulez-vous modifier?")
				print("1. Table")
				print("2. Lhs")
				print("3. Rhs")

				choice = input("Entrez le nombre: ")
				newnbre = int(choice)
				new = input("Entrez les nouvelles donnees :")

				if newnbre == 1: 
					retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.TABLE)
					
					if retour:
						print("Votre donnee a bien ete modifiee")
						print_dep=input("La nouvelle dependance est :"+ new +" "+ tableau[nbre -1][1] + "-->" + tableau[nbre -1][2])
						main_menu()
					
					else:
						error_edit=input("Une erreur est apparue lors de la modification de votre dependance")
						main_menu()
				
				elif newnbre == 2:
					retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.LHS)
					
					if retour:
						print("Votre donnee a bien ete modifiee")
						print_dep=input("La nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ new + "-->" + tableau[nbre -1][2])
						main_menu()
					
					else:
						error_edit=input("Une erreur est apparue lors de la modification de votre dependance")
						main_menu()

				elif newnbre == 3:
					
					if new.count(" ") != 0:
						print("le nouvel Rhs est mal ecrit il contient plus d'un element")
						edit()
					
					else:
						retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.RHS)

						if retour:
							print("Votre donnee a bien ete modifiee")
							print_dep=input("La nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ tableau[nbre -1][1] + "-->" + new)
							main_menu()
						
						else:
							error_edit=input("Une erreur est apparue lors de la modification de votre dependance")
							main_menu()

				else:
					error_int=input("Le nombre que vous avez inserer ne fais pas partie des nombres disponibles")
					edit()

		except ValueError:
			except_error=input("Une erreur c'est produite lors d'une operation")
			edit()





def delete():

	"""
	fonctionpermettant la suppression de dependance
	"""

	cls()
	tableau = dbh.getAllDep() 
	
	if len(tableau)== 0:
		empty_table=input("La table FuncDep ne contient aucun element a supprimer")
		main_menu()

	else:
		print("Quelle ligne voulez-vous supprimer?")
		increment = 1
		
		for line in tableau:
			print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle :"+line[1]+" --> "+line[2])
			increment += 1

		try: 
			num = input("Entrez le numero de la ligne : ")
			nbre = int(num)

			if nbre > (len(tableau)) or nbre <= 0:
				error_int=input("la ligne que vous avez choisi n'existe pas")
				delete()

			else:
				cls()
				verif = input("La suppression est definitive voulez-vous vraiment continuer?(Y/N) : ")
				
				if verif == "Y" or verif == "y":
					
					if dbh.removeDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
						print_dep=input("La dependance "+ tableau[nbre -1][1]+"-->"+tableau[nbre -1][2]+" venant de la table "+tableau[nbre -1][0]+" a bien ete supprimee")
						main_menu()
					
					else:
						error_del=input("Une erreur c est produite pendant l'operation")
						main_menu()
				
				elif verif == "N" or verif == "n":
					main_menu()
				
				else:
					error_synth=input("Vous n'avez pas rentre le bon caractere")
					delete()
		
		except ValueError:
			except_error=input("Une erreur c'est produite lors d'une operation")
			delete()





def analyse():
	
	"""
	fonction contenant les differentes option d analyse de df/ de tables
	"""
	
	cls()
	tableau = dbh.getAllDep() #ajout de getAllDep à dfHandler
	
	if len(tableau)== 0:
		empty_table=input("Option analyse temporairement indisponible car la table FuncDep est vide")
		main_menu()
	
	else:
		
		try:
			print("Que voulez-vous faire?")
			print("1. Determiner les cles et supercles d'un schema")
			print("2. Determiner les consequences logiques")
			print("3. DF non satisfaite(s)")
			print("4. BCNF ou 3NF")
			print("5. Retour au menu principal")
			nbre = input("Entrez le nombre: ")
			option = int(nbre)

			if option ==1:
				
				try:
					cls()
					print("Quelle table voulez-vous determiner?")
					print("-----------------------------------------------")
					t= dbh.getAllTableInFuncDep()
					
					for i in t:
						print(i)
					print("-----------------------------------------------")
					table_name=input("Entrez le nom de la table: ")
					
					if table_name in t == False:
						table_name = input("Erreur de synthaxe veuillez reecrire le nom de la table : ")
					
					else:
						choice=input("Voulez vous les cles(1) ou les supercles(2)? : ")
						cle=int(choice)
						
						if cle ==1:
							cls()
							cle=input("Les cles de la table "+table_name+" sont : "+str(dbh.getCle(table_name)))
							main_menu()
						
						elif cle == 2:
							cls()
							supercle=input("Les supercles de la table "+table_name+" sont : "+str(dbh.getSuperCle(table_name)))
							main_menu()
						
						else:
							error_int=input("le numero demande n'est pas disponible")
							analyse()
				
				except ValueError:
					except_error = input("Une erreur c'est produite lors d'une operation")
					analyse()





			elif option == 2:
				cls()
				increment =1
				
				for line in tableau:
					print(str(increment)+".  Table: "+line[0]+" dependance fonctionnelle :"+line[1]+" --> "+line[2])
					increment +=1
				
				try:
					num= input("Entrez le numero de la dependance a analyser :")
					nbre = int(num)

					if nbre > (len(tableau)) or nbre <= 0:
						error_int=input("la dependance que vous demandez n'existe pas")
						analyse()
					
					else:
						
						if dbh.isLogicConsequence(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
							print_LC_OK = input(tableau[nbre -1][0]+" -->"+tableau[nbre -1][2]+ " est bien une consequence logique")
							analyse()
						
						else:
							print_LC_NOT = input("Votre dependance n'est pas une consequence logique")
							analyse()
				
				except ValueError:
					except_error=input("Une erreur c'est produite lors d'une operation")
					analyse()





			elif option == 3:
				cls()
				print("Que voulez-vous faire?")
				print("1. Afficher et supprimer les df ayant la table ou un argument qui n'est plus existant")
				print("2. Afficher et supprimer les df qui sont des consequences logiques")
				print("3. Afficher et supprimer les df qui ne sont pas respectees")
				print("4. Suppression de toutes les df inutiles")
				print("5. Retour au menu analyse")

				try:
					nbre = input("Entrez le nombre: ")
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
							print("Quelle(s) lignes voulez-vous supprimer?")
							nbre = input("Numero de la ligne (si plusieurs separez les nombre par des espaces) : ")
							
							for i in nbre.split():		
								
								if i != " ":
									i = int(i)
									dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2])
									if not dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2]):
										print("Une erreur c'est produite lors de la suppression de la dependance : "+dbh.getInutileDF()[option-1][i -1][1]+" --> "+ dbh.getInutileDF()[option-1][i -1][2])
										error=input("Verifiez que cette dependance soit bien dans FuncDep")
										analyse()
							Good = input("Vos df inutiles ont bien ete supprimees")
							analyse()
								

					elif option == 4:
						
						if len(dbh.getInutileDF()[0]) == 0 and len(dbh.getInutileDF()[1]) == 0 and len(dbh.getInutileDF()[2]) == 0:
							void = input("FuncDep ne contient aucune dependances inutiles")
							analyse()
						
						else:
							print("Les df suivantes vont etre supprimees")
							increment = 1
							h = 0
							
							while h <=2:
								
								for line in dbh.getInutileDF()[h]:
									print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
									increment += 1
								h += 1

							choice = input("Voulez-vous continuer? (Y/N) : ")
							
							if choice == "Y" or choice == "y":
								i = 0
								
								while i <=2:
									
									for j in range(0,len(dbh.getInutileDF()[i])-1):
										dbh.removeDep(dbh.getInutileDF()[i][j][0],dbh.getInutileDF()[i][j][1],dbh.getInutileDF()[i][j][2])

										if not dbh.removeDep(dbh.getInutileDF()[option-1][i -1][0],dbh.getInutileDF()[option-1][i -1][1],dbh.getInutileDF()[option-1][i -1][2]):
											print("Une erreur c'est produite lors de la suppression de la dependance : "+dbh.getInutileDF()[option-1][i -1][1]+" --> "+ dbh.getInutileDF()[option-1][i -1][2])
											error=input("Verifiez que cette dependance soit bien dans FuncDep")
											analyse()
									i+=1
								Good = input("Vos df inutiles ont bien ete supprimees")
								analyse()

							elif choice == "N" or choice == "n":
								analyse()

							else:
								error = input("le caractere rentre n'est pas valide")
								analyse()

					elif option == 5:
						analyse()

					else:
						error=input("l'option demandee n'existe pas")
						analyse()

				except ValueError:
					except_error=input("Une erreur c'est produite lors d'une operation")
					analyse()





			elif option == 4: 
				cls()
				print("Quelle table voulez-vous determiner?")
				print("-----------------------------------------------")
				tableall= dbh.getTableName()
				
				for table in tableall:
					print(table)
				print("-----------------------------------------------")
				table_name=input("Entrez le nom de la table: ")
				
				if table_name in tableall == False:
					table_name = input("Erreur de synthaxe veuillez reecrire le nom de la table :")
				
				else:

					if dbh.is3nf(table_name) == False:
						not3NF = input("Votre schema n est pas en 3nf donc ne sera pas en BCNF voulez vous faire une decomposition 3NF de votre table? (Y/N) : ")
						
						if not3NF == "Y" or not3NF == "y":
							decomp=input("La decomposition en 3nf serait : "+ str(dbh.getDecomposition3nf(table_name)))

							DataBase=input("Voulez-vous creer une nouvelle base de donnee avec les decompositions? Y/N : ")

							if DataBase == "N" or DataBase =="n":
								notcreate = input("La nouvelle base de donnee n'as pas ete cree")
								main_menu()

							elif DataBase == "Y" or DataBase == "y":
								cls()
								name_DataBase = input("Veuillez entrer le nom de la nouvelle base de donnee : ")
								print("Voila les decompositions:")
								print("-----------------------------------------------")
								newDataBase =dbh.getDecomposition3nf(table_name)

								for newtable in newDataBase:
									print("Nom provisoire de la table : "+str(newtable[0])+" qui a comme attribut : "+str(newtable[1])+" et comme df : "+str(newtable[2]))
								print("-----------------------------------------------")
								
								print("Attention de ne pas mettre un mot cle de sqlite3 en nom de table")
								for i in range(0, len(newDataBase)):
									
									newTableName=input("Veuillez modifier le nom provisoire de la table "+str(newDataBase[i][0])+" par celui de votre choix : ")
									
									if not newTableName == '':
										newDataBase[i][0] = newTableName
										newDataBase[i][2][0] = newTableName
								
								try:
									dbh.createNewData(name_DataBase,newDataBase):

									print("La nouvelle base de donnee a bien ete cree")
									decomp = input("Attention l'application continue a tourner sur l'ancienne base de donnee")
									main_menu()
								
								except Exception:
									decomp_not= input("Une erreur c'est produite lors de la creation de la nouvelle base de donnee\n Veuillez verifier les donnees que vous avez rentre")
									main_menu()
							
							else:
								print("le caractere que vous avez rentre n'est pas valide")
								analyse()
						
						elif not3NF == "N" or not3NF == "n":
							analyse()
						
						else:
							print("le caractere que vous avez rentre n'est pas valide")
							analyse()

					else:
						
						if dbh.isBcnf(table_name):
							bcnf = input("Votre schema est en BCNF")
							main_menu()
						
						else:
							not_bcnf = input("Votre schema est en 3nf mais n est pas en BCNF")
							analyse()
							




			elif option == 5:
				main_menu()





			else:
				error_int=input("Le nombre n'est pas valide")
				analyse()





		except ValueError:
			except_error=input("Une erreur c'est produite lors d'une operation")





def main_menu():

	"""
	fonction contenant le menu principal de l'application
	"""

	cls()
	print("Veuillez choisir votre fonctionnalite :")
	print("1. Ajouter une dependance")
	print("2. Modifier une dependance")
	print("3. Supprimer une dependance")
	print("4. Analyser des dependances")
	print("5. Changer de base de donnee")
	print("6. Visionner vos dependances fonctionnelles")
	print("7. Quitter l'application")

	try:
		choice = input("Entrez le nombre : ")
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
				empty_table=input("Vous n'avez pas encore de dependances fonctionnelles")
				main_menu()

			else:
				increment = 1

				for line in tableau:
					print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle : "+line[1]+"-->"+line[2])
					increment += 1
				back=input("Retour au menu principal")
				main_menu()

		elif fonctio == 7:
			exit()

		else:
			error_int=input("L'option que vous avez choisi n'existe pas")
			main_menu()

	except ValueError:
		except_error=input("Une erreur c'est produite lors d'une operation")
		main_menu()





def init():

	"""
	fonction initiale permettant de choisir la base de donnee
	"""


	bdd=input("Inserer la base de donnee:")
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
	os.system('cls' if os.name =='nt' else 'clear')
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

