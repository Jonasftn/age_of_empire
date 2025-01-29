from Buildings import Buildings
import numpy as np
from Units import Units
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur
import random


class Strat_eco:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.resource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit


    def gestion_des_villageois_construction_house(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('H')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('H')

    def gestion_des_villageois_construction_camp(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('C')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('C')

    def gestion_des_villageois_construction_farm(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 3 / 4)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('F')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('F')

    def gestion_des_villageois_construction_keep(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 9 / 10)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('K')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('K')

    def gestion_des_villageois_construction_barracks(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 9 / 10)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('B')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('B')

    def gestion_des_villageois_construction_stable(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 9 / 10)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('S')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('S')

    def gestion_des_villageois_construction_archery_range(self, joueur):
        villageois_du_joueur = [person for person in self.gameObj.persons if person.playerName == joueur and len(
            person.actionNames) == 0 and person.entityType == 'v']
        nb_a_traiter = int(len(villageois_du_joueur) * 9 / 10)
        villageois_a_traiter = villageois_du_joueur[:nb_a_traiter]
        reste_des_villageois = villageois_du_joueur[nb_a_traiter:]
        gold = compteurs_joueurs[joueur]['ressources']['G']
        wood = compteurs_joueurs[joueur]['ressources']['W']

        if gold < wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 4 + ["G"] * 6
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('A')

        if gold >= wood:
            for person in villageois_a_traiter:
                actionsPossibles = ["W"] * 6 + ["G"] * 4
                newAction = random.choice(actionsPossibles)
                person.actionNames.append(newAction)
            for person in reste_des_villageois:
                person.actionNames.append('A')

    def create_villageois(self, joueur):
        for building in self.gameObj.buildingsDict.values():
            if building.entityType == 'T':
                food = compteurs_joueurs[joueur]['ressources']['f']
                if food >= 50:
                    building.create_person()
                    print("un villageois est en cours d'entrainement")

    def create_epeiste(self, joueur):
        for building in self.gameObj.buildingsDict.values():
            if building.entityType == 'B':
                food = compteurs_joueurs[joueur]['ressources']['f']
                gold = compteurs_joueurs[joueur]['ressources']['G']
                if food >= 50 and gold >= 20:
                    building.create_person()
                    print("un swordsmen est en cours d'entrainement")

    def create_archer(self, joueur):
        for building in self.gameObj.buildingsDict.values():
            if building.entityType == 'A':
                wood = compteurs_joueurs[joueur]['ressources']['W']
                gold = compteurs_joueurs[joueur]['ressources']['G']
                if wood >= 25 and gold >= 45:
                    building.create_person()
                    print("un archer est en cours d'entrainement")

    def create_cavalier(self, joueur):
        for building in self.gameObj.buildingsDict.values():
            if building.entityType == 'S':
                food = compteurs_joueurs[joueur]['ressources']['f']
                gold = compteurs_joueurs[joueur]['ressources']['G']
                if food >= 80 and gold >= 20:
                    building.create_person()
                    print("un horsemen est en cours d'entrainement")

    def attack_ennemies(self):
        for person in self.gameObj.persons:
            if person is 's' or 'a' or 'c':
                person.attackPerson() or person.attackBuilding()
                print("attaque l'ennemie")

    def execute(self, joueur):
        if compteurs_joueurs[joueur]['batiments']['H'] < 2:
            self.gestion_des_villageois_construction_house(joueur)
        elif compteurs_joueurs[joueur]['unites']['v'] < 4:
            self.create_villageois(joueur)
        elif compteurs_joueurs[joueur]['batiments']['C'] < 1:
            self.gestion_des_villageois_construction_camp(joueur)
        elif compteurs_joueurs[joueur]['batiments']['F'] < 2:
            self.gestion_des_villageois_construction_farm(joueur)
        elif compteurs_joueurs[joueur]['unites']['v'] < 10:
            self.create_villageois(joueur)
        elif 2 < compteurs_joueurs[joueur]['batiments']['H'] < 5:
            self.gestion_des_villageois_construction_house(joueur)
        elif compteurs_joueurs[joueur]['batiments']['B'] < 1:
            self.gestion_des_villageois_construction_barracks(joueur)
        elif compteurs_joueurs[joueur]['unites']['s'] < 5:
            self.create_epeiste(joueur)
        elif compteurs_joueurs[joueur]['batiments']['S'] < 1:
            self.gestion_des_villageois_construction_stable(joueur)
        elif compteurs_joueurs[joueur]['unites']['h'] < 5:
            self.create_cavalier(joueur)
        elif compteurs_joueurs[joueur]['batiments']['A'] < 1:
            self.gestion_des_villageois_construction_archery_range(joueur)
        elif compteurs_joueurs[joueur]['unites']['a'] < 5:
            self.create_archer(joueur)
        elif 3 < compteurs_joueurs[joueur]['batiments']['H'] < 10:
            self.gestion_des_villageois_construction_house(joueur)
        elif (compteurs_joueurs[joueur]['unites']['v'] + compteurs_joueurs[joueur]['unites']['a'] + compteurs_joueurs[joueur]['unites']['s'] + compteurs_joueurs[joueur]['unites']['h']) < 55:
            for i in range(15):
                self.create_epeiste(joueur)
            for i in range(15):
                self.create_archer(joueur)
            for i in range(15):
                self.create_cavalier(joueur)
            self.attack_ennemies()
        else:
            self.attack_ennemies()

