import customtkinter as ctk
from scoreboard import Scoreboard
from PIL import Image, ImageTk
import tkinter as tk
import grille_backend as gridb
from tkinter import font

class SudokuApp:
    def __init__(self, root, username, difficulty="Facile"):
        self.root = root
        self.username = username
        self.difficulty = difficulty
        self.score = 0
        self.root.title("Sudoku")
        self.root.geometry("1920x1080")
        ctk.set_appearance_mode("light")  # Utiliser le thème clair

        self.font_style = ctk.CTkFont(family="mincho", size=22)
        self.fg_color = "red"
        self.scoreboard = Scoreboard()

        self.create_widgets()

        grille = gridb.Grille(9)
        grille.fill()
        grille.trim(70)
        self.display_sudoku_grid(grille.toList())

        # Configurer les lignes et colonnes pour centrer la grille de Sudoku
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=2)

        self.time_elapsed = 0  # Initialisation du timer
        self.update_timer()  # Commence le timer

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.grid(row=0, column=1, pady=30, padx=20,sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        self.username_label = ctk.CTkLabel(self.frame, text=f"Joueur : {self.username} \n Difficulté : {self.difficulty}", font=self.font_style, width=300)
        self.username_label.grid(row=0, column=0, padx=20)

        self.restart_button = ctk.CTkButton(
            self.frame, text="Recommencer la partie", command=self.restart_game, 
            corner_radius=10, font=self.font_style, width=300, height=60, 
            fg_color=self.fg_color, hover_color="#144d75"
        )
        self.restart_button.grid(row=0, column=1)

        self.scoreboard_button = ctk.CTkButton(
            self.frame, text="Voir le scoreboard", command=self.show_scoreboard_window, 
            corner_radius=10, font=self.font_style, width=300, height=60, 
            fg_color=self.fg_color, hover_color="#144d75"
        )
        self.scoreboard_button.grid(row=0, column=2)

        self.best_score_label = ctk.CTkLabel(self.frame, text=f"Meilleur score : {self.scoreboard.get_best_score(self.username, self.difficulty)}", font=self.font_style, width=300)
        self.best_score_label.grid(row=1, column=0, padx=20)

        # Ajout du label du timer
        self.timer_label = ctk.CTkLabel(self.frame, text="00:00", font=self.font_style)
        self.timer_label.grid(row=1, column=1)

        self.best_score_label = ctk.CTkLabel(self.frame, text=f"Score : 0", font=self.font_style, width=300)
        self.best_score_label.grid(row=1, column=2, padx=20)

    def update_timer(self):
        minutes, seconds = divmod(self.time_elapsed, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        self.timer_label.configure(text=time_str)
        self.time_elapsed += 1
        self.root.after(1000, self.update_timer)

    def update_score(self, score): 
        self.best_score_label.configure(text=f"Score : {score}")

    def show_scoreboard_window(self):
        scoreboard_window = ctk.CTk()
        scoreboard_window.title("Scoreboard")
        scoreboard_window.geometry("800x600")

        scoreboard_frame = ctk.CTkFrame(scoreboard_window, corner_radius=10)
        scoreboard_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scoreboard_text = ctk.CTkTextbox(scoreboard_frame, corner_radius=10, font=self.font_style)
        scoreboard_text.pack(fill="both", expand=True, padx=10, pady=10)

        scores = self.scoreboard.get_scores()
        score_message = "Rang | Score | Difficulté | Temps | Pseudo \n"
        for i in range(len(scores)):
            entry = scores[i]
            if entry['level'] == "Facile":
                entry['level'] = "Facile     "
            elif entry['level'] == "Moyen":
                entry['level'] = "Moyen      "
            elif entry['level'] == "Difficile":
                entry['level'] = "Difficile  "
            score_message += f"{i+1}    | {entry['score']}   | {entry['level']}| {entry['time']} | {entry['name']} \n"
        scoreboard_text.insert("1.0", score_message)

        scoreboard_window.mainloop()

    def restart_game(self):
        self.root.destroy()
        root = ctk.CTk()
        app = WelcomeApp(root, self.username)
        root.mainloop()

    def display_sudoku_grid(self, sudoku_grid):
        # Effacer la grille précédente si elle existe
        if hasattr(self, "sudoku_frame"):
            self.sudoku_frame.destroy()

        # Taille des cases
        cell_size = 35

        # Création du cadre pour la grille de Sudoku
        self.sudoku_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.sudoku_frame.grid(row=1, column=1, padx=20, sticky="nsew")
        
         # Séparation des sous-grilles avec des bordures plus épaisses et transparentes
        for i in range(3):
            for j in range(3):
                frame = ctk.CTkFrame(self.sudoku_frame, border_width=2)
                frame.grid(row=i*3, column=j*3, rowspan=3, columnspan=3, sticky="nsew")

        # Configurer les lignes et colonnes pour les séparations de la grille
        for i in range(9):
            self.sudoku_frame.grid_rowconfigure(i, minsize=cell_size)
            self.sudoku_frame.grid_columnconfigure(i, minsize=cell_size)

        # Création et affichage de la grille de Sudoku
        for i in range(9):
            for j in range(9):
                cell_value = sudoku_grid[i][j]
                if cell_value != " ":
                    label = ctk.CTkLabel(self.sudoku_frame, text=cell_value, font=self.font_style, width=cell_size, height=cell_size, anchor="center")
                    label.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                else:
                    entry = ctk.CTkEntry(self.sudoku_frame, font=self.font_style, width=cell_size, height=cell_size, justify="center")
                    entry.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
    
        self.sudoku_frame.grid_propagate(False)
    
class WelcomeApp:
    def __init__(self, root, username=""):
        self.root = root
        self.root.title("Sudoku - Bienvenue")
        self.root.geometry("1920x1080")
        ctk.set_appearance_mode("light")
        self.font_style = ctk.CTkFont(family="mincho", size=22)

        self.difficulty = tk.StringVar()
        self.difficulty.set("Facile")
        self.username = username

        # Set up de la grille
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=2)

        self.create_widgets()

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.grid(row=1, column=1, pady=20, padx=25, sticky="nsew")

        # Champ input
        self.label = ctk.CTkLabel(self.frame, text="Entrez votre pseudo :", font=self.font_style)
        self.label.grid(row=0, column=1, pady=0, padx=25)

        self.entry = ctk.CTkEntry(self.frame, font=self.font_style, width=300, height=50)
        self.entry.grid(row=1, column=1, padx=25)
        self.entry.insert(0, self.username)

        # Choix de difficulté
        self.difficulty = ctk.StringVar(value="Facile")
        difficulties = ["Facile", "Moyen", "Difficile"]
        for index, difficulty in enumerate(difficulties):
            ctk.CTkRadioButton(self.frame, text=difficulty, variable=self.difficulty, value=difficulty, font=self.font_style).grid(row=2+index, column=1)

        # Bouton pour commencer la partie
        self.button = ctk.CTkButton(
            self.frame, text="Commencer", command=self.start_app, 
            corner_radius=10, font=self.font_style, width=300, height=60, 
            fg_color="red", hover_color="#144d75"
        )
        self.button.grid(row=5, column=1, padx=20)

        # Ajout de l'image
        self.image_frame = ctk.CTkFrame(self.frame)
        self.image_frame.grid(row=6, column=1)

        # Charger l'image
        image = Image.open("assets/insa.png")
        image = image.resize((210, 210), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        # Afficher l'image dans un label
        self.image_label = ctk.CTkLabel(self.image_frame, image=photo, text="")
        self.image_label.image = photo  # Gardez une référence à l'image pour éviter la collecte des déchets
        self.image_label.pack()

        # Centrer les éléments horizontalement
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(5, weight=2)
        self.frame.grid_rowconfigure(6, weight=5)

    def start_app(self):
        username = self.entry.get()
        if username:
            self.root.destroy()
            root = ctk.CTk()
            app = SudokuApp(root, username)
            root.mainloop()
        else:
            self.entry.configure(placeholder_text="Le pseudo est requis", placeholder_text_color="red")

if __name__ == "__main__":
    root = ctk.CTk()
    app = WelcomeApp(root)
    root.mainloop()
