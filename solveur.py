import grille_backend as gridb

class Solveur(gridb.Grille):
    def __init__(self, grille:list, n:int):
        super().__init__(n)
        self.fill(grille)
        self.fileCaseAResoudre = self.__getCaseAResoudre()
        self.pileCaseResolu = gridb.Pile()

    def __getCaseAResoudre(self)->list:
        """ Récupérer dans une pile les case à résoudre """
        file = gridb.File()
        for i in range(self.size):
            for j in range(self.size):
                if self.grille[i][j] not in self.casePossibilites:
                    case = gridb.Case(self.casePossibilites, i, j)
                    file.enfiler(case)
        return file
    
    def getSolution(self):
        """ Renvoie la solution du Sudoku dans un type Solveur() """
        while not self.fileCaseAResoudre.isEmpty():
            case = self.fileCaseAResoudre.defiler()
            self.modifyCase(case)
            
        newGrille = Solveur(self.grille, self.size)
        return newGrille
    
    def modifyCase(self, case):
        valeur = case.getNewValue()
        i, j = case.getPos()
        if self.isPossible(i, j, valeur):
            self.grille[i][j] = valeur
            self.pileCaseResolu.empiler(case)
        elif case.hasNewValue():
            self.modifyCase(case)
        elif not self.pileCaseResolu.isEmpty():
            self.grille[i][j] = 0
            # On remet l'ancienne case résolu dans la file, mais il ne faut pas oublier
            # de lui redonner toutes les cases potentiels ! On la recreer donc complétement
            case = gridb.Case(self.casePossibilites, i, j)
            self.fileCaseAResoudre.enfiler(case) 
            self.modifyCase(self.pileCaseResolu.depiler())
        # Ce cas n'arrive jamais normalement mais il est bon de le laisser pour le debug au cas où
        else:
            print("ELSE DE modifyCase()")
            print(self)
            return False
    
    def isSolutionOk(self)->bool:
        for i in range(self.size):
            row = self.getRow(i)
            compteur = [row.count(i) for i in row]
            compteurSouhaite = [1 for i in range(self.size)]
            if compteur != compteurSouhaite or 0 in row:
                print(f"Il y a un problème dans la solution (ligne {i+1})")
                return False
        print("----------------------------------------\nLa grille a été correctement solutionnée\n----------------------------------------")
        return True

# --- Test --- #
grille = gridb.Grille(9)
grille.fill()

print('La solution :')
print(grille)

grille.trim(30)

print('Avec des trous : ')
print(grille)

solveur = Solveur(grille.toList(), grille.size)
solution = solveur.getSolution()
print('Solutionné : ')
print(solution)

solution.isSolutionOk()