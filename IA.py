from Units import *
from Buildings import Buildings
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur

class StrategyManager:
    def __init__(self, gameObj, joueur, unit_methods):
        """Initialize the strategy manager"""
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = unit_methods
        try:
            self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
            self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]
        except KeyError:
            print(f"Error: Player {joueur} not found in compteurs_joueurs")
            self.batiments = {}
            self.ressources = {}

    def select_strategy(self):
        """
        Selects strategy based on game conditions
        Returns: 'offensive', 'defensive', or 'economic'
        """
        try:
            # Resource evaluation
            gold = self.ressources.get('G', 0)
            wood = self.ressources.get('W', 0) 
            food = self.ressources.get('f', 0)
            population = self.ressources.get('U', 0)
            max_pop = self.ressources.get('max_pop', 200)

            # Military building analysis
            barracks = self.batiments.get('B', 0)
            archery_range = self.batiments.get('A', 0)
            stable = self.batiments.get('S', 0)

            # Strategy selection logic
            if population >= max_pop * 0.9:
                return 'offensive'  # Population near max, attack
                
            if gold < 100 or wood < 150 or food < 200:
                return 'economic'  # Low resources, focus on economy
                
            if not (barracks or archery_range or stable):
                return 'economic'  # No military buildings, build economy
                
            if len(self.find_nearby_enemies()) > 2:
                return 'defensive'  # Multiple enemies nearby, defend
                
            if gold > 300 and wood > 250 and food > 400:
                return 'offensive'  # Rich in resources, attack
                
            return 'economic'  # Default to economic strategy
            
        except Exception as e:
            print(f"Error in strategy selection: {e}")
            return 'economic'  # Default to economic if error

    def find_nearby_enemies(self):
        """Find enemy units and buildings in proximity"""
        try:
            nearby_enemies = []
            for position, tile_data in self.gameObj.tuiles.items():
                if 'unites' in tile_data:
                    for enemy, units in tile_data['unites'].items():
                        if enemy != self.joueur:
                            nearby_enemies.append((position, 'unit', enemy))
                if 'batiments' in tile_data:
                    for enemy, buildings in tile_data['batiments'].items():
                        if enemy != self.joueur:
                            nearby_enemies.append((position, 'building', enemy))
            return nearby_enemies
        except Exception as e:
            print(f"Error finding nearby enemies: {e}")
            return []

    def execute_strategy(self):
        """
        Exécute la stratégie sélectionnée.
        """
        strategy = self.select_strategy()

        if strategy == 'offensive':
            self.Strat_offensive()
        elif strategy == 'defensive':
            self.Strat_defensive()
        elif strategy == 'economic':
            self.Strat_economique()

    def Strat_offensive(self):
        """
        Exécute la stratégie offensive.
        """
        print("Exécution de la stratégie offensive.")
        # Priorité : Construire des bâtiments militaires, entraîner des unités de combat
        strat_offensive = StratOffensive(self.gameObj, self.joueur)
        strat_offensive.execute(self.joueur)

    def Strat_defensive(self):
        """
        Exécute la stratégie défensive.
        """
        print("Exécution de la stratégie défensive.")
        # Priorité : Construire des bâtiments défensifs, protéger les ressources
        strat_defensive = StratDefensive(self.gameObj, self.joueur)
        strat_defensive.execute(self.joueur)

    def Strat_economique(self):
        """
        Exécute la stratégie économique.
        """
        print("Exécution de la stratégie économique.")
        # Priorité : Augmenter la collecte de ressources, construire des bâtiments économiques
        strat_economique = StratEconomique(self.gameObj, self.joueur)
        strat_economique.execute(self.joueur)

class StratDefensive:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie défensive pour un joueur
        :param gameObj: Objet de jeu contenant l'état global
        :param joueur: Identifiant du joueur
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_defensif(self):
        """
        Construit des bâtiments défensifs comme des murailles, des tours ou des fortifications.
        """
        # Vérifier si les ressources nécessaires sont disponibles pour construire un bâtiment défensif
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)
        
        if gold > 100 and wood > 200:
            print(f"{self.joueur} construit une tour de défense.")
            # Logique de construction d'un bâtiment défensif
            self.gameObj.construire_batiment(self.joueur, 'tour')
            self.ressources['G'] -= 100 # Déduire le coût en or
            self.ressources['W'] -= 200 # Déduire le coût en bois

    def proteger_ressources(self):
        """
        Déplace les unités militaires pour protéger les ressources
        """
        # Exemple : Déplacer une unité militaire vers les ressources
        for position, tuile in self.gameObj.tuiles.items():
            if 'ressources' in tuile and tuile['ressources']:
                for ressource in tuile['ressources']:
                    if ressource == 'G' or ressource == 'W': # Par exemple, on protège l'or et le bois
                        print(f"{self.joueur} déplace une unité militaire pour protéger les ressources à {position}")
                        # Logique pour déplacer une unité militaire vers la ressource
                        self.unit.deplacer_unite(self.joueur, 'militaire', 1, position) # ID de l'unité militaire 1

    def execute(self, joueur):
        """
        Exécute la stratégie défensive
        """
        print("Exécution de la stratégie défensive.")
        # Priorité : Construire des bâtiments défensifs, protéger les ressources
        self.construire_batiment_defensif()
        self.proteger_ressources()

class StratEconomique:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie économique pour un joueur
        :param gameObj: Objet de jeu contenant l'état global
        :param joueur: Identifiant du joueur
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_economique(self):
        """
        Construit des bâtiments économiques comme des centres-villes, des fermes, etc.
        """
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)
        food = self.ressources.get('F', 0)
        
        if gold > 200 and wood > 150 and food > 100:
            print(f"{self.joueur} construit un centre-ville.")
            self.gameObj.construire_batiment(self.joueur, 'centre_ville')
            self.ressources['G'] -= 200
            self.ressources['W'] -= 150
            self.ressources['F'] -= 100

    def optimiser_collecte_ressources(self):
        """
        Assigne des villageois à la collecte optimale de ressources
        """
        # Exemple de logique d'assignation des villageois
        villageois_inactifs = self.get_inactifs()
        for villageois in villageois_inactifs:
            # Assignation des villageois aux ressources les plus importantes
            self.assigner_ressource_optimale(villageois)

    def execute(self, joueur):
        """
        Exécute la stratégie économique
        """
        print("Exécution de la stratégie économique.")
        self.construire_batiment_economique()
        self.optimiser_collecte_ressources()

class StratOffensive:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie offensive pour un joueur.
        :param gameObj: Objet de jeu contenant l'état global.
        :param joueur: Identifiant du joueur.
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_militaire(self):
        """
        Construit des bâtiments militaires comme des casernes, des écuries, etc.
        """
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)
        
        # Si les ressources sont suffisantes, construire un bâtiment militaire
        if gold > 150 and wood > 100:
            print(f"{self.joueur} construit une caserne.")
            # Logique pour construire la caserne
            self.gameObj.construire_batiment(self.joueur, 'caserne')
            self.ressources['G'] -= 150 # Déduire le coût en or
            self.ressources['W'] -= 100 # Déduire le coût en bois

    def entrainer_unite_militaire(self):
        """
        Entraîne des unités militaires pour préparer l'attaque (soldats, archers, etc.).
        """
        # Vérifier les bâtiments militaires
        if 'caserne' in self.batiments:
            print(f"{self.joueur} entraîne un soldat.")
            # Logique d'entraînement d'une unité (par exemple, un soldat)
            self.gameObj.entraîner_unite(self.joueur, 'soldat')
        if 'ecurie' in self.batiments:
            print(f"{self.joueur} entraîne un cavalier.")
            # Logique d'entraînement d'une autre unité militaire (par exemple, un cavalier)
            self.gameObj.entraîner_unite(self.joueur, 'cavalier')

    def attaquer_ennemi(self):
        """
        Attaque les ennemis proches.
        """
        enemies = self.trouver_ennemis_proches()
        if enemies:
            for enemy in enemies:
                print(f"{self.joueur} envoie des unités attaquer l'ennemi à {enemy}.")
                # Logique pour attaquer un ennemi (par exemple, déplacer des unités militaires)
                self.unit.deplacer_unite(self.joueur, 'militaire', 1, enemy) # Exemple de déplacement d'unité

    def trouver_ennemis_proches(self):
        """
        Trouve les ennemis proches à attaquer.
        :return: Liste des positions ennemies proches.
        """
        nearby_enemies = []
        for position, tile_data in self.gameObj.tuiles.items():
            if 'unites' in tile_data:
                for enemy, units in tile_data['unites'].items():
                    if enemy != self.joueur: # Si l'ennemi n'est pas le joueur actuel
                        nearby_enemies.append(position)
        return nearby_enemies

    def execute(self, joueur):
        """
        Exécute la stratégie offensive pour le joueur.
        """
        print("Exécution de la stratégie offensive.")
        
        # Priorités : Construire des bâtiments militaires, entraîner des unités militaires, attaquer les ennemis
        self.construire_batiment_militaire() # Construire des bâtiments militaires
        self.entrainer_unite_militaire() # Entraîner des unités militaires
        self.attaquer_ennemi() # Attaquer les ennemis proches
