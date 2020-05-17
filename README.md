## Projet du cours de Bases de données 1

## Dépendances fonctionnelles et normalisation
*Auteurs*: **Arnaud Palgen, Guillaume Proot**
*Professeur*: **Pierre Hauweele**

---
L'objectif de ce projet est d'implémenter un outil de gestion de dépendances
fonctionnelles sur des bases de données. Nous avons réaliser ce projet en Python 3.

### Utilisation de l'application
##### Exécution
- ` python3 main.py `

- Suivez les instructions à l'écran.

##### Remarques
- Pour utiliser une base de donnée existante, celle-ci doit se trouver dans le répertoire courant de ` main.py `

- Lorsque vous insérez une dépendance fonctionnelle (au format: lhs-->rhs): les attributs de lhs doivent être séparés par un espace. Il ne peut y avoir qu'un seul attribut dans rhs.

### Utilisation du module
Les fichiers `dataBaseHandler.py` et `dfHandler.py` sont respectivement le gestionnaire de base de donnee et le gestionnaire de dépendance fonctionnelle. 
Pour utiliser le module, importez `dataBaseHandler`


### Remarques générales

- Si vous indiquez une base de donnée qui n'existe pas une nouvelle base de donnée sera crée.
        
- Le fichier `testUnitaire.py` dans le dossier `misc` contient une série de tests unitaires.
