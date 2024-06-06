import grille_backend as gridb
import grille_frontend as gridf
import customtkinter as ctk

def main():
    # --- Test --- #
    # grille = gridb.Grille(9)
    # grille.fill()
    # grille.trim(70)
    
    # root = tk.Tk()
    # root.geometry("384x460")
    # app = gridf.SudokuGrid(master=root, initial_grid=grille.toList())
    # app.mainloop()

    root = ctk.CTk()
    #app = gridf.WelcomeApp(root)
    app = gridf.SudokuApp(root, 'patrick')
    root.mainloop()

if __name__ == '__main__':
    main()
    
