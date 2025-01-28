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

    def gestion_des_villageois_construction_house_and_camp(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        actionsPossiblesBuild = ["H"] * 7 + ["C"] * 3
                        Action = random.choice(actionsPossiblesBuild)
                        person.actionNames.append(Action)
            if gold >= wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        actionsPossiblesBuild = ["H"] * 7 + ["C"] * 3
                        Action = random.choice(actionsPossiblesBuild)
                        person.actionNames.append(Action)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_house_and_camp, args=(joueur,)).start()

    def gestion_des_villageois_construction_house(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('H')
            if gold >= wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('H')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_house, args=(joueur,)).start()

    def gestion_des_villageois_construction_farm(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('F')
            if gold > wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('F')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_farm, args=(joueur,)).start()

    def gestion_des_villageois_construction_keep(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('K')
            if gold > wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('K')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_keep, args=(joueur,)).start()

    def gestion_des_villageois_construction_barracks(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('B')
            if gold >= wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('B')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_barracks, args=(joueur,)).start()

    def gestion_des_villageois_construction_stable(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('S')
            if gold >= wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('S')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_stable, args=(joueur,)).start()

    def gestion_des_villageois_construction_archery_range(self, joueur):
        try:
            villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur]
            nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
            villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
            reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
            gold = compteurs_joueurs[joueur]['ressources']['G']
            wood = compteurs_joueurs[joueur]['ressources']['W']

            if gold < wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 3 + ["G"] * 7
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('A')
            if gold >= wood:
                for person in villageois_a_traiter:
                    actionsPossibles = ["W"] * 7 + ["G"] * 3
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        newAction = random.choice(actionsPossibles)
                        person.actionNames.append(newAction)
                for person in reste_des_villageois:
                    if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                        person.actionNames.append('A')
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        finally:
            threading.Timer(60, self.gestion_des_villageois_construction_archery_range, args=(joueur,)).start()
    
    def execute(self, joueur):
        if compteurs_joueurs[joueur]['batiments']['H'] < 3 and compteurs_joueurs[joueur]['batiments']['C'] < 2:
            self.gestion_des_villageois_construction_house_and_camp(joueur)
        elif compteurs_joueurs[joueur]['batiments']['F'] < 3:
            self.gestion_des_villageois_construction_farm(joueur)
        elif compteurs_joueurs[joueur]['batiments']['B'] < 1:
            self.gestion_des_villageois_construction_barracks(joueur)
        elif compteurs_joueurs[joueur]['batiments']['S'] < 1:
            self.gestion_des_villageois_construction_stable(joueur)
        elif compteurs_joueurs[joueur]['batiments']['A'] < 1:
            self.gestion_des_villageois_construction_archery_range(joueur)
        elif 3 < compteurs_joueurs[joueur]['batiments']['H'] < 15:
            self.gestion_des_villageois_construction_house(joueur)

