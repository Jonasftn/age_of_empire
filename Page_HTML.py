import os
from constants import *


class Page_HTML:
    def __init__(self):
        pass

    def generate_html(self, persons, ressources, buildings):
        # Début du fichier HTML
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Game Snapshot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                h1, h2 {
                    color: #333;
                }
                .tab {
                    display: none;
                }
                .tab-button {
                    background-color: #5d85ab;
                    color: white;
                    padding: 10px 20px;
                    cursor: pointer;
                    border: none;
                    margin-right: 10px;
                    font-size: 16px;
                }
                .tab-button:hover {
                    background-color: #587795;
                }
                .active {
                    background-color: #5d85ab;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 20px;
                }
                table, th, td {
                    border: 1px solid #ccc;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f4f4f4;
                }
            </style>
            <script>
                function showTab(player) {
                    var tabs = document.querySelectorAll('.tab');
                    var buttons = document.querySelectorAll('.tab-button');

                    // Masquer tous les onglets
                    tabs.forEach(tab => tab.style.display = 'none');
                    buttons.forEach(button => button.classList.remove('active'));

                    // Afficher l'onglet du joueur sélectionné
                    document.getElementById(player).style.display = 'block';
                    document.querySelector('[data-player="' + player + '"]').classList.add('active');
                }

                document.addEventListener("DOMContentLoaded", function() {
                    var firstPlayer = document.querySelector('.tab-button');
                    if (firstPlayer) {
                        showTab(firstPlayer.getAttribute('data-player'));
                    }
                });
            </script>
        </head>
        <body>
            <h1>Game Snapshot</h1>
        """

        joueurs = set(person.playerName for person in persons)

        joueurs_tries = sorted(joueurs, key=lambda x: int(x.split('_')[1]))

        # Création des boutons pour chaque joueur
        for joueur in joueurs_tries:
            html += f'<button class="tab-button" data-player="{joueur}" onclick="showTab(\'{joueur}\')">Joueur {joueur}</button>'

        # Création des onglets pour chaque joueur
        for joueur in joueurs_tries:
            html += f'<div id="{joueur}" class="tab">'
            html += f"<h2>Unité du joueur {joueur}</h2>"
            html += "<table><tr><th>Type d'unité</th><th>HP</th><th>Coordonnées</th></tr>"

            for person in persons:
                if person.playerName == joueur:
                    type_unite = person.entityType
                    hp_unite = person.healthPoint
                    coord = person.position
                    if type_unite == 'v':
                        type_unite = "Villageois"
                    elif type_unite == 's':
                        type_unite = "Épéiste"
                    elif type_unite == 'h':
                        type_unite = "Hallebardier"
                    elif type_unite == 'a':
                        type_unite = "Archer"
                    html += f"<tr><td>{type_unite}</td><td>{hp_unite}</td><td>{coord}</td></tr>"

            html += "</table>"

            # Affichage des bâtiments du joueur
            html += f"<h2>Bâtiments du joueur {joueur}</h2>"
            batiments = [(coord, data) for coord, data in buildings.items() if data.playerName == joueur]
            html += "<table><tr><th>Type</th><th>HP</th><th>Coordonnées</th></tr>"
            for coord, batiment in batiments:
                if batiment.entityType == 'T':
                    bat_type = "Town Center"
                elif batiment.entityType == 'H':
                    bat_type = "House"
                elif batiment.entityType == 'C':
                    bat_type = "Camp"
                elif batiment.entityType == 'F':
                    bat_type = "Farm"
                elif batiment.entityType == 'B':
                    bat_type = "Barrack"
                elif batiment.entityType == 'S':
                    bat_type = "Stable"
                elif batiment.entityType == 'A':
                    bat_type = "Archery"
                elif batiment.entityType == 'K':
                    bat_type = "Keep"


                #coord = (batiment.x, batiment.y) if hasattr(batiment, 'x') else 'N/A'
                html += f"<tr><td>{bat_type}</td><td>{batiment.healthPoint}</td><td>{coord}</td></tr>"
            html += "</table>"

            html += "</div>"

        # Fin du fichier HTML
        html += """
            </body>
            </html>
        """

        # Écrire dans un fichier
        file_path = os.path.join(os.getcwd(), "game_snapshot.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        return file_path
