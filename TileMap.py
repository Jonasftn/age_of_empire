import pygame
import random
from constants import *
import keyboard
import curses
import pygame
import threading
import time
import numpy as np
from entity import Ressource


mapToDisplay =  [[('G', None) for i in range(size)] for j in range(size)]


class TileMap:
    """Classe gérant la carte des tuiles."""

    def __init__(self, gameObj):
        # self.add_wood_patches()
        self.gameObj = gameObj
        self.position_initiale = (size // 2, size // 2)


        """for position, data in self.tuiles.items():
            unites = data.get('unites', {})
            for joueur, types in unites.items():
                if 'v' in types:
                    for id, details in types['v'].items():
                        person = Person('V', position)
                        self.tabPersons.append(person)
        


        for position in self.tuiles:
            batiments = self.tuiles[position].get('batiments', {})
            for joueur, types_batiments in batiments.items():
                if 'T' in types_batiments:
                    building = Building('T', position)
                    self.tabBuildings.append(building)

        
        for position, data in self.tuiles.items():
            ressources = data.get('ressources')
            if ressources in ('W', 'G'):
                res = Ressource(ressources, position)
                self.tabRessources.append(res)
        print (self.tabRessources)"""
        

    def mode(self, mode):
        if mode == "patches":
            self.add_gold_patches()
        elif mode == "middle":
            self.add_gold_middle()

    def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
        # print("wood")
        num_patches = random.randint(20, 30)
        min_patch_size = 7
        max_patch_size = 15

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)
            wood_tiles = [(start_x, start_y)]
            if (start_x, start_y) not in self.gameObj.tuiles:
                ressource = Ressource(self.gameObj, 'W', (start_x, start_y))
                self.gameObj.ressourcesDict[start_x, start_y] = ressource
                #self.gameObj.tuiles[(start_x, start_y)] = {'ressources': "W", 'quantite': ressources_dict['W']['quantite']}

            while len(wood_tiles) < patch_size:
                tile_x, tile_y = random.choice(wood_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Choisir une direction
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if (new_x, new_y) not in self.gameObj.tuiles:
                        ressource = Ressource(self.gameObj,'W', (new_x, new_y))
                        self.gameObj.ressourcesDict[new_x, new_y] = ressource
                        #self.gameObj.tuiles[(new_x, new_y)] = {'ressources': "W", 'quantite': ressources_dict['W']['quantite']}
                        wood_tiles.append((new_x, new_y))

    def add_gold_patches(self):
        """Ajoute des paquets d'or (G) sur la carte."""
        num_patches = random.randint(10, 15)  # Nombre de paquets d'or à générer
        min_patch_size = 2  # Taille minimale d'un paquet
        max_patch_size = 5  # Taille maximale d'un paquet

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)

            gold_tiles = [(start_x, start_y)]
            if (start_x, start_y) not in self.gameObj.tuiles:
                ressource = Ressource(self.gameObj, 'G', (start_x, start_y))
                self.gameObj.ressourcesDict[start_x, start_y] = ressource
                #self.gameObj.tuiles[(start_x, start_y)] = {'ressources': "G", 'quantite': ressources_dict['G']['quantite']}

            while len(gold_tiles) < patch_size:
                tile_x, tile_y = random.choice(gold_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # (dx, dy)
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if (new_x, new_y) not in self.gameObj.tuiles:
                        ressource = Ressource(self.gameObj, 'G', (new_x, new_y))
                        self.gameObj.ressourcesDict[new_x, new_y] = ressource
                        #self.gameObj.tuiles[(new_x, new_y)] = {'ressources': "G", 'quantite': ressources_dict['G']['quantite']}
                        gold_tiles.append((new_x, new_y))

    def add_gold_middle(self):
        """Ajoute un paquet d'or (G) au centre de la carte."""
        center_x = size // 2
        center_y = size // 2
        patch_size=25
        # Placer un paquet d'or autour du centre
        gold_tiles = []
        while len(gold_tiles) < patch_size:    
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    new_x = center_x + dx
                    new_y = center_y + dy
                
                    if 0 <= new_x < size and 0 <= new_y < size:
                        if (new_x, new_y) not in self.gameObj.tuiles:
                            ressource = Ressource(self.gameObj, 'G', (new_x, new_y))
                            self.gameObj.ressourcesDict[new_x, new_y] = ressource
                            #self.gameObj.tuiles[(new_x, new_y)] = {'ressources': "G", 'quantite': ressources_dict['G']['quantite']}
                            gold_tiles.append((new_x, new_y))

    def apply_color_filter(self, surface, color):
        """
        Applique un filtre de couleur sur une surface pygame.Surface.
        :param surface: Une surface valide.
        :param color: Tuple (R, G, B) représentant la couleur du filtre.
        :return: Une nouvelle surface avec le filtre appliqué.
        """
        if not isinstance(surface, pygame.Surface):
            raise TypeError("L'objet fourni n'est pas une surface pygame.Surface valide.")

        # Copier la surface d'origine
        image_with_filter = surface.copy()

        # Créer une surface de filtre avec la couleur souhaitée
        color_filter = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        color_filter.fill(color)  # Ajouter de la transparence pour le mélange

        # Appliquer le filtre sur l'image
        image_with_filter.blit(color_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return image_with_filter

    def afficher_unite(self, tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface, grid_x, grid_y):
        # Obtenir l'image correspondant au type d'unité

        tuile = self.gameObj.tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('unites'):
            return

        for joueur, buildings in tuile['unites'].items():

            unit_tile = units_dict.get(tile_type, {}).get('image')
            if not unit_tile:
                return  # Si l'image n'existe pas, ne rien faire

            if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                continue  # Si l'image n'est pas valide, passez à l'élément suivant

            # Récupérer la couleur du joueur depuis PLAYER_COLORS
            player_color = PLAYER_COLORS.get(joueur, (255, 255, 255))  # Blanc par défaut

            # Appliquer un filtre de couleur sur une copie de l'image
            unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)

            # Calculer les offsets
            offset_x = tile_grass.width_half - unit_tile.width // 2
            offset_y = tile_grass.height_half - unit_tile.height // 2

            # Recalculer les coordonnées isométriques pour l'unité
            iso_x = (cart_x - cart_y) - cam_x + offset_x
            iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y
            #print("reel",iso_x, iso_y)

            # print("units", cart_x,cart_y)
            display_surface.blit(unit_image_colored, (iso_x, iso_y))

    def afficher_buildings(self, grid_x, grid_y, cam_x, cam_y, display_surface):
        tuile = self.gameObj.tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('batiments'):
            return

        for joueur, buildings in tuile['batiments'].items():
            for tile_type, data in buildings.items():
                if isinstance(data, dict) and data.get('principal'):
                    # Vérifiez si les données du bâtiment existent
                    if tile_type not in builds_dict:
                        return

                    unit_tile = builds_dict.get(tile_type, {}).get('tile')
                    if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                        continue  # Si l'image n'est pas valide, passez à l'élément suivant

                    # Récupérer la couleur du joueur depuis PLAYER_COLORS
                    player_color = PLAYER_COLORS.get(joueur, (255, 255, 255))  # Blanc par défaut

                    # Appliquer un filtre de couleur sur une copie de l'image
                    unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)

                    # Calculer les coordonnées cartésiennes de la tuile
                    centered_col = grid_y - size // 2  # Décalage en X (par rapport à la grille)
                    centered_row = grid_x - size // 2  # Décalage en Y (par rapport à la grille)

                    offset_y = tile_grass.height_half - unit_tile.height
                    offset_x = tile_grass.width_half - unit_tile.width

                    # Calcul des coordonnées cartésiennes
                    cart_x = centered_col * tile_grass.width_half
                    cart_y = centered_row * tile_grass.height_half

                    # Conversion en coordonnées isométriques
                    iso_x = (cart_x - cart_y) - cam_x  # - offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y + offset_y

                    display_surface.blit(unit_image_colored, (iso_x, iso_y))


    def render2(self, display_surface, cam_x, cam_y):
        
        for i in range(size):
            for j in range(size):
                mapToDisplay[i][j] = " "
        for position in self.gameObj.ressourcesDict :
                mapToDisplay[position[0]][position[1]] = (self.gameObj.ressourcesDict[position].entityType, None)

        for row in range(size):
            for col in range(size):
                
                tileType = mapToDisplay[col][row][0]
                
                
                if tileType == "W":
                    tile = ressources_dict['W']['image']
                    offset_y = tile.height - tile_grass.height
                elif tileType == "G":
                    tile = ressources_dict['G']['image']
                    offset_y = tile.height - tile_grass.height
                else:
                    tile = tile_grass
                    offset_y = 0

                # Coordonnées cartésiennes centrées
                centered_col = col - half_size  # Décalage en X
                centered_row = row - half_size  # Décalage en Y

                # Conversion en coordonnées isométriques
                cart_x = centered_col * tile_grass.width_half
                cart_y = centered_row * tile_grass.height_half

                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                display_surface.blit(tile.image, (iso_x, iso_y))


        for position, building in self.gameObj.buildingsDict.items():
            (x, y) = position
            tileType = building.entityType
            for buildingType in ("T", "H", "C", "F", "B", "S", "A", "K"):
                if tileType == buildingType:
                    tile = builds_dict[buildingType]['tile']
                    offset_y = tile.height - tile_grass.height
                    unit_tile = builds_dict.get(tileType, {}).get('tile')
                    if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                        continue  # Si l'image n'est pas valide, passez à l'élément suivant

                    # Récupérer la couleur du joueur depuis PLAYER_COLORS
                    player_color = PLAYER_COLORS.get(building.playerName, (255, 255, 255))  # Blanc par défaut

                    # Appliquer un filtre de couleur sur une copie de l'image
                    unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)

                    # Calculer les coordonnées cartésiennes de la tuile
                    centered_col = x - size // 2  # Décalage en X (par rapport à la grille)
                    centered_row = y - size // 2  # Décalage en Y (par rapport à la grille)

                    offset_y = tile_grass.height_half - unit_tile.height
                    offset_x = tile_grass.width_half - unit_tile.width

                    # Calcul des coordonnées cartésiennes
                    cart_x = centered_col * tile_grass.width_half
                    cart_y = centered_row * tile_grass.height_half

                    # Conversion en coordonnées isométriques
                    iso_x = (cart_x - cart_y) - cam_x  # - offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y + offset_y

                    display_surface.blit(unit_image_colored, (iso_x, iso_y))



        for person in self.gameObj.persons:
            (x, y) = person.position

            unit_tile = units_dict.get(person.entityType, {}).get('image')
            if not unit_tile:
                return  # Si l'image n'existe pas, ne rien faire

            if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                continue  # Si l'image n'est pas valide, passez à l'élément suivant

            # Récupérer la couleur du joueur depuis PLAYER_COLORS
            player_color = PLAYER_COLORS.get(person.playerName, (255, 255, 255))  # Blanc par défaut

            # Appliquer un filtre de couleur sur une copie de l'image
            unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)
            centered_col = x - size // 2  # Décalage en X (par rapport à la grille)
            centered_row = y - size // 2
            # Calculer les offsets
            offset_x = tile_grass.width_half - unit_tile.width // 2
            offset_y = tile_grass.height_half - unit_tile.height // 2

            cart_x = centered_col * tile_grass.width_half
            cart_y = centered_row * tile_grass.height_half
            # Recalculer les coordonnées isométriques pour l'unité
            iso_x = (cart_x - cart_y) - cam_x + offset_x
            iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y
            #print("reel",iso_x, iso_y)

            # print("units", cart_x,cart_y)
            display_surface.blit(unit_image_colored, (iso_x, iso_y))




            



    def move_player(self, direction):
        x, y = self.position_initiale
        self.gameObj.tuiles[y,x] = " "  # Efface l'ancienne position

        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < size - 1:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < size - 1:
            x += 1

        self.position_initiale = (x, y)
