from math import sqrt
import math
import pygame
from constants import *
from colorama import Fore, Style
import time
import asyncio
from random import randint
from entity import *


from constants import *

class Buildings:
    def __init__(self, gameObj):
        self.gameObj = gameObj
        self.tile_grass = tile_grass
        self.map_data = map_data
        self.compteurs_joueurs = compteurs_joueurs
        self.file_attente_batiments = []


    def conversion(self, x, y):
        half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

        # Décalage centré pour le joueur
        centered_col = y - half_size
        centered_row = x - half_size

        # Conversion en coordonnées isométriques
        cart_x = centered_row * tile_grass.width_half
        cart_y = centered_col * tile_grass.height_half

        iso_x = cart_x - cart_y  # Ne pas soustraire cam_x ici
        iso_y = (cart_x + cart_y) / 2  # Ne pas soustraire cam_y ici

        return iso_x, iso_y

    def placer_joueurs_cercle(self, players, rayon, center_x, center_y):
        """Calculate cartesian positions for n players distributed in a circle around center."""
        positions = []
        angle_increment = 360 / players
        
        # Slightly increased radius - from size//3 to size//2.5
        adjusted_radius = int(size // 2.5)  # This will place them a bit further apart
        
        # Center should be at map center
        center_x = size // 2
        center_y = size // 2

        for i in range(players):
            angle = angle_increment * i
            # Calculate position
            cart_x = int(center_x + adjusted_radius * math.cos(math.radians(angle)))
            cart_y = int(center_y + adjusted_radius * math.sin(math.radians(angle)))
            
            # Ensure positions stay within map bounds, accounting for TC size (4x4)
            cart_x = max(6, min(cart_x, size - 6))  
            cart_y = max(6, min(cart_y, size - 6))
            
            positions.append((cart_x, cart_y))

        return positions

    # pour del : del self.gameObj.tuiles[(60, 110)]['unites']['v'][0]
    def trouver_position_avec_offset_dynamique(self, x, y, taille, size, half_size):
        portee = 1  # Portée initiale
        coord_libres = None

        while coord_libres is None:
            # Générer les offsets pour la portée actuelle
            offsets = [(dx, dy) for dx in range(-portee, portee + 1) for dy in range(-portee, portee + 1)
                       if abs(dx) <= portee and abs(dy) <= portee]

            # Essayer chaque offset dans la portée actuelle
            for offset_x, offset_y in offsets:
                coord_libres = self.trouver_coordonnees_motif(x, y, taille, size, size, offset_x, offset_y)
                if coord_libres:  # Trouvé une position valide
                    break


            # Si aucune position n'est trouvée, augmenter la portée
            if not coord_libres:
                portee += 1
                if portee > half_size:
                    raise ValueError("Impossible de trouver une position valide dans la portée maximale autorisée.")

        return coord_libres

    def trouver_coordonnees_motif(self, x, y, taille, size, size_half, offset_x, offset_y):
        """Find valid building position within radius of existing buildings"""
        
        # Get all existing buildings for this player
        player_buildings = []
        for pos, building in self.gameObj.buildingsDict.items():
            if building.playerName == self.playerName:
                player_buildings.append(pos)
        
        if not player_buildings:
            # If no buildings exist, use town center position
            reference_point = (x, y)
        else:
            # Use closest existing building as reference
            closest_building = min(player_buildings, 
                                 key=lambda p: (p[0]-x)**2 + (p[1]-y)**2)
            reference_point = closest_building

        # Smaller initial radius and max radius
        radius = 2  # Start closer (was 5)
        max_radius = 10  # Smaller max radius (was 20)
        
        while radius <= max_radius:
            # Try positions in current radius
            for dx in range(-radius, radius+1):
                for dy in range(-radius, radius+1):
                    test_x = reference_point[0] + dx
                    test_y = reference_point[1] + dy
                    
                    # Check if position is valid
                    if (0 <= test_x <= size-taille and 
                        0 <= test_y <= size-taille and
                        self.is_position_valid(test_x, test_y, taille)):
                        return test_x, test_y
            
            radius += 2  # Smaller increment (was 5)
        
        return None

    def is_position_valid(self, x, y, taille):
        """Check if position is valid for building placement"""
        # Check each tile needed for the building
        for dx in range(taille):
            for dy in range(taille):
                pos = (x + dx, y + dy)
                # Check if position is occupied
                if (pos in self.gameObj.buildingsDict or 
                    pos in self.gameObj.ressourcesDict or
                    'batiments' in self.gameObj.tuiles.get(pos, {}) or
                    'unites' in self.gameObj.tuiles.get(pos, {})):
                    return False
        return True

    def prochain_id_batiment(self, joueur, batiment):
        """
        Trouve le prochain identifiant disponible sous la forme f"{batiment}{i}" pour un joueur donné.
        """
        ids_existants = set()

        # Parcourt toutes les tuiles pour trouver les IDs existants pour le joueur et le bâtiment
        for position, data in self.gameObj.tuiles.items():
            if 'batiments' in data and joueur in data['batiments']:
                for b, info in data['batiments'][joueur].items():
                    if b == batiment and 'id' in info:
                        ids_existants.add(info['id'])

        numeros_existants = {
            int(id[len(batiment):]) for id in ids_existants
            if id.startswith(batiment) and id[len(batiment):].isdigit()
        }

        # Trouver le plus petit numéro non utilisé
        prochain_numero = 0
        while prochain_numero in numeros_existants:
            prochain_numero += 1

        # Retourner l'identifiant au format f"{batiment}{i}"
        return f"{batiment}{prochain_numero}"

    def ajouter_batiment(self, joueur, batiment, x, y, taille, status):
        if status == 0:
            self.creation_batiments(joueur, batiment, x, y, taille)
        elif status == 1:
            required_cost = builds_dict[batiment]['cout']
            if (compteurs_joueurs[joueur]["ressources"]['W'] >= required_cost['W']
                    and compteurs_joueurs[joueur]["ressources"]['G'] >= required_cost['G']
                    and compteurs_joueurs[joueur]["ressources"]['f'] >= required_cost['f']):
                if compteurs_joueurs[joueur]['ressources']['max_pop'] <= 200 - 5:
                    position = self.trouver_position_avec_offset_dynamique(x, y, taille, size, half_size)
                    if position:
                        bat_x, bat_y = position
                        if (bat_x, bat_y) not in self.gameObj.tuiles:
                            self.gameObj.tuiles[(bat_x, bat_y)] = {}
                        elif not isinstance(self.gameObj.tuiles[(bat_x, bat_y)], dict):
                            self.gameObj.tuiles[(bat_x, bat_y)] = {}

                        if "building_creation_queue" not in self.gameObj.tuiles[(bat_x, bat_y)]:
                            self.gameObj.tuiles[(bat_x, bat_y)]["building_creation_queue"] = []

                        # Vérifier s'il y a des villageois libres
                        assigned_villagers = self.assign_villagers_to_construction(joueur)
                        if assigned_villagers:  # Villageois trouvés, commencer immédiatement
                            self.gameObj.tuiles[(bat_x, bat_y)]["building_creation_queue"].append({
                                "joueur": joueur,
                                "batiment": batiment,
                                "taille": taille,
                                "time_started": time.time(),
                                "creation_time": builds_dict[batiment]["build_time"],
                                "ouvriers_assignes": len(assigned_villagers),
                                "villageois_ids": assigned_villagers,
                                "position": (bat_x, bat_y)
                            })
                        else:  # Aucun villageois, ajouter à la file d'attente
                            self.file_attente_batiments.append({
                                "joueur": joueur,
                                "batiment": batiment,
                                "taille": taille,
                                "creation_time": builds_dict[batiment]["build_time"],
                                "position": (bat_x, bat_y)
                            })

                        # Déduire les ressources
                        compteurs_joueurs[joueur]["ressources"]['W'] -= required_cost['W']
                        compteurs_joueurs[joueur]["ressources"]['f'] -= required_cost['f']
                        compteurs_joueurs[joueur]["ressources"]['G'] -= required_cost['G']
                else:
                    print("maxpop atteinte")
    def assign_villagers_to_construction(self, joueur_id):
        """
        Assigne un nombre donné de villageois libres à la construction.
        """
        villagers_free = []

        # Trouver les villageois libres pour le joueur
        for position, data in self.gameObj.tuiles.items():
            if "unites" in data and joueur_id in data["unites"]:
                villagers = data["unites"][joueur_id].get("v", {})
                for villager_id, villager_data in villagers.items():
                    if villager_data["Status"] == "libre":
                        villagers_free.append((position, villager_id, villager_data))

        if not villagers_free:  # Aucun villageois disponible
            return None

        num_to_assign = max(1, math.ceil(len(villagers_free) / 3))
        assigned_villagers = villagers_free[:num_to_assign]  # Prendre les premiers villageois libres

        # Marquer les villageois sélectionnés comme "occupé"
        for position, villager_id, villager_data in assigned_villagers:
            self.gameObj.tuiles[position]["unites"][joueur_id]["v"][villager_id]["Status"] = "occupé"

        return assigned_villagers

    def update_creation_times(self):
        current_time = time.time()

        # 1. Vérifier les bâtiments en attente
        for unit in self.file_attente_batiments[:]:  # Copie pour éviter les modifications pendant l'itération
            assigned_villagers = self.assign_villagers_to_construction(unit["joueur"])
            if assigned_villagers:  # Dès qu'un villageois est disponible
                unit["ouvriers_assignes"] = len(assigned_villagers)
                unit["villageois_ids"] = assigned_villagers  # On sauvegarde les villageois assignés
                unit["time_started"] = current_time  # Démarrer le temps de construction
                if "building_creation_queue" not in self.gameObj.tuiles[unit["position"]]:
                    self.gameObj.tuiles[unit["position"]]["building_creation_queue"] = []

                self.gameObj.tuiles[unit["position"]]["building_creation_queue"].append(unit)
                self.file_attente_batiments.remove(unit)

        # 2. Mettre à jour les constructions en cours
        for position, tile in self.gameObj.tuiles.items():
            if "building_creation_queue" in tile:
                queue = tile["building_creation_queue"]
                completed_units = []

                for unit in queue:
                    # Temps écoulé depuis le début
                    elapsed_time = current_time - unit["time_started"]
                    nominal_time = unit["creation_time"]
                    num_ouvriers = unit["ouvriers_assignes"]

                    # Temps effectif avec ouvriers
                    effective_time = (3 * nominal_time) / (num_ouvriers + 2)

                    if elapsed_time >= effective_time:  # Construction terminée
                        completed_units.append(unit)

                # Retirer les bâtiments terminés et les ajouter au jeu
                for unit in completed_units:
                    queue.remove(unit)
                    self.creation_batiments(
                        unit["joueur"], unit["batiment"], position[0], position[1], unit["taille"], self.gameObj.tuiles
                    )
                    if unit['joueur'] in compteurs_joueurs:
                        if unit['batiment'] in compteurs_joueurs[unit['joueur']]['batiments']:
                            compteurs_joueurs[unit['joueur']]['batiments'][unit['batiment']] += 1


                    if unit['batiment'] == 'T' or unit['batiment'] == 'H':
                        compteurs_joueurs[unit['joueur']]['ressources']['max_pop'] += 5



                    # Libérer les villageois assignés
                    if "villageois_ids" in unit:
                        for villager_info in unit["villageois_ids"]:
                            tile_pos, villager_id, villager_data = villager_info
                            self.gameObj.tuiles[tile_pos]["unites"][unit["joueur"]]["v"][villager_id]["Status"] = "libre"

                # Supprimer la file si elle est vide
                if not queue:
                    del tile["building_creation_queue"]

    def creation_batiments(self,joueur, batiment, x, y, taille):
        identifiant = self.prochain_id_batiment(joueur, batiment)
        for dx in range(taille):
            for dy in range(taille):
                tuile_position = (x + dx, y + dy)

                # Initialiser la tuile si nécessaire
                if tuile_position not in self.gameObj.tuiles:
                    self.gameObj.tuiles[tuile_position] = {'batiments': {}}
                if not isinstance(self.gameObj.tuiles[tuile_position], dict):
                    self.gameObj.tuiles[tuile_position] = {'batiments': {}}

                if "unites" not in self.gameObj.tuiles[tuile_position]:
                    self.gameObj.tuiles[tuile_position]["batiments"] = {}

                if joueur not in self.gameObj.tuiles[tuile_position]['batiments']:
                    self.gameObj.tuiles[tuile_position]['batiments'][joueur] = {}
                if taille ==4:
                    # Ajouter les informations principales ou secondaires
                    if dx == 3 and dy ==1:  # Nouvelle tuile principale 3-1
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']

                        }
                    else:  # Tuiles secondaires
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                elif taille ==3:

                    if dx == 2 and dy ==1:  # Nouvelle tuile principale 2-1
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                elif taille ==2:

                    if dx == 1 and dy ==0:  # Nouvelle tuile principale 1-0
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp'],
                            **({'quantite': builds_dict[batiment]['quantite']} if 'quantite' in builds_dict[
                                batiment] else {})
                        }
                    else:  # Tuiles secondaires
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp'],
                            **({'quantite': builds_dict[batiment]['quantite']} if 'quantite' in builds_dict[
                                batiment] else {})
                        }
                elif taille == 1:
                    if dx == 0 and dy ==0:  # Nouvelle tuile principale 0-0
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        self.gameObj.tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }

    def generer_offsets(self):
        for joueur, compteurs in compteurs_joueurs.items():
            if sum(compteurs['batiments'].values())<=9:
                portee = 2
            elif sum(compteurs['batiments'].values())<=25:
                portee = 3
            elif sum(compteurs['batiments'].values()) <= 49:
                portee = 4
            else :
                portee =5

            offsets = [(dx, dy) for dx in range(-portee, portee + 1) for dy in range(-portee, portee + 1)]
            # Trier d'abord par distance Manhattan, puis par proximité radiale
            return sorted(offsets, key=lambda offset: (abs(offset[0]) + abs(offset[1]), abs(offset[0]), abs(offset[1])))
        #return offsets

    def initialisation_compteur(self, position):
        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            (x,y) = position[idx]  # Point central pour ce joueur

            #position_building = self.trouver_coordonnees_motif(self, x, y, players, rayon, center_x, center_y)
            self.gameObj.buildingsDict[(x,y)] = Building(self.gameObj, 'T', (x,y), joueur)
            """for batiment, nombre in data['batiments'].items():
                taille = builds_dict[batiment]['taille']

                for i in range(nombre):
                    coord_libres = None
                    while coord_libres is None:
                        for offset_x, offset_y in offsets:
                            coord_libres = self.trouver_coordonnees_motif(
                                x, y, taille, size, size, offset_x, offset_y
                            )


                            if coord_libres:  # Trouvé une position valide
                                break


                        if not coord_libres:
                                raise ValueError(
                                    f"Impossible de trouver un emplacement libre pour le bâtiment {batiment}."
                                )
                    if coord_libres:
                        bat_x, bat_y = coord_libres
                        in_game = 0
                        self.ajouter_batiment(joueur, batiment, bat_x, bat_y, taille, in_game)"""

    def decrementer_hp_batiments(self):
        """Décroît les HP des bâtiments dans le dictionnaire tuiles, en tenant compte des bâtiments multi-tuiles."""
        traites = set()  # Pour éviter de traiter plusieurs fois le même bâtiment

        for (x, y), data in list(self.gameObj.tuiles.items()):
            if isinstance(data, dict) and 'batiments' in data:
                batiments = data['batiments']

                for joueur, joueur_batiments in list(batiments.items()):
                    for unite, stats in list(joueur_batiments.items()):
                        if isinstance(stats, dict):
                            # Identifier la tuile principale
                            parent = stats.get('parent', (x, y))
                            identifiant = stats.get('id', 'Inconnu')

                            # Si déjà traité, passer
                            if (joueur, identifiant) in traites:
                                continue

                            # Ajouter à la liste des traités
                            traites.add((joueur, identifiant))

                            if 'HP' in stats:
                                stats['HP'] -= 250

                                # Si les HP tombent à 0, supprimer le bâtiment
                                if stats['HP'] <= 0:
                                    stats['HP'] = 0
                                    self.supprimer_batiment(joueur, identifiant, parent)
                                    if joueur in compteurs_joueurs:
                                        if unite in compteurs_joueurs[joueur]['batiments'] and \
                                                compteurs_joueurs[joueur]['batiments'][unite] > 0:
                                            compteurs_joueurs[joueur]['batiments'][unite] -= 1
                                return

    def supprimer_batiment(self, joueur, identifiant, parent):
        """Supprime un bâtiment multi-tuiles."""
        tuiles_a_supprimer = []



        for (x, y), data in list(self.gameObj.tuiles.items()):
            if 'batiments' in data and joueur in data['batiments']:
                batiments = data['batiments'][joueur]

                for unite, stats in list(batiments.items()):
                    if isinstance(stats, dict) and stats.get('id') == identifiant:
                        del self.gameObj.tuiles[(x, y)]['batiments'][joueur][unite]



                        # Si le niveau est vide, marquer pour suppression
                        if not self.gameObj.tuiles[(x, y)]['batiments'][joueur]:
                            del self.gameObj.tuiles[(x, y)]['batiments'][joueur]
                        if not self.gameObj.tuiles[(x, y)]['batiments']:
                            tuiles_a_supprimer.append((x, y))

        # Supprimer les tuiles marquées
        for tuile in tuiles_a_supprimer:
            del self.gameObj.tuiles[tuile]

