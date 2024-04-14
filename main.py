import grille_backend as gridb
import solveur as grids

def main():
    # --- Test --- #
    grille = gridb.Grille(9)
    # Evite de recharger une grille à chaque fois
    # grilleTab = [[' ', 2, ' ', 7, ' ', ' ', 5, 1, 6], [' ', ' ', ' ', 4, ' ', 5, ' ', 9, 7], [' ', 5, 9, 3, ' ', ' ', ' ', ' ', 4], [4, 7, 2, 9, ' ', ' ', 6, 5, 1], [' ', ' ', ' ', ' ', ' ', 4, ' ', 7, 2], [' ', ' ', ' ', 2, ' ', 6, 8, 4, ' '], [' ', ' ', ' ', 8, ' ', ' ', ' ', ' ', ' '], [9, 1, ' ', ' ', ' ', 3, 4, ' ', 8], [' ', ' ', ' ', ' ', ' ', ' ', 7, ' ', 9]]
    grille.fill()
    print('La solution :')
    print(grille)

    # grilleSansSolution = [[1, 3, 5, 4, 6, 9, 7, 1, 2], [6, 9, 4, 1, 7, 2, 8, 3, 5], [1, 7, 2, 3, 5, 8, 9, 4, 6], [2, 8, 7, 9, 4, 1, 5, 6, 3], [9, 1, 6, 2, 3, 5, 4, 8, 7], [4, 5, 3, 7, 8, 6, 2, 9, 1], [7, 6, 8, 5, 9, 3, 1, 2, 4], [5, 2, 9, 6, 1, 4, 3, 7, 8], [3, 4, 1, 8, 2, 7, 6, 5, 9]] 
    # grille.fill(grilleSansSolution)
    # print("Grille sans solution :")
    # print(grille)

    grille.trim(40)
    print('Avec des trous : ')
    print(grille)

    solveur = grids.Solveur(grille.toList(), grille.size)
    # print("Une solution :")
    # print(solveur.getSolution())
    solutions = solveur.getAllSolutions()
    
    print('\nSolution(s) : ')
    for i in range(len(solutions)):
        print(solutions[i])
    print(f"Nombre de solutions : {len(solutions)}")
if __name__ == '__main__':
    main()