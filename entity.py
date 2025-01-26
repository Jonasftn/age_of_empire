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
    def __init__(self, entityType, position):

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
        self.position = position
        self.entityType = entityType
        


    def set_final_position(x, y):
        self.positionFinal = (x, y) 

    def is_moving():
        return self.positionFinal != self.position 

class Person(Entity):
    def __init__(self, entityType, position):
        self.healthPoint = constants.units_dict[entityType]['hp']
        self.image = constants.units_dict[entityType]['image']
        self.position = position
        self.entityType = entityType

class Ressource(Entity):
    def __init__(self, entityType, position):
        self.quantity = constants.ressources_dict[entityType]['quantite']
        self.image = constants.ressources_dict[entityType]['image']
        self.position = position
        self.entityType = entityType

class Building(Entity):
    def __init__(self, entityType, position):
        self.healthPoint = constants.builds_dict[entityType]['hp']
        self.image = constants.builds_dict[entityType]['image']
        self.position = position
        self.entityType = entityType
        


    
