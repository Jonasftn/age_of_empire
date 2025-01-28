from Buildings import Buildings
import numpy as np
from Units import Units
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur
import random


class StratOffensive:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.resource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit

    def gestion_des_villageois_construction_house_and_camp(self, joueur):
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
                    print("on est dans la première méthode")
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
                    print("on est dans la première méthode")

    def gestion_des_villageois_construction_house(self, joueur):
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

    def gestion_des_villageois_construction_farm(self, joueur):
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
                    print("on est dans la deuxième méthode")
        if gold > wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 7 + ["G"] * 3
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(actionsPossibles)
                    person.actionNames.append(newAction)
            for person in reste_des_villageois:
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    person.actionNames.append('F')
                    print("on est dans la deuxieme méthode")

    def gestion_des_villageois_construction_keep(self, joueur):
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

    def gestion_des_villageois_construction_barracks(self, joueur):
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
                    print("on est dans la troisième méthode")
        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 7 + ["G"] * 3
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(actionsPossibles)
                    person.actionNames.append(newAction)
            for person in reste_des_villageois:
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    person.actionNames.append('B')
                    print("on est dans la troisième méthode")

    def gestion_des_villageois_construction_stable(self, joueur):
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

    def gestion_des_villageois_construction_archery_range(self, joueur):
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
    
    def execute(self, joueur):
        if compteurs_joueurs[joueur]['batiments']['H'] < 3 and compteurs_joueurs[joueur]['batiments']['C'] < 1:
            self.gestion_des_villageois_construction_house_and_camp(joueur)
        elif compteurs_joueurs[joueur]['batiments']['F'] < 2:
            self.gestion_des_villageois_construction_farm(joueur)
        elif compteurs_joueurs[joueur]['batiments']['B'] < 1:
            self.gestion_des_villageois_construction_barracks(joueur)
        elif compteurs_joueurs[joueur]['batiments']['S'] < 1:
            self.gestion_des_villageois_construction_stable(joueur)
        elif compteurs_joueurs[joueur]['batiments']['A'] < 1:
            self.gestion_des_villageois_construction_archery_range(joueur)
        elif 3 < compteurs_joueurs[joueur]['batiments']['H'] < 10:
            self.gestion_des_villageois_construction_house(joueur)

