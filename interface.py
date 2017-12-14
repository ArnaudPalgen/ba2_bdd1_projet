from dfHandler import *
from DataBaseHandler import *
import os

dbh = None


def add():

    """fonction permettant l ajout de dependance fonctionelle"""

    cls()
    print("rentrer les elements suivants :")
    addTables = input("nom de la table : ")
    aLhs = input("partie gauche de la dependance fonctionnelle(si vous avez plusieurs elements separez les par des espaces et non des virgules) : ")
    addRhs = input("partie droite de la dependance fonctionnelle : ")

    addLhs=cleaning(aLhs)
    
    dep=dbh.insertDep(addTables, addLhs, addRhs)
    if dep == False:
        error_add=input("votre dependance n'a pas pu etre ajoutee. Sorry :( (verifiez que la dependance n'existe pas deja ou a ete bien ecrite) ")
        main_menu()

    print_dep=input("Votre dependance a bien ete ajoutee : "+ addLhs + "-->" +addRhs)
    main_menu()





def edit():

    """fonction permettant la modification de dependance fonctionelle"""

    cls()

    tableau = dbh.getAllDep()

    if len(tableau)== 0:
        empty_table=input("la table ne contient aucun element a modifier")
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
                    newLhs=cleaning(new)
                    retour=dbh.editDep(tableau[nbre -1][0],tableau[nbre -1][1],tableau[nbre -1][2],newLhs, dbh.LHS)
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

    """fonction de suppression de dependance"""

    cls()

    tableau = dbh.getAllDep() 
    if len(tableau)== 0:
        empty_table=input("la table ne contient aucun element a supprimer")
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
                        delete()
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
    option d analyse
    """
    cls()
    tableau = dbh.getAllDep() #ajout de getAllDep à dfHandler
    if len(tableau)== 0:
        empty_table=input("la table ne contient aucun element a analyser")
        main_menu()
    else:
        try:
        
            print("que voulez-vous faire?")
            print("1. determiner les cles et supercles d'un schema")
            print("2. determiner les consequences logiques")
            print("3. restreindre le schema")
            print("4. BCNF ou 3NF")
            print("5. retour au menu principal")
            nbre = input("entrez le nbre: ")
            option = int(nbre)

            if option ==1:
                try:
                
                    choice=input("voulez vous les cles(1) ou les supercles(2)?")
                    cle=int(choice)
                    if cle ==1:
                        getCle()
                    elif cle == 2:
                        getSuperCle()
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
            				print_LC_OK = input("votre dependance est bien une consequence logique")
            				analyse()
            			else:
            				print_LC_NOT = input("votre dependance n'est pas une consequence logique")
            				analyse()
            	except ValueError:
                    except_error=input("invalid syntax, try again")
                    analyse()





            elif option == 3:
                pass





            elif option == 4:
                print("quelle table voulez-vous determiner?")
                t= dbh.getAllTableInFuncDep()
                for i in t:
                    print(i)
                table_name=input("entrez le nom de la table: ")
                if table_name in t == False:
                    table_name = input("erreur de synthaxe veuillez reecrire le nom de la table :")
                else:
                    """
                    if is3nf(b) == False:
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
                    if dbh.isBcnf(table_name):
                        bcnf = input("votre schema est en BCNF")
                        main_menu()
                    else:
                        not_bcnf = input("votre schema est en 3nf mais n est pas en BCNF voulez vous faire une decomposition en BCNF? (Y/N) :")
                        if not_bcnf == "Y" or not_bcnf == "y":
                            decomp_bcnf = input("la decomposition en BCNF serait : "+ getDecompositionBcnf())
                            main_menu()
                        elif not_bcnf == "N" or not_bcnf == "n":
                            analyse()
                        else:
                            error_synth=input("erreur synthaxe")
                            analyse()





            elif option == 5:
                main_menu()

            



            else:
                error_int=input("le nombre n est pas valide")
                analyse()
                
        



        except ValueError:
            except_error=input("invalid syntax, try again")





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
            error_int=input("invalid number, try again")
            main_menu()
    except ValueError:
        except_error=input("invalid syntax, try again")
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

def cleaning(x):


    if x[0] == " ":
        x[1:]
        cleaning(x)
    if x[len(x)-1] ==  " ":
        x.pop()
        cleaning(x)


    for i in range(0,len(x)):
        if x[i] ==',' and x[i+1] == ' ':
            x[0:i]+x[i+1:]
            i+=2
        elif x[i] ==',' and x[i+1] !=' ':
            x.replace(i,',',' ')
            i+=1
        else:
            i+=1

    return x





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

