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
    
    def execute(self, joueur):
        for person in self.gameObj.persons:
            if person.playerName == joueur:
                actionsPossibles = ["W"] * 10 + ["G"] * 10 + ["B"] * 3
                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(actionsPossibles)
                    person.actionNames.append(newAction)