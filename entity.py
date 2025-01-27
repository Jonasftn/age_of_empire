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
        self.cost = constants.units_dict[entityType]['cout']
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
        self.isFirstCycle = True

    def update(self):
        #if self.playerName == 'joueur_2':
            #print ('update', self.playerName, 'moving', self.isMoving, '(x, y)', self.position, '(xFinal, yFinal)', self.finalPosition, 'actions', len(self.actionNames))


        # Motion
        if self.isMoving:

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
                #print ('actionName', actionName)

                if actionName in ('W', 'G'):
                    self.collect(actionName)
                    self.actionNames.pop(0)
                    print ("pop collect")

                if actionName == 'B':
                    self.build(self)



                if actionName == 'createS':
                    self.create("S")
                    self.actionNames.pop(0)
        #print("update la position finale est", self.finalPosition, "la position actuelle est", self.position)
        #print("update liste des batiments", self.gameObj.buildingsDict.keys())


    def build(self, nearWhat = None):
 
        


        # We are on the position, we build
        if self.isFirstCycle == True:
    
            # We research the closest building
            actualBuildings = self.get_closest_building(self.playerName)
            x_actual = actualBuildings[0]
            y_actual = actualBuildings[1]
            #We find position for new building
            diameter = 20
            
            for i in range (1000):
                caseX = random.randint(-diameter, diameter)
                caseY = random.randint(-diameter, diameter)
                x = x_actual + caseX
                y = y_actual + caseY
                # Vérifie si la case est dans le cercle et dans les limites [0, 120]
                if 0 <= x <= size and 0 <= y <= size:
                    if (x, y) not in self.gameObj.buildingsDict.keys() and (x, y) not in self.gameObj.ressourcesDict.keys():
                        self.finalPosition = (x, y)
                        self.isFirstCycle = False
                        self.isMoving = True

                        break

        if self.isFirstCycle == False and self.finalPosition == self.position:

            print ("position creation building", self.position)
            building = Building(self.gameObj, 'S', self.position, self.playerName)
            self.gameObj.buildingsDict[self.position] = building
            self.actionNames.pop(0)
            self.isFirstCycle = True
            print ("pop build")



    def create(self, buildingType):
        for building in self.gameObj.buildingsDict.values():
            if building.entityType == buildingType:


                if 'children' in constants.builds_dict[buildingType].keys():
                    self.gameObj.persons.append(Person(self.gameObj, constants.builds_dict[buildingType]['children'], building.position, self.playerName))
                    for differentRessource, cost in self.cost:
                        compteurs_joueurs[self.playerName]['ressources'][differentRessource] -= cost
                
    def collect(self, ressourceName):
        # We go to the closest ressource
        self.finalPosition = self.get_closest_ressource(ressourceName)
        self.isMoving = True

        # We are on the ressource, we pickup
        if self.position in self.gameObj.ressourcesDict:
            ressource = self.gameObj.ressourcesDict[self.position]
            if ressource.quantity > 0:
                self.quantity = min(ressource.quantity, 20)
                ressource.quantity = max(0, ressource.quantity - 20)
                if ressource.quantity == 0: # We remove the ressource
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
        distanceSquaredMin = 9999999
        positionClosest = None
        for (xRessource, yRessource), ressource in self.gameObj.ressourcesDict.items():
            if ressource.entityType == ressourceName:
                distanceSquared = (x - xRessource)**2 + (y - yRessource)**2
                if distanceSquared < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xRessource, yRessource)
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
    def __init__(self, gameObj, buildingType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.builds_dict[buildingType]['hp']
        self.image = constants.builds_dict[buildingType]['tile']
        self.position = position
        self.entityType = buildingType
        self.playerName = playerName


    def create(self):

        if 'children' in constants.builds_dict[self.entityType].keys():
            childrenType = constants.builds_dict[self.entityType]['children']
            self.gameObj.persons.append(Person(self.gameObj, childrenType, self.position, self.playerName))
            for differentRessource, cost in units_dict[childrenType]['cout'].items():
                compteurs_joueurs[self.playerName]['ressources'][differentRessource] -= cost


    
