import grille_frontend as gridf
import customtkinter as ctk

# ----------- /!\ ----------- #
# Pensez à installer les modules
# présents dans requirements.txt
# pip install -r requirements.txt
# ----------- /!\ ----------- #
def main():
    # Code principal
    root = ctk.CTk()
    app = gridf.WelcomeApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    
