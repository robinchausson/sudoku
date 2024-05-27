import grille_backend as gridb
import copy


class Solveur(gridb.Grille):
    """ Grille avec des méthodes supplémentaires pour obtenir les solutions """

    def __init__(self, grille:list, n:int):
        super().__init__(n)
        self.fill(grille)
        self._tabGrille = grille  # On garde le tableau pour les solutions multiples
        self._caseAResoudre = [] # On récupère les cases potentiels

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
        tmpSolv = Solveur(self._tabGrille, self.size)
        for valeur in self.casePossibilites:
            if tmpSolv.isPossible(i, j, valeur):
                valeurs.append(valeur)
        return valeurs
    
    def modifyCase(self, case)->bool:
        i, j = case.getPos()
        if case.hasNewValue():
            valeur = case.getNewValue()
            if self.isPossible(i, j, valeur):
                self.grille[i][j] = valeur
                self.pileCaseResolu.empiler(case)
                return True
            else:
                return self.modifyCase(case)
            
        elif not self.pileCaseResolu.isEmpty():
            # Remettre à 0 est nécessaire pour ne pas retirer des possibilités au parent
            self.grille[i][j] = 0
            # On met la dernière case résolu dans la pile à résoudre, mais il ne faut pas oublier
            # de lui redonner toutes les cases potentiels ! On la recreer donc complétement
            case = gridb.Case(self.__getValeursPossible(i,j), i, j)
            self.pileCaseAResoudre.empiler(case) 
            return self.modifyCase(self.pileCaseResolu.depiler())
        # Quand il n'y a pas de solution
        else:
            return False
    
    def getAllSolutions(self)->list:
        """ Renvoie les solution du Sudoku dans une liste de Solveur()"""
        self.solutions = []
        
        self.grille = Solveur(self._tabGrille, self.size).grille
        self.pileCaseAResoudre = gridb.Pile(self.__getCaseAResoudre())
        self.pileCaseResolu = gridb.Pile()

        isASolution = True
        # On fais une résolution de la grille avec la case actuelle en premiere place
        while not self.pileCaseAResoudre.isEmpty():
            case = self.pileCaseAResoudre.depiler()
            if not self.modifyCase(case):
                isASolution = False
                break
        
        if isASolution:
            solution = self.toList()
            if solution not in self.solutions:
                self.solutions.append(solution)

        # On repasse les solutions sous forme de grille
        for i in range(len(self.solutions)):
            self.solutions[i] = Solveur(self.solutions[i], self.size)
            
        return self.solutions
    
    def isSolutionOk(self)->bool:
        for i in range(self.size):
            row = self.getRow(i)
            compteur = [row.count(j) for j in row]
            compteurSouhaite = [1 for j in range(self.size)]
            if compteur != compteurSouhaite or 0 in row:
                return False
        return True


