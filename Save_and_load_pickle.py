import pickle
import os
from tkinter import filedialog
import tkinter as tk
from datetime import datetime

class Save_and_load:
    def __init__(self):
        self.save_folder = "saves"
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def sauvegarder_jeu(self, game_state):
        """
        Sauvegarde l'état complet du jeu dans un fichier pickle.
        
        Args:
            game_state: Dictionnaire contenant tous les états du jeu à sauvegarder
                - tuiles: Dict des tuiles du jeu
                - compteurs: Dict des compteurs des joueurs
                - ressources: Dict des ressources
                - units: Dict des unités
                - builds: Dict des bâtiments
                - compteurs_unites: Dict des compteurs d'unités
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_{timestamp}.pkl"
        filepath = os.path.join(self.save_folder, filename)
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(game_state, f)
            print(f"Jeu sauvegardé avec succès dans {filepath}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    def charger_jeu(self, filepath):
        """
        Charge l'état complet du jeu depuis un fichier pickle.
        
        Args:
            filepath: Chemin vers le fichier de sauvegarde
        
        Returns:
            dict: Dictionnaire contenant tous les états du jeu, None si erreur
        """
        try:
            with open(filepath, 'rb') as f:
                game_state = pickle.load(f)
                return game_state
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return None

    def choisir_fichier_sauvegarde(self):
        """
        Ouvre une boîte de dialogue pour choisir un fichier de sauvegarde.
        
        Returns:
            str: Chemin vers le fichier sélectionné ou None si annulé
        """
        root = tk.Tk()
        root.withdraw()

        filepath = filedialog.askopenfilename(
            initialdir=self.save_folder,
            title="Choisir une sauvegarde",
            filetypes=(("Fichiers pickle", "*.pkl"), ("Tous les fichiers", "*.*"))
        )

        root.destroy()
        return filepath if filepath else None