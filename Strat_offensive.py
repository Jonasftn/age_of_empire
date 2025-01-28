from Buildings import Buildings
import numpy as np
from Units import Units
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur
import random
import threading


class StratOffensive:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.resource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit

    def gestion_des_villageois_debut(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 5
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('H')
            if gold > wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 5 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('K')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_debut, args=(joueur,)).start()
    
    def execute(self, joueur):
        self.gestion_des_villageois_debut(joueur)

