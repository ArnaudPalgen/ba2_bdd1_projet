from init import *

def add():
    """
    option de creation
    """
    print("rentrer les elements suivants :")
    aTables = input("nom de la table : ")
    aLhs = input("partie gauche de la dependance fonctionnelle : ")
    aRhs = input("partie droite de la dependance fonctionnelle : ")

    if aRhs.count(" ") != 0:
        print("error synthax")
        add()
    else:
        insertDep(aTables, aLhs, aRhs)
        print ("votre dependance a bien ete ajoutee")
        main_menu()

def edit():
    """
    option de modification
    """
    print("quelle ligne voulez-vous modifier?")
    tableau = getAllDep()
    for line in tableau:
        #print(line+".  Table: "+     +"relation: "+   +" --> "+   )
        
    try:
        nbre = input("numero de la ligne : ")

       if nbre >= tableau.len() -1 or nbre <= 0:
           print("error integer")
           
       else:
          print("que voulez-vous modifier?")
          print("1. table")
          print("2. lhs")
          print("3. rhs")
          nbre = input("entrez le nbre: ")
          new = input("rentrez les nouvelles donnees :")
          if nbre == 3 and new.count(" ") != 0:
             error
          else:
             print("votre donnee a bien ete modifiee")
             main_menu()
    except ValueError:
        print("invalid syntax, try again")
        

def delete():
    """
    option de suppression
    """
    print("quelle ligne voulez-vous supprimer?")
    #afficher nbre + chaque ligne de la table FuncDep
    nbre = input("numero de la ligne : ")
    """
       if nbre >= FuncDep.size -1 or nbre <= 0:
           error integer
       else:
          verif = input("la suppression est definitive voulez-vous vraiment continuer?(Y/N)")
          if verif = "Y" or verif = "y":
             print("votre dependance a bien ete supprimee")
             init()
          elif verif = "N" or verif = "n":
             delete()
          else:
             print("erreur synthaxe")
             delete()
             
    """
def main_menu():

    """
    fonction menu de base du programme
    """
    print("Veuillez choisir votre fonctionnalite :")
    print("1. ajouter")
    print("2. modifier")
    print("3. supprimer")
    print("4. analyse")
    print("5. quitter")

    try:
        a = input("entrez le nombre : ")
        fonctio = float(a)

        if fonctio == 1:
            add()
        elif fonctio == 2:
            edit()
        elif fonctio == 3:
            delete()
        elif fonctio == 4:
            analyse()
        elif fonctio == 5:
            print("goodbye")
        else:
            print("invalid number, try again")
            main_menu()
    except ValueError:
        print("invalid syntax, try again")
        main_menu()

def init():
    bdd=input("inserer la base de donnee:")
    #connect(bdd)
    main_menu()
init();
