import random

class Grille: 
    """ Permet de créer une grille carré de sudoku"""

    def __init__(self, n:int):
        # Creation d'une grille vierge ne contenant que des 0
        self.grille = [[0 for i in range(n)] for i in range(n)]
        self.size = n
        self.pileCase = Pile()
        # Nombre possible pour les cases (le tuple sert à ce que la liste ne soit pas modifier dans les appels de méthode)
        self.casePossibilites = tuple([x for x in range(1, self.size+1)])

    def fill(self, tab=None):
        """ Remplit la grille avec les nombre de 1 à self.size de manière aléatoire
        (en respectant les règles du Sudoku) ou remplit à partir d'un tableau passé en paramètre
        (mais ne vérifie pas les règles du Sudoku) """

        if tab is None:
            i = 0
            j = 0
            while i < 9 and j < 9:
                # On essaye d'ajouter une case
                case = Case(self.casePossibilites, i, j)
                self.insertCase(case)

                # On récupère les informations sur la case qui a vraiment été ajoutée
                caseAjoute = self.pileCase.depiler()
                self.pileCase.empiler(caseAjoute)
                i, j = caseAjoute.getPos()

                # On modifie le i et le j en conséquence
                if j + 1 == self.size:
                    i += 1
                    j = 0
                else:
                    j += 1
                
        else:
            assert len(tab) == self.size, "Le tableau que vous voulez rentrer doit être de la même taille que la grille"
            # Permet de vraiment copier et pas seulement de faire un lien vers tab
            for i in range(self.size):
                for j in range(self.size):
                    self.grille[i][j] = tab[i][j]

    def trim(self, n=17):
        """ Supprime aléatoirement certaines cases et laisse n cases remplies (par défaut 5)"""
        assert self.size**2 > n >= 17, "Vous devez laisser au moins 17 cases remplies"

        for i in range((self.size**2)-n):
            estTrimer = False
            while not estTrimer:
                i = random.randint(0, self.size-1)
                j = random.randint(0, self.size-1)
                if self.grille[i][j] != ' ':
                    self.grille[i][j] = ' '
                    estTrimer = True
        
    def isPossible(self, i, j, nb):
        """ Renvoie vrai si l'on peut mettre le nombre nb aux coordonnées i,j, faux sinon"""

        column = self.getColumn(j)
        row = self.getRow(i)
        zone = self.getZone(i, j).toList()

        return (nb not in column) and (nb not in row) and (nb not in zone)
            
    def insertCase(self, case):
        valeur = case.getNewValue()
        i, j = case.getPos()
        if self.isPossible(i, j, valeur):
            self.grille[i][j] = valeur
            self.pileCase.empiler(case)
        elif case.hasNewValue():
            self.insertCase(case)
        elif not self.pileCase.isEmpty():
            self.grille[i][j] = 0
            self.insertCase(self.pileCase.depiler())
        # Ce cas n'arrive jamais normalement mais il est bon de le laisser pour le debug au cas où
        else:
            print("plus d'option")
            print(self)
            return False
        
    def getColumn(self, j:int) -> list:
        """ Retourne la j-eme colonne """
        colonne = []
        for i in range(self.size):
            for k in range(self.size):
                if j == k:
                    colonne.append(self.grille[i][k])
        return colonne
        
    def getRow(self, i:int) -> list:
        """ Retourne la i-eme ligne """
        return self.grille[i]
    
    def getZone(self, i, j):
        """ Retourne la Zone (aussi appelé bloc ou région) de type Zone de l'élément aux coordonnées i,j """

        assert 0 <= i < self.size, f"L'indice i doit être compris entre 0 et {self.size-1} compris"
        assert 0 <= j < self.size, f"L'indice j doit être compris entre 0 et {self.size-1} compris"
        assert self.size**(1/2).is_integer(), "Pour pouvoir récupérer un Zone, la grille doit être d'une taille carré (4, 9, 16, 25)"
       
        # On note que le nombre de zones correspond à la taille de la grille
        # La taille d'une zone vaut la racine carré de la taille de grille.
        zoneSize = int(self.size**(1/2))
        
        # On regarde la ligne sur laquelle se trouve l'élément
        debut_zone_i = int(i//zoneSize)*zoneSize
        fin_zone_i = debut_zone_i + zoneSize

        # On regarde la colonne sur laquelle se trouve l'élément
        debut_zone_j = int(j//zoneSize)*zoneSize
        fin_zone_j = debut_zone_j + zoneSize

        tab = self.grille[debut_zone_i:fin_zone_i]
        for k in range(zoneSize):
            tab[k] = tab[k][debut_zone_j:fin_zone_j]

        newZone = Zone(zoneSize)
        newZone.fill(tab)

        return newZone
                
    def isFillOk(self)->bool:
        for i in range(self.size):
            row = self.getRow(i)
            compteur = [row.count(i) for i in row]
            compteurSouhaite = [1 for i in range(self.size)]
            if compteur != compteurSouhaite or 0 in row:
                print(f"Il y a un problème dans la grille (ligne {i+1})")
                return False
        print("----------------------------------------\nLa grille a été correctement générée\n----------------------------------------")
        return True
    
    def toList(self)->list:
        return self.grille
    
    def __repr__(self):
        s = ''
        for i in range(self.size):
            if i%(self.size**(1/2)) == 0:
                s += ' -'*self.size
                s += '\n'
            for j in range(self.size):
                s += str(self.grille[i][j])
                if (j+1) % (self.size**(1/2)) == 0:
                    s += ' | '
                else:
                    s += ' '
            s += '\n'
        return s
    
class Zone(Grille):
    """ Sous-division d'une grille """
    def __init__(self, n:int):
        super().__init__(n)

    def toList(self):
        liste = []
        for i in range(self.size):
            for j in range(self.size):
                liste.append(self.grille[i][j])
        return liste

class Case():
    """ Case à ajouter au Sudoku"""
    def __init__(self, valeursPossible:tuple, i, j):
        self.valeursPossible = list(valeursPossible)
        self.valeur = 0
        self.i = i
        self.j = j

    def getNewValue(self)->int:
        """ Renvoie une nouvelle valeur pour la case, faux si la case n'a plus de valeur possible """
        if self.hasNewValue():
            self.valeur = self.valeursPossible[random.randint(0, len(self.valeursPossible)-1)] # On change la valeur actuel
            self.valeursPossible.pop(self.valeursPossible.index(self.valeur)) # On supprime la valeur que l'on vient de prendre
            return self.valeur
        return False
    
    def hasNewValue(self):
        """ Renvoie vrai si la case peut prendre de nouvelles valeurs, faux sinon"""
        return len(self.valeursPossible) != 0
    
    def getPos(self):
        return self.i, self.j

    def __repr__(self):
        return f"{self.valeur} ({self.i}, {self.j})"

class Pile():
    """ Structure de donnée classique d'une pile """

    def __init__(self):
        self.pile = []

    def empiler(self, elt):
        """ Empile un élément """
        self.pile.append(elt)

    def depiler(self):
        """ Dépile un élément """
        return self.pile.pop()
    
    def isEmpty(self):
        """ Renvoie vrai si la pile est vide, faux sinon"""
        return len(self.pile) == 0
    
    def __repr__(self):
        s = ""
        for elt in self.pile:
            s += elt.__repr__() + ', '
        return s[:-2]

class File():
    """ Structure de donnée classique d'une file """
    def __init__(self):
        self.file = []

    def enfiler(self, elt):
        self.file.insert(0, elt)

    def defiler(self):
        return self.file.pop()
    
    def isEmpty(self):
        """ Renvoie vrai si la file est vide, faux sinon"""
        return len(self.file) == 0

    def __repr__(self):
        s = ''
        for i in range(len(self.file)):
            s += self.file[i].__repr__() + ', '
        return s[:-2]

""""
# --- TEST --- #
grille = Grille(9)
# tab = [['a','b'], ['c','d']]
grille.fill()
grille.isFillOk()
grille.trim(50)
print(grille)
# zone = grille.getZone(0, 0).toList()
# print(zone)
"""
