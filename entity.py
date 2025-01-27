from math import sqrt
import math
import pygame

from TileMap import *
import constants
from Coordinates import *


import random
import time
from Global_image_load import *
from numpy.random import poisson
import constants

class Entity:
    def __init__(self, gameObj):


        """
        self.tile_grass = tile_grass
        self.map_data = map_data  # Dictionnaire global à modifier
        self.compteurs_joueurs = compteurs_joueurs
        self.unit_list = None
        self.current_unit_index = 0

        self.coordinates = Coordinates()
        self.id = None  # Identifiant unique pour l'unité

        self.position = None
        self.target_position = None
        self.moving = False
        self.deplacement_termine = False
        self.move_start_time = 0
        self.move_duration = 0
        self.frame_index = 0
        self.direction_index = 0
        self.last_time = pygame.time.get_ticks()
        self.destination = None
        self.moving_unit=None

        self.start_time_offset = 0
        self.attacks_in_progress = []
        
        """
        self.isMoving = False
        self.epsilon = 0.001
        self.lastTime = pygame.time.get_ticks()
        self.gameObj = gameObj

    def update(self):

        # Motion
        if self.isMoving:

            (x, y) = self.position
            (xFinal, yFinal) = self.finalPosition
            
            if abs(x - xFinal) < self.epsilon and abs(y - yFinal) < self.epsilon:
                self.position = self.finalPosition
                self.isMoving = False
                
            else:
                currentTime = pygame.time.get_ticks()
                elapsedTime = currentTime - self.lastTime
                self.lastTime = currentTime
                distance = math.sqrt((x - xFinal)**2 + (y - yFinal)**2)
                durationToFinal = 1000.*distance/self.speed
                stepDuration = min(elapsedTime, durationToFinal)
                x = x + (x - xFinal)*stepDuration/durationToFinal
                y = y + (y - yFinal)*stepDuration/durationToFinal
                self.position = (x, y)

        # Actions
        else:
            
            if len(self.actionNames) > 0:
                actionName = self.actionNames[0]

                if actionName in ('W', 'G'):
                    self.collect(actionName)

                
    def collect(self, ressourceName):

        # We are on the ressource, we pickup
        if self.position in self.gameObj.ressourcesDict:
            ressource = self.gameObj.ressourcesDict[self.position]
            if ressource.quantity > 0:
                self.quantity = min(ressource.quantity, 20)
                ressource.quantity = max(0, ressource.quantity - 20)

            # We go to our closest building
            self.finalPosition = self.get_closest_building(self.playerName)
            self.isMoving = True

        # We are in our building, we store the ressource and remove the action
        elif self.position in self.gameObj.buildingsDict and self.quantity > 0:
            building = self.gameObj.buildingsDict[self.position]
            if building.playerName == self.playerName:
                compteurs_joueurs[self.playerName]['ressources'][ressourceName] += self.quantity
                self.quantity = 0
                self.actionNames.pop(0)

        # We search another ressource
        else :
            self.finalPosition = self.get_closest_ressource(ressourceName)
            self.isMoving = True
            
    def get_closest_ressource(self, ressourceName):
        (x, y) = self.position
        distanceSquaredMin = 99999
        for (xRessource, yRessource), ressource in self.gameObj.ressourcesDict:
            if ressource.entityType == ressourceName:
                distanceSquared = (x - xRessource)**2 + (y - yRessource)**2
                if distanceSquaredMin < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xRessource, yRessource)
        return positionClosest

    def get_closest_building(self, playerName):
        (x, y) = self.position
        distanceSquaredMin = 99999
        for (xBuilding, yBuilding), building in self.gameObj.buildingsDict:
            if building.playerName == playerName:
                distanceSquared = (x - xBuilding)**2 + (y - yBuilding)**2
                if distanceSquaredMin < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xBuilding, yBuilding)
        return positionClosest

class Person(Entity):
    def __init__(self, gameObj, entityType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.units_dict[entityType]['hp']
        self.image = constants.units_dict[entityType]['image']
        self.position = position
        self.entityType = entityType
        self.playerName = playerName
        self.speed = constants.units_dict[entityType]['vitesse']
        self.actionNames = []
        self.quantity = 0

class Ressource(Entity):
    def __init__(self, gameObj, entityType, position):
        self.gameObj = gameObj
        self.quantity = constants.ressources_dict[entityType]['quantite']
        self.image = constants.ressources_dict[entityType]['image']
        self.position = position
        self.entityType = entityType

class Building(Entity):
    def __init__(self, gameObj, entityType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.builds_dict[entityType]['hp']
        self.image = constants.builds_dict[entityType]['image']
        self.position = position
        self.entityType = entityType
        self.playerName = playerName
        
        


    
