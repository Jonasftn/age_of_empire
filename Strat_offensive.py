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

    def getStatus(self, position, joueur, type_unit, id):
        return (self.gameObj.tuiles[position]['unites'][joueur][type_unit][id]['Status'] == 'libre')

    def find_closest_enemy(self, position, joueur):
        """Find closest enemy unit"""
        closest_enemy = None
        min_distance = float('inf')
        
        for pos, data in self.gameObj.tuiles.items():
            if 'unites' in data:
                for enemy_player, units in data['unites'].items():
                    if enemy_player != joueur:  # If it's an enemy
                        distance = abs(position[0] - pos[0]) + abs(position[1] - pos[1])
                        if distance < min_distance:
                            min_distance = distance
                            # Store enemy info
                            for unit_type, unit_dict in units.items():
                                for unit_id in unit_dict:
                                    closest_enemy = {
                                        'position': pos,
                                        'player': enemy_player,
                                        'type': unit_type,
                                        'id': unit_id
                                    }
        return closest_enemy

    def bouge(self, joueur, type_unit, id_unite, pos_bois):
        self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois)
        self.unit.update_position()
        
        """action_a_executer.append(
            lambda posress=pos_bois: self.resource_collector.recolter_ressource_plus_proche_via_trouver(joueur, type_unit, id_unite, posress=posress))
        def action_apres_deplacement():
            if int(self.gameObj.tuiles[self.unit.position]['unites'][joueur][type_unit][id_unite]['capacite']) == 20:
                pos_batiment = self.resource_collector.trouver_plus_proche_batiment(joueur, type_unit, id_unite)
                if pos_batiment:
                    self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_batiment)

        action_a_executer.append(action_apres_deplacement)"""

        def deposer_ressources_in_batiment():
                quantite = 20
                ressource = 'f'
                self.resource_collector.deposer_ressources(quantite, joueur, type_unit, id_unite, ressource)

        action_a_executer.append(deposer_ressources_in_batiment)
    
    def execute(self, joueur):
        for person in self.gameObj.persons:
            if person.playerName == joueur and len(person.actionNames) == 0:
                # Find closest enemy
                closest_enemy = self.find_closest_enemy(person.position, joueur)
                
                if closest_enemy:
                    # Attack enemy
                    self.unit.attack(
                        joueur_a=person.playerName,
                        type_a=person.entityType,
                        id_a=person.id,
                        joueur_b=closest_enemy['player'],
                        type_b=closest_enemy['type'],
                        id_b=closest_enemy['id']
                    )
                    person.actionNames.append('A')  # 'A' for attack

            if person.playerName == joueur:
                print ('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh')
                proba = np.arange(0, 1.1, 0.1)
                actionPossible = {'G' : 0.5, 'W': 0.9, 'B': 1}
                print ('execute', joueur, 'person.playerName', person.playerName, 'len(actions', len(person.actionNames), 'type', person.entityType, 'position', person.position)

                if person.playerName == joueur and len(person.actionNames) == 0 and person.entityType == 'v':
                    newAction = random.choice(proba)
                    if newAction <= actionPossible['G']:
                        person.actionNames.append('G')
                    elif newAction <= actionPossible['W']:
                        person.actionNames.append('W')
                    else:
                        person.actionNames.append('B')