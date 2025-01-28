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
        self.startTime = None
        self.buildingDuration = 1000
        self.isAttaquing = False
        self.distanceCible = None

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
                elapsedTime = min(100, currentTime - self.lastTime)
                self.lastTime = currentTime
                distance = math.sqrt((x - xFinal)**2 + (y - yFinal)**2)
                durationToFinal = 1000.*distance/self.speed  # ms
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
                if actionName in ('T', 'H', 'F', 'B', 'A', 'C', 'S'):
                    self.build(actionName)
                if actionName == 'attaquePerson':
                    self.attackPerson()
                    print ("pop attaquePerson")
        #print("update la position finale est", self.finalPosition, "la position actuelle est", self.position)
        #print("update liste des batiments", self.gameObj.buildingsDict.keys())


    def build(self, buildingType, nearWhat = None):
        if self.startTime == None:
            # Check the ressources
            isEnough = True
            for ressourceName, cost in builds_dict[buildingType]['cout'].items():
                nAvailables = compteurs_joueurs[self.playerName]['ressources'][ressourceName]
                print ('buildingType', buildingType, 'ressourceName', ressourceName, 'cost', cost, 'nAvailables', nAvailables)
                if nAvailables < cost:
                    isEnough = False
                    self.actionNames.pop(0)
                    return

            if isEnough == True:
                for ressourceName, cost in builds_dict[buildingType]['cout'].items():
                    compteurs_joueurs[self.playerName]['ressources'][ressourceName] -= cost

                # We research the closest building
                actualBuildings = self.get_closest_building(self.playerName)
                x_actual = actualBuildings[0]
                y_actual = actualBuildings[1]

                # We find position for new building
                if buildingType == 'C':
                    diameter = 15
                else:
                    diameter = 5
                for i in range (1000):
                    caseX = random.randint(-diameter, diameter)
                    caseY = random.randint(-diameter, diameter)
                    x = x_actual + caseX
                    y = y_actual + caseY
                    # Vérifie si la case est dans le cercle et dans les limites 
                    if 0 <= x <= size and 0 <= y <= size:
                        if (x, y) not in self.gameObj.buildingsDict.keys() and (x, y) not in self.gameObj.ressourcesDict.keys():
                            self.finalPosition = (x, y)
                            self.isFirstCycle = False
                            self.startTime = pygame.time.get_ticks()
                            self.isMoving = True
                            break

        if self.startTime is not None and self.finalPosition == self.position:
            # If building is terminated, show it
            self.buildingDuration = constants.builds_dict[buildingType]['build_time']*1000
            if pygame.time.get_ticks() > self.startTime + self.buildingDuration:
                newBuilding = Building(self.gameObj, buildingType, self.position, self.playerName)
                self.gameObj.buildingsDict[self.position] = newBuilding
                compteurs_joueurs[self.playerName]['batiments'][buildingType] += 1
                if buildingType =='T' or buildingType == 'H':
                    compteurs_joueurs[self.playerName]['ressources']['max_pop'] += 5
                self.startTime = None
                self.actionNames.pop(0)


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



    def attackPerson(self):
        self.distanceCible, self.victim = self.get_closest_person()
        if self.victim != None:
            self.finalPosition = self.victim.position                    
            self.isMoving = True
            if self.distanceCible < 1:
                self.isAttaquing = True
        else :
            self.actionNames.pop(0)
            self.isMoving = False
            self.isAttaquing = False
        if self.isAttaquing:
            currentTime = pygame.time.get_ticks()
            elapsedTime = min(100, currentTime - self.lastTime)
            self.lastTime = currentTime
            victimType = self.victim.entityType
            speed = constants.units_dict[self.entityType]['attaque']
            
            self.victim.healthPoint -= elapsedTime*speed/1000.
            print('victim.healthPoint', self.victim.healthPoint)
            if self.victim.healthPoint <= 0.:
                for iPerson, person in enumerate(self.gameObj.persons):
                    if person.position == self.victim.position:
                        del self.gameObj.persons[iPerson]
                        compteurs_joueurs[self.playerName]['unites'][victimType] -= 1
                        if len(self.actionNames) > 0:
                            self.actionNames.pop(0)
                        #self.isMoving = False
                        self.isAttaquing = False

    def attackBuilding(self):
            self.distanceCible, self.victim = self.get_closest_building_opponent()
            if self.victim != None:
                self.finalPosition = self.victim.position                    
                self.isMoving = True
                if self.distanceCible < 1:
                    self.isAttaquing = True
            else :
                self.actionNames.pop(0)
                self.isMoving = False
                self.isAttaquing = False
            if self.isAttaquing:
                currentTime = pygame.time.get_ticks()
                elapsedTime = min(100, currentTime - self.lastTime)
                self.lastTime = currentTime
                victimType = self.victim.entityType
                speed = constants.units_dict[self.entityType]['attaque']
                keys_to_remove = []
                self.victim.healthPoint -= elapsedTime*speed/1000.
                print('victim.healthPoint', self.victim.healthPoint)
                if self.victim.healthPoint <= 0.:
                    for coordinatesBuilding, building in self.gameObj.buildingsDict.items():
                        if building.position == self.victim.position:
                            keys_to_remove.append(coordinatesBuilding)
                            compteurs_joueurs[self.playerName]['batiments'][victimType] -= 1
                            if len(self.actionNames) > 0:
                                self.actionNames.pop(0)
                            #self.isMoving = False
                            self.isAttaquing = False
                    for key in keys_to_remove:
                        self.gameObj.buildingsDict.pop(key)

    def get_closest_building_opponent(self):
        (x, y) = self.position
        buildingClosest = None
        distanceSquaredMin = 30.*size*size
        for building in self.gameObj.buildingsDict.values():
            if building.playerName != self.playerName:
                xBuilding, yBuilding = building.position
                distanceSquared = (x - xBuilding)**2 + (y - yBuilding)**2
                if distanceSquared < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    buildingClosest = building
        return math.sqrt(distanceSquaredMin), buildingClosest
         
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
            


    def get_closest_person(self):
        (x, y) = self.position
        personClosest = None
        distanceSquaredMin = 30.*size*size
        for person in self.gameObj.persons:
            if person.playerName != self.playerName:
                xPerson, yPerson = person.position
                distanceSquared = (x - xPerson)**2 + (y - yPerson)**2
                if distanceSquared < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    personClosest = person

        return math.sqrt(distanceSquaredMin), personClosest
        
    def get_closest_building(self, playerName):
        (x, y) = self.position
        distanceSquaredMin = 99999
        for (xBuilding, yBuilding), building in self.gameObj.buildingsDict.items():
            if building.playerName == playerName:
                distanceSquared = (x - xBuilding)**2 + (y - yBuilding)**2
                if distanceSquared < distanceSquaredMin:
                    distanceSquaredMin = distanceSquared
                    positionClosest = (xBuilding, yBuilding)
        return positionClosest

class Ressource():
    def __init__(self, gameObj, entityType, position):
        self.gameObj = gameObj
        self.quantity = constants.ressources_dict[entityType]['quantite']
        self.image = constants.ressources_dict[entityType]['image']
        self.position = position
        self.entityType = entityType
        self.is_harvesting = 48

class Building():
    def __init__(self, gameObj, buildingType, position, playerName):
        self.gameObj = gameObj
        self.healthPoint = constants.builds_dict[buildingType]['hp']
        self.image = constants.builds_dict[buildingType]['tile']
        self.position = position
        self.entityType = buildingType
        self.playerName = playerName
        self.startTime = None
        self.trainingDuration = 1000

    def create_person(self):
        if 'children' in constants.builds_dict[self.entityType].keys():
            # Take the money and start the training
            if self.startTime == None:
                self.personType = constants.builds_dict[self.entityType]['children']
                self.trainingDuration = constants.units_dict[self.personType]['temps_entrainement']*1000
                isEnough = True
                for ressourceName, cost in units_dict[self.personType]['cout'].items():
                    nAvailables = compteurs_joueurs[self.playerName]['ressources'][ressourceName]
                    if nAvailables < cost:
                        return

                for ressourceName, cost in units_dict[self.personType]['cout'].items():
                    compteurs_joueurs[self.playerName]['ressources'][ressourceName] -= cost
                self.startTime = pygame.time.get_ticks()

            # Training is done, create the person
            else:
                if pygame.time.get_ticks() > self.startTime + self.trainingDuration:
                    newPerson = Person(self.gameObj, self.personType, self.position, self.playerName)
                    self.gameObj.persons.append(newPerson)
                    compteurs_joueurs[self.playerName]['unites'][self.personType] += 1
                    self.startTime = None
            


    
