import grille_backend as gridb
import grille_frontend as gridf
import tkinter as tk

def main():
    # --- Test --- #
    grille = gridb.Grille(9)
    grille.fill()
    grille.trim(75)
    
    root = tk.Tk()
    root.geometry("384x460")
    app = gridf.SudokuGrid(master=root, initial_grid=grille.toList())
    app.mainloop()

if __name__ == '__main__':
    main()
    
