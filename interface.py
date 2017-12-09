from dfHandler import *
from DataBaseHandler import *
import os

dbh = None


def add():

    """fonction permettant l ajout de dependance fonctionelle"""

    cls()
    print("rentrer les elements suivants :")
    aTables = input("nom de la table : ")
    aLhs = input("partie gauche de la dependance fonctionnelle : ")
    aRhs = input("partie droite de la dependance fonctionnelle : ")

    
    dep=dbh.insertDep(aTables, aLhs, aRhs)
    if dep == False:
        b=input("votre dependance n'a pas pu etre ajoutee. Sorry :( ")
        main_menu()

    jr=input("Votre dependance a bien ete ajoutee : "+ aLhs + "-->" +aRhs)
    main_menu()





def edit():

    """fonction permettant la modification de dependance fonctionelle"""

    cls()

    tableau = dbh.getAllDep()

    if len(tableau)== 0:
        a=input("la table ne contient aucun element a modifier")
        main_menu()
    else:
        print("quelle ligne voulez-vous modifier?")
        increment = 1
        for line in tableau:
            print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
            increment  += 1
        
        try:
            a = input("numero de la ligne : ")
            nbre = int(a)
            if nbre > (len(tableau)) or nbre <= 0:
                e=input("error integer")
                edit()
            else:
                cls()

                print("que voulez-vous modifier?")
                print("1. table")
                print("2. lhs")
                print("3. rhs")

                b = input("entrez le nbre: ")
                newnbre = int(b)
                new = input("rentrez les nouvelles donnees :")

                if newnbre == 1: 
                    retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.TABLE)
                    if retour:

                    	print("votre donnee a bien ete modifiee")
                    	t=input("la nouvelle dependance est :"+ new +" "+ tableau[nbre -1][1] + "-->" + tableau[nbre -1][2])
                    	main_menu()
                    else:
                        	x=input("une erreur est apparue lors de la modification de votre dependance")
                        	main_menu()

                elif newnbre == 2:
                    retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.LHS)
                    if retour:
                    	print("votre donnee a bien ete modifiee")
                    	l=input("la nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ new + "-->" + tableau[nbre -1][2])
                    	main_menu()
                    else:
                        	x=input("une erreur est apparue lors de la modification de votre dependance")
                        	main_menu()

                elif newnbre == 3:
                    if new.count(" ") != 0:
                        print("error syntax")
                        edit()
                    else:
                        retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],new, dbh.RHS)
                        
                        if retour:
                       		print("votre donnee a bien ete modifiee")
                        	r=input("la nouvelle dependance est :"+ tableau[nbre -1][0] +" "+ tableau[nbre -1][1] + "-->" + new)
                        	main_menu()
                        else:
                        	x=input("une erreur est apparue lors de la modification de votre dependance")
                        	main_menu()

                else:
                	r=input("error integer")
                	edit()
                
                

        except ValueError:
            print("invalid syntax, try again")

            



def delete():

    """fonction de suppression de dependance"""

    cls()

    tableau = dbh.getAllDep() 
    if len(tableau)== 0:
        d=input("la table ne contient aucun element a supprimer")
        main_menu()

    else:
        print("quelle ligne voulez-vous supprimer?")
        increment = 1
        for line in tableau:
            print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle :"+line[1]+" --> "+line[2])
            increment += 1

        try: 
            a = input("numero de la ligne : ")
            nbre = int(a)

            if nbre > (len(tableau)) or nbre <= 0:
                print("error integer")

            else:
                cls()

                verif = input("la suppression est definitive voulez-vous vraiment continuer?(Y/N)")
                if verif == "Y" or verif == "y":
                    if dbh.removeDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
                        d=input("la dependance "+ tableau[nbre -1][1]+"-->"+tableau[nbre -1][2]+" venant de la table "+tableau[nbre -1][0]+" a bien ete supprimee")
                        main_menu()
                    else:
                        print("une erreur c est produite pendant l'operation")    
                elif verif == "N" or verif == "n":
                    main_menu()
                else:
                    print("erreur synthaxe")
                    delete()
        except ValueError:
            print("invalid syntax, try again")





def analyse():
    """
    option d analyse
    """
    cls()
    tableau = dbh.getAllDep() #ajout de getAllDep à dfHandler
    if len(tableau)== 0:
        z=input("la table ne contient aucun element a analyser")
        main_menu()
    else:
        try:
        
            print("que voulez-vous faire?")
            print("1. determiner les cles et supercles du schema")
            print("2. determiner les consequences logiques")
            print("3. restreindre le schema")
            print("4. BCNF ou 3NF")
            print("5. retour au menu principal")
            nbre = input("entrez le nbre: ")
            opti = int(nbre)

            if opti ==1:
                c=input("voulez vous les cles(1) ou les supercles(2)?")
                cle=int(c)
                if cle ==1:
                    getCle()
                elif cle == 2:
                    getSuperCle()
                else:
                    print("le nombre est inconnu")
                    analyse()









            elif opti == 2:

            	cls()
            	increment =1
            	for line in tableau:
            		print(str(increment)+".  Table: "+line[0]+" dependance fonctionnelle :"+line[1]+" --> "+line[2])
            		increment +=1
            	try:
            		a= input("numero de la dependance a analyser :")
            		nbre = int(a)

            		if nbre > (len(tableau)) or nbre <= 0:
            			b=input("error integer")
            			analyse()
            		else:
            			if dbh.isLogicConsequence(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2]):
            				g = input("votre dependance est bien une consequence logique")
            				analyse()
            			else:
            				h = input("votre dependance n'est pas une consequence logique")
            				analyse()
            	except ValueError:
            		print("invalid syntax, try again")










            elif opti == 3:
                pass











            elif opti == 4:
                print("quelle table voulez-vous determiner?")
                t= dbh.getAllTableInFuncDep()
                for i in t:
                    print(i)
                b=input("entrez le nom de la table: ")
                """
                if is3nf == False:
                    c = input("votre schema n est pas en 3nf donc ne sera pas en BCNF voulez vous faire une decomposition? Y/N")
                    if verif == "Y" or verif == "y":
                        print("la decomposition en 3nf serait : "+ getDecomposition3nf())
                        d = input("la decomposition en BCNF serait : "+ getDecompositionBcnf())
                        main_menu()
                    elif verif == "N" or verif == "n":
                        analyse()
                    else:
                        print("erreur synthaxe")
                        analyse()

                else:
                """
                if dbh.isBcnf(b):
                    b = input("votre schema est en BCNF")
                    main_menu()
                else:
                    c = input("votre schema est en 3nf mais n est pas en BCNF voulez vous faire une decomposition en BCNF? Y/N")
                    if verif == "Y" or verif == "y":
                        d = input("la decomposition en BCNF serait : "+ getDecompositionBcnf())
                        main_menu()
                    elif verif == "N" or verif == "n":
                        analyse()
                    else:
                        print("erreur synthaxe")
                        analyse()














            elif opti == 5:
                main_menu()

            else:
                print("le nombre n est pas valide")
                analyse()
                
        except ValueError:
            print("invalid syntax, try again")





def main_menu():

    """fonction menu de base du programme"""
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
        a = input("entrez le nombre : ")
        fonctio = int(a)

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
        		d=input("vous n'avez pas encore de dependances fonctionnelles")
        		main_menu()

        	else:
        		increment = 1
        		for line in tableau:
        			print(str(increment)+".  Table: "+line[0]+"  dependance fonctionnelle : "+line[1]+"-->"+line[2])
        			increment += 1
        		defp=input("retour au menu principal")
        		main_menu()
        elif fonctio == 7:
            print("###############################################")
            print("###############################################")
            print("##### #####  #####  ####   ####   #    #  #####")
            print("#     #   #  #   #  #   #  #   #   #  #   #    ")
            print("#  ## #   #  #   #  #   #  ####     ##    #####")
            print("#  #  #   #  #   #  #   #  #   #    ##    #    ")
            print("####  #####  #####  ####   ####     ##    #####")
            print("###############################################")
            print("###############################################")
            exit()
        else:
            print("invalid number, try again")
            main_menu()
    except ValueError:
        print("invalid syntax, try again")
        main_menu()





def init():

    """ fonction pour l insertion de la base de donnee"""
    
    
    bdd=input("inserer la base de donnee:")
    global dbh
    dbh = DfHandler(bdd)
    main_menu()





def cls():
    
    """ fonction de clean d ecran """
    
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

