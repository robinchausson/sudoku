import grille_backend as gridb

class Solveur(gridb.Grille):
    """ Grille avec des méthodes supplémentaires pour obtenir les solutions """
    def __init__(self, grille:list, n:int):
        super().__init__(n)
        self.fill(grille)
        self.tabGrille = grille  # On garde le tableau pour les solutions multiples
        self.pileCaseAResoudre = self.__getCaseAResoudre()
        self.pileCaseResolu = gridb.Pile()
        self.nbCaseAResoudre = self.pileCaseAResoudre.longueur()
        self.solutions = []

    def __getCaseAResoudre(self):
        """ Récupérer dans une pile les case à résoudre """
        pile = gridb.Pile()
        for i in range(self.size):
            for j in range(self.size):
                if self.grille[i][j] not in self.casePossibilites:
                    case = gridb.Case(self.casePossibilites, i, j)
                    pile.empiler(case)
        return pile
    
    def modifyCase(self, case)->bool:
        valeur = case.getNewValue()
        i, j = case.getPos()
        if self.isPossible(i, j, valeur):
            self.grille[i][j] = valeur
            self.pileCaseResolu.empiler(case)
            return True
        elif case.hasNewValue():
            return self.modifyCase(case)
        elif not self.pileCaseResolu.isEmpty():
            # Remettre à 0 est nécessaire pour ne pas retirer des possibilités au parent
            self.grille[i][j] = 0
            # On met la dernière case résolu dans la pile à résoudre, mais il ne faut pas oublier
            # de lui redonner toutes les cases potentiels ! On la recreer donc complétement
            case = gridb.Case(self.casePossibilites, i, j)
            self.pileCaseAResoudre.empiler(case) 
            return self.modifyCase(self.pileCaseResolu.depiler())
        # Quand il n'y a pas de solution
        else:
            return False
    
    def getSolution(self):
        """ Renvoie la solution du Sudoku dans un type Solveur() """
        while not self.pileCaseAResoudre.isEmpty():
            case = self.pileCaseAResoudre.depiler()
            if not self.modifyCase(case):
                return Solveur(gridb.Grille(self.size).toList(), self.size)
        
        # Ce que l'on renvoit
        newGrille = Solveur(self.grille, self.size)

        # On remet au propre notre Solveur()
        self = Solveur(self.tabGrille, self.size)

        return newGrille
    
    def getAllSolutions(self)->list:
        """ Renvoie les solution du Sudoku dans une liste de Solveur()"""
        self.solutions = []
        
        # Pour chaque case à résoudre
        for i in range(self.nbCaseAResoudre):
            # On reset la pile des cases à résoudres (remplissage) et on vide les cases résolues
            self.grille = Solveur(self.tabGrille, self.size).grille
            self.pileCaseAResoudre = Solveur(self.tabGrille, self.size).__getCaseAResoudre()
            self.pileCaseResolu = gridb.Pile()

            # On la place en début de pile
            self.pileCaseAResoudre.pile[i], self.pileCaseAResoudre.pile[0] = self.pileCaseAResoudre.pile[0], self.pileCaseAResoudre.pile[i]
            premiereCase = self.pileCaseAResoudre.pile[0]
            valeursPossiblePremiereCase = premiereCase.valeursPossible
            # Tant qu'elle a des valeurs possible, on cherche des solutions
            for valeur in valeursPossiblePremiereCase:
                # On reset la pile des cases à résoudres (remplissage) et on vide les cases résolues
                self.grille = Solveur(self.tabGrille, self.size).grille
                self.pileCaseAResoudre = Solveur(self.tabGrille, self.size).__getCaseAResoudre()
                self.pileCaseResolu = gridb.Pile()

                # On la place en début de pile
                self.pileCaseAResoudre.pile[i], self.pileCaseAResoudre.pile[0] = self.pileCaseAResoudre.pile[0], self.pileCaseAResoudre.pile[i]
                premiereCase = self.pileCaseAResoudre.pile[0]
                premiereCase.valeursPossible = [valeur]

                solution = self.getSolution()
                if solution.isSolutionOk():
                    if solution.toList() not in self.solutions:
                        self.solutions.append(solution.toList())

        # On repasse les solutions sous forme de grille
        for i in range(len(self.solutions)):
            self.solutions[i] = Solveur(self.solutions[i], self.size)
            
        return self.solutions
    
    def countSolutions(self):
        """ Renvoie le nombre de solutions """
        return len(self.getAllSolutions()) if len(self.getAllSolutions()) == 0 else len(self.solutions) 
    
    def isSolutionOk(self)->bool:
        for i in range(self.size):
            row = self.getRow(i)
            compteur = [row.count(i) for i in row]
            compteurSouhaite = [1 for i in range(self.size)]
            if compteur != compteurSouhaite or 0 in row:
                return False
        return True


