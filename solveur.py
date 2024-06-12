import grille_backend as gridb
import time
import tkinter as tk

class Solveur(gridb.Grille):
    """ Grille avec des méthodes supplémentaires pour obtenir les solutions """

    def __init__(self, grille:list, n:int, root=None, grille_front=None):
        super().__init__(n)
        self.fill(grille)
        self._tabGrille = grille  # On garde le tableau pour les solutions multiples
        self._caseAResoudre = [] # On récupère les cases potentiels
        self.grille_front = grille_front
        self.root = root

        self.pileCaseAResoudre = gridb.Pile()
        self.pileCaseResolu = gridb.Pile()
        self.solutions = []

    def __getCaseAResoudre(self)->list:
        """ Récupérer dans une liste les case à résoudre """
        cases = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grille[i][j] not in self.casePossibilites:
                    case = gridb.Case(self.__getValeursPossible(i,j), i, j)
                    cases.append(case)
        return cases
    
    def __getValeursPossible(self, i, j)->list:
        """ Récupère les valeurs vraiment possible pour une case (on retire tout ce qui se trouve sur les ligne ou colonne)"""
        valeurs = []
        # Le tmpSolv permet de ne pas regarder les potentiels case déjà résolu
        tmpSolv = Solveur(self._tabGrille, self.size, self.root, self.grille_front)
        for valeur in self.casePossibilites:
            if tmpSolv.isPossible(i, j, valeur):
                valeurs.append(valeur)
        return valeurs
    
    def modifyCase(self, case)->bool:
        # On met un petit timeout pour voir les choses
        i, j = case.getPos()
        if case.hasNewValue():
            valeur = case.getNewValue()
            if self.isPossible(i, j, valeur):
                self.grille[i][j] = valeur
                self.grille_front[i][j].delete(0,tk.END)
                self.grille_front[i][j].insert(0, valeur)
                self.root.update()
                time.sleep(0.1)
                self.pileCaseResolu.empiler(case)
                return True
            else:
                return self.modifyCase(case)
            
        elif not self.pileCaseResolu.isEmpty():
            # Remettre à 0 est nécessaire pour ne pas retirer des possibilités au parent
            self.grille[i][j] = 0
            self.grille_front[i][j].delete(0,tk.END)
            self.grille_front[i][j].insert(0, ' ')
            self.root.update()
            time.sleep(0.1)
            # On met la dernière case résolu dans la pile à résoudre, mais il ne faut pas oublier
            # de lui redonner toutes les cases potentiels ! On la recreer donc complétement
            case = gridb.Case(self.__getValeursPossible(i,j), i, j)
            self.pileCaseAResoudre.empiler(case) 
            return self.modifyCase(self.pileCaseResolu.depiler())
        # Quand il n'y a pas de solution
        else:
            return False
    
    def getSolution(self)->list:
        """ Renvoie une solution du Sudoku sous forme de liste (sans utiliser getAllSoltions())"""
        caseAResoudre = self.__getCaseAResoudre()
        self.pileCaseAResoudre = gridb.Pile(caseAResoudre)
        while not self.pileCaseAResoudre.isEmpty():
            case = self.pileCaseAResoudre.depiler()
            self.modifyCase(case)
        return self.toList()
    
    def isSolutionOk(self)->bool:
        for i in range(self.size):
            row = self.getRow(i)
            compteur = [row.count(j) for j in row]
            compteurSouhaite = [1 for j in range(self.size)]
            if compteur != compteurSouhaite or 0 in row:
                return False
        return True


