from Buildings import Buildings
from Recolte_ressources import Recolte_ressources
from Units import *
from TileMap import TileMap
from constants import *
import numpy as np
from Initialisation_Compteur import Initialisation_Compteur
import random
import threading
import time

class StratEconomique:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit
        self.building = self.gameObj.buildings
        self.start_time = time.time()

    def construire_farm(self):
        wood = compteurs_joueurs[self.joueur]['ressources']['W']

        if wood > 60:
            self.building.build('F')

    def construire_house(self):
        wood = compteurs_joueurs[self.joueur]['ressources']['W']

        for joueur, compteurs in compteurs_joueurs.items():
            if isinstance(compteurs['batiments'], dict):
                max_pop = (compteurs['batiments'].get('T', 0) + compteurs['batiments'].get('H', 0)) * 5

        for joueur, compteurs in compteurs_joueurs.items():
            if isinstance(compteurs['unites'], dict):
                nb_pop = (compteurs['unites'].get('v', 0) + compteurs['unites'].get('a', 0) + compteurs['unites'].get('h', 0) + compteurs['unites'].get('s', 0))

        if wood > 25 and max_pop == nb_pop:
            self.building.build('H')

    def optimiser_collecte_ressources(self, joueur):
        # Exemple de logique d'assignation des villageois
        gold = compteurs_joueurs[self.joueur]['ressources']['G']
        wood = compteurs_joueurs[self.joueur]['ressources']['W']

        if gold < wood:
            proba = np.arange(0, 1.1, 0.1)
            actionPossible = {'G' : 0.7, 'W': 0.9, 'B': 1}
            for person in self.gameObj.persons:
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(proba)
                    if newAction <= actionPossible['G']:
                        person.actionNames.append('G')
                    elif newAction <= actionPossible['W']:
                        person.actionNames.append('W')
                    else:
                        person.actionNames.append('B')
        elif wood <= gold:
            proba = np.arange(0, 1.1, 0.1)
            actionPossible = {'G': 0.2, 'W': 0.9, 'B': 1}
            for person in self.gameObj.persons:
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(proba)
                    if newAction <= actionPossible['G']:
                        person.actionNames.append('G')
                    elif newAction <= actionPossible['W']:
                        person.actionNames.append('W')
                    else:
                        person.actionNames.append('B')


    def execute(self, joueur):
        self.phase_1(joueur)

        if i == 2:
            self.phase_2(joueur)

        """
        if i == 3:
            self.phase_3(joueur)
        """
    def phase_1(self, joueur):
        food = compteurs_joueurs[self.joueur]['ressources']['f']

        timer = threading.Timer(60.0, self.optimiser_collecte_ressources, args=[joueur])
        timer.start()

        while len(self.gameObj.persons) < 14:
            if food >= 50:
                #self.unit.creation_unite('v', self.joueur)
                #self.construire_house()

        self.construire_farm()

        if time.time() - self.start_time >= 300:  # 5 minutes = 300 secondes
            i = 2
            self.start_time = time.time()

    def phase_2(self, joueur):
        timer = threading.Timer(60.0, self.optimiser_collecte_ressources, args=[joueur])
        timer.start()


"""
    def phase_3(self):



        food = compteurs_joueurs[self.joueur]['ressources']['F']




        if food <= 50:
            self.construire_farm()

        self.construire_house()
        self.optimiser_collecte_ressources()
"""
