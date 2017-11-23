def add():
    """
    option de création
    """
    print("rentrer les éléments suivants :")
    aTables = input("nom de la table : ")
    aLhs = input("partie gauche de la dépendance fonctionnelle : ")
    aRhs = input("partie droite de la dépendance fonctionnelle : ")

    if aRhs.count(" ") != 0:
        print("error")
    else:
        print ("votre dépendance à bien été ajoutée")
        init()

def edit():
    """
    option de modification
    """
    print("quelle ligne voulez-vous modifier?")
    #afficher nbre + chaque ligne de la table FuncDep
    nbre = input("numero de la ligne : ")
    """
       if nbre >= FuncDep.size -1 or nbre <= 0:
           error integer
       else:
          print("que voulez-vous modifier?")
          print("1. table")
          print("2. lhs")
          print("3. rhs")
          nbre = input("entrez le nbre: ")
          new = input("rentrez les nouvelles données :")
          if nbre == 3 and new.count(" ") != 0:
             error
          else:
             print("votre donnée à bien été modifiée")
             init()
    """

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
             print("votre dependance à bien été supprimée")
             init()
          elif verif = "N" or verif = "n":
             delete()
          else:
             print("erreur synthaxe")
             delete()
             
    """
def init():

    """
    fonction menu de base du programme
    """
    print("Veuillez choisir votre fonctionnalité :")
    print("1. ajouter")
    print("2. modifier")
    print("3. supprimer")
    print("4. analyse")

    a = input("entrez le nombre : ")
    #rajouter erreur si input n'est pas un float
    fonctio = float(a)

    if fonctio == 1:
        add()
    elif fonctio == 2:
        edit()
    elif fonctio == 3:
        delete()
    elif fonctio == 4:
        analyse()
    else:
        print("error")
        init()


init();
