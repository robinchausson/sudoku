import tkinter as tk
import grille_backend as gridb

class SudokuGrid(tk.Frame):
    def __init__(self, master=None, initial_grid=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sudoku")

        self.configure(bg='white')
        self.grid(row=0, column=0, padx=10, pady=10)

        self.create_widgets(initial_grid)
        self.grille = gridb.Grille(9)
        self.grille.fill(initial_grid)

    def create_widgets(self, initial_grid):
        title_label = tk.Label(self, text="Sudoku", font=("Helvetica", 20, "bold"), bg='white')
        title_label.grid(row=0, column=0, columnspan=9, pady=(10, 20))

        self.grid_frame = tk.Frame(self, bg='black')
        self.grid_frame.grid(row=1, column=0, padx=10, pady=10)

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if initial_grid and initial_grid[i][j] != " ":
                    cell = tk.Label(self.grid_frame, text=str(initial_grid[i][j]), font=('Helvetica', 16, "bold"), width=2, bg='white')
                else:
                    cell = tk.Entry(self.grid_frame, width=2, font=('Helvetica', 16), justify='center')
                    cell.config(validate="key", validatecommand=(cell.register(lambda value, i=i, j=j: self.validate_input(value, i, j)), '%P'))
                cell.grid(row=i, column=j, padx=2, pady=2, ipady=5, ipadx=5)
                self.cells[i][j] = cell

                # Ajout des lignes de délimitation entre les sous-zones
                if (i in (2, 5)) and (j in (2, 5)):
                    line = tk.Frame(self.grid_frame, height=27, width=2, bg='black')
                    line.grid(row=i, column=j, rowspan=3, padx=(0, 10))
                    line = tk.Frame(self.grid_frame, height=2, width=27, bg='black')
                    line.grid(row=i, column=j, columnspan=3, pady=(0, 10))
        self.finish_label = tk.Label(self, text="", font=("Helvetica", 16), bg='white')
        self.finish_label.grid(row=2, column=0, columnspan=9)

    def validate_input(self, value, i, j):
        if value.isdigit() and int(value) in range(1, 10) and self.grille.isPossible(i, j, int(value)):
            self.grille.grille[i][j] = int(value)
            if self.grille.isFillOk():
                self.finish_label.config(text="Bravo, vous avez réussi !")
            return True
        elif value == "":
            return False
        else:
            return False