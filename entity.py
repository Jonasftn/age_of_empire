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


class Person():
    
    def __init__(self, gameObj, entityType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.units_dict[entityType]['hp']
        self.image = constants.units_dict[entityType]['image']
        self.position = position
        self.finalPosition = position
        self.entityType = entityType
        self.playerName = playerName
        self.speed = constants.units_dict[entityType]['vitesse']
        self.actionNames = []
        self.quantity = 0
        self.isMoving = False
        self.lastTime = pygame.time.get_ticks()
        self.epsilon = 0.001
        self.gameObj = gameObj

    def update(self):
        if self.playerName == 'joueur_2':
            print ('update', self.playerName, 'moving', self.isMoving, '(x, y)', self.position, '(xFinal, yFinal)', self.finalPosition, 'actions', len(self.actionNames))

        # Motion
        if self.isMoving and self.finalPosition is not None:
            (x, y) = self.position
            (xFinal, yFinal) = self.finalPosition
            
            if abs(x - xFinal) < self.epsilon and abs(y - yFinal) < self.epsilon:
                self.position = self.finalPosition
                self.isMoving = False
                
            else:
                currentTime = pygame.time.get_ticks()
                elapsedTime = min(100, currentTime - self.lastTime)
                self.lastTime = currentTime
                distance = math.sqrt((x - xFinal)**2 + (y - yFinal)**2)
                durationToFinal = 1000.*distance/self.speed
                stepDuration = min(elapsedTime, durationToFinal)
                x = x + (xFinal - x)*stepDuration/durationToFinal
                y = y + (yFinal - y)*stepDuration/durationToFinal
                self.position = (x, y)

        # Actions
        else:
            
            if len(self.actionNames) > 0:
                actionName = self.actionNames[0]
                print ('actionName', actionName)

                if actionName in ('W', 'G'):
                    self.collect(actionName)
                    self.actionNames.pop(0)

                if actionName == 'B':
                    self.build(self)
                    self.actionNames.pop(0)


    def build(self, nearWhat = None):
        # We research the closest building
        actualBuildings = self.get_closest_building(self.playerName)

        #We find position for new building
        radius = 20
        x_center, y_center = actualBuildings
        for caseX in range(-radius, radius + 1):
            for caseY in range(-radius, radius + 1):
                x = x_center + caseX
                y = y_center + caseY
                # Vérifie si la case est dans le cercle et dans les limites [0, 120]
                if 0 <= x <= 120 and 0 <= y <= 120:
                    if (x, y) not in self.gameObj.buildingsDict.keys() and (x, y) not in self.gameObj.ressourcesDict.keys():
                        self.finalPosition = (x, y)
                        break
        self.isMoving = True

        # We are on the position, we build
        if self.position == self.finalPosition:
            building = Building(self.gameObj, 'S', self.position, self.playerName)
            self.gameObj.buildingsDict[self.position] = building


                
    def collect(self, ressourceName):
        # We go to the closest ressource
        self.finalPosition = self.get_closest_ressource(ressourceName)
        self.isMoving = True

        # We are on the ressource, we pickup
        if self.position in self.gameObj.ressourcesDict:
            ressource = self.gameObj.ressourcesDict[self.position]
            if ressource.quantity > 0:
                # Get collection speed from constants (convert from per minute to per second)
                collection_rate = constants.units_dict[self.entityType]['collection_speed'] / 60.0
                current_time = pygame.time.get_ticks()
                
                if not hasattr(self, 'last_collection_time'):
                    self.last_collection_time = current_time
                
                # Calculate time passed and amount to collect
                time_passed = (current_time - self.last_collection_time) / 1000.0  # Convert to seconds
                amount_to_collect = min(
                    collection_rate * time_passed,  # Amount per second * seconds passed
                    ressource.quantity,            # Available resource
                    20 - self.quantity            # Remaining capacity
                )
                
                # Round to nearest integer
                amount_to_collect = int(amount_to_collect)
                
                # Update collection (accumulate instead of replace)
                if amount_to_collect > 0:
                    self.quantity += amount_to_collect
                    ressource.quantity -= amount_to_collect
                    self.last_collection_time = current_time

                # Check if resource is depleted
                if ressource.quantity <= 0:
                    del self.gameObj.ressourcesDict[self.position]

            # We go to our closest building
            self.finalPosition = self.get_closest_building(self.playerName)
            self.isMoving = True

        # We are in our building, we store the ressource and remove the action
        elif self.position in self.gameObj.buildingsDict and self.quantity > 0:
            building = self.gameObj.buildingsDict[self.position]
            if building.playerName == self.playerName:
                compteurs_joueurs[self.playerName]['ressources'][ressourceName] += self.quantity
                self.quantity = 0

        # We search another ressource
        else :
            self.finalPosition = self.get_closest_ressource(ressourceName)
            self.isMoving = True
            
    def get_closest_ressource(self, ressourceName):
        (x, y) = self.position
        print ("je suis en ", self.position)
        distanceSquaredMin = 9999999
        positionClosest = None
        for (xRessource, yRessource), ressource in self.gameObj.ressourcesDict.items():
            print ("est ce que cette valeur marche?", (xRessource, yRessource), ressource.entityType)
            if ressource.entityType == ressourceName:
                distanceSquared = (x - xRessource)**2 + (y - yRessource)**2
                print ('distanceSquared', distanceSquared)
                if distanceSquared < distanceSquaredMin:
                    print ("je suis la nouvelle distance min", distanceSquared)
                    print ('xRessource', xRessource, 'yRessource', yRessource)
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xRessource, yRessource)
        print ('positionClosest', positionClosest)
        for ressource in self.gameObj.ressourcesDict.values():
            if ressource.position == positionClosest:
                print ('ressource', ressource.entityType, ressource.position)
                return positionClosest


    def get_closest_building(self, playerName):
        (x, y) = self.position
        distanceSquaredMin = 99999
        for (xBuilding, yBuilding), building in self.gameObj.buildingsDict.items():
            if building.playerName == playerName:
                distanceSquared = (x - xBuilding)**2 + (y - yBuilding)**2
                if distanceSquared < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xBuilding, yBuilding)
        print ('positionClosest', positionClosest)
        return positionClosest

class Ressource():
    def __init__(self, gameObj, entityType, position):
        self.gameObj = gameObj
        self.quantity = constants.ressources_dict[entityType]['quantite']
        self.image = constants.ressources_dict[entityType]['image']
        self.position = position
        self.entityType = entityType

class Building():
    def __init__(self, gameObj, entityType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.builds_dict[entityType]['hp']
        self.image = constants.builds_dict[entityType]['tile']
        self.position = position
        self.entityType = entityType
        self.playerName = playerName