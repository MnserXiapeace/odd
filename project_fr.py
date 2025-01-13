# Importation des bibliothèques nécessaires
import requests
import re
from tabulate import tabulate
import csv
import textwrap


# Fonction principale pour afficher le menu principal et demander l'entrée utilisateur
def main():
    """
    Affiche le menu principal et demande à l'utilisateur de choisir une option
    parmi les objectifs, cibles, zones géographiques, séries ODD ou indicateurs pour un pays.
    """
    print(
        """
            MENU

    1- Liste des objectifs et cibles ODD
    2- Liste et codes des zones géographiques
    3- Liste des séries ODD
    4- Trouver la valeur d'un indicateur pour un pays
        """
    )
    gestion_choix_utilisateur()


# Section des fonctions de récupération de données

# Fonction pour récupérer et afficher les objectifs et cibles ODD
def recuperer_objectifs_et_cibles():
    """
    Récupère et renvoie la liste des objectifs et des cibles ODD via l'API de l'ONU.
    Formate les données en ajoutant des sauts de lignes dans les titres longs.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Goal/List?includechildren=true"
    response = requests.get(base_url)
    list_goals_targets = []

    if response.status_code == 200:
        data = response.json()
        numero = 0

        if data:
            for goal in data:
                for target in goal["targets"]:
                    dict = {}
                    numero += 1
                    dict["N°"] = numero
                    dict["Code objectif"] = goal["code"]
                    dict["Titre objectif"] = '\n'.join(
                        textwrap.wrap(goal["title"], width=20))  # Retour à la ligne tous les 20 caractères
                    dict["Code cible"] = target["code"]
                    dict["Titre cible"] = '\n'.join(textwrap.wrap(target["title"], width=20))
                    list_goals_targets.append(dict)
            return tuple(list_goals_targets)

    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None


# Fonction pour récupérer la liste des zones géographiques
def recuperer_zones_geographiques():
    """
    Récupère la liste des zones géographiques via l'API de l'ONU et formate les noms des zones avec des sauts de ligne.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List"
    reponse = requests.get(base_url)

    if reponse.status_code == 200:
        list_geo_area = reponse.json()
        for dico_area in list_geo_area:
            dico_area['geoAreaName'] = '\n'.join(textwrap.wrap(dico_area['geoAreaName'], width=30))
        return list_geo_area
    else:
        print(f"Erreur {reponse.status_code} : {reponse.text}")
        return None


# Fonction pour récupérer le code de la zone géographique à partir du nom du pays
def get_geographic_area_code(nom_pays: str):
    """
    Récupère le code de la zone géographique correspondant au nom d'un pays donné via l'API de l'ONU.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List"
    reponse = requests.get(base_url)

    if reponse.status_code == 200:
        list_geo_area = reponse.json()
        nom_pays = nom_pays.strip()

        for geo_area in list_geo_area:
            if nom_pays == geo_area["geoAreaName"]:
                return str(geo_area["geoAreaCode"])

        print("Nom du pays renseigné est incorrect")
    else:
        print(f"Erreur {reponse.status_code} : {reponse.text}")
        return str(1)


# Fonction pour récupérer les données d'un indicateur pour une zone géographique donnée
def get_indicator_data(code_indicateur: str, code_zone: str):
    """
    Récupère les données d'un indicateur spécifique pour une zone géographique donnée via l'API de l'ONU.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data"
    params = {
        "indicator": code_indicateur,
        "areaCode": code_zone,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None


# Fonction pour récupérer la liste des séries d'indicateurs ODD
def recuperer_series_odd():
    """
    Récupère et renvoie la liste des séries d'indicateurs ODD via l'API de l'ONU.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/List"
    response = requests.get(base_url)
    list_indi_series = []
    global numero
    numero = 0

    if response.status_code == 200:
        list_indicators = response.json()

        for indicator in list_indicators:
            for series in indicator["series"]:
                numero += 1
                dict = {}
                dict["Numero"] = numero
                dict["Code série"] = series["code"]
                dict["Description"] = series["description"]
                dict["Objectif"] = ", ".join(series["goal"])
                dict["Cibles"] = ", ".join(series["target"])
                dict["Indicateurs"] = ", ".join(series["indicator"])
                dict["Version"] = series["release"]
                list_indi_series.append(dict)
        return list_indi_series
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None


# Section des fonctions d'affichage

# Fonction pour afficher la liste des objectifs et cibles ODD
def afficher_objectifs_et_cibles():
    """
    Affiche la liste des objectifs et cibles ODD sous forme de tableau.
    """
    print("\nListe des objectifs et cibles ODD")
    print(tabulate(recuperer_objectifs_et_cibles(), headers="keys", tablefmt="grid"))


# Fonction pour afficher la liste des séries ODD
def afficher_series_odd():
    """
    Affiche la liste des séries ODD sous forme de tableau.
    """
    print("\nListe des séries ODD")
    print(tabulate(recuperer_series_odd(), headers="keys", tablefmt="grid"))


# Fonction pour afficher la liste des codes des zones géographiques ODD
def afficher_zones_geographiques():
    """
    Affiche la liste des zones géographiques et leurs codes sous forme de tableau.
    """
    print("\nListe des zones géographiques ODD")
    print(tabulate(recuperer_zones_geographiques(), headers="keys", tablefmt="grid"))


# Section des fonctions d'interaction utilisateur

# Fonction pour supprimer des colonnes inutiles
def supprimer_colonnes_inutiles(liste_dict: list):
    """
    Supprime les colonnes inutiles d'une liste de dictionnaires. Par dictionnaire comprehension
    """
    new_list = []
    keys_to_remove = ['goal', 'target', 'geoAreaCode', 'geoAreaName', 'valueType', 'time_detail', 'upperBound',
                      'lowerBound', 'geoInfoUrl']
    for element_dict in liste_dict:
        nouveau_dict = {k: v for k, v in element_dict.items() if k not in keys_to_remove}
        new_list.append(nouveau_dict)
    return new_list


# Fonction pour trouver la valeur d'un indicateur pour un pays
def trouver_valeur_indicateur_pays():
    """
    Permet de trouver la valeur d'un indicateur ODD pour une zone géographique donnée en interagissant avec l'utilisateur.
    """
    areas = [geo_area["geoAreaName"] for geo_area in recuperer_zones_geographiques()]
    areas_codes = [geo_area["geoAreaCode"] for geo_area in recuperer_zones_geographiques()]

    while True:
        try:
            pattern = r"^([1-9]{1,2}|10)\.([1-9]{1,2}|[a-d]{1}|10)\.([1-9]{1,2})$" # Pattern pour valider l'entree des indicateurs
            area = input("Nom de la zone géographique / Code de la zone : ").strip().title()
            indicator = input("Code de l'indicateur (#.#.#) : ").strip()
            match = re.fullmatch(pattern, indicator, re.IGNORECASE)

            if (match is not None) and (area in areas or area in areas_codes):
                code_zone = area if area.isnumeric() else get_geographic_area_code(area)
                data = get_indicator_data(indicator, code_zone)
                data_complet = {k: v for k, v in data.items()}  # Copie de data, afin de l'utiliser lors de l'exportation en CSV sans appliquer la supression des collonnes

                if len(data["data"]) > 0:
                    print(
                        f"\nIndicateur N° {indicator} pour {data['data'][0]['geoAreaName']} ({data['data'][0]['geoAreaCode']})")
                    for d in data['data']:
                        d['seriesDescription'] = '\n'.join(textwrap.wrap(d['seriesDescription'], width=22)) #Formatte et limite les dimensions à 15 caractères par ligne pour une meilleure lisibilité d'une chaine
                        d['source'] = '\n'.join(textwrap.wrap(d['source'], width=15))
                        d['footnotes'] = '\n'.join(textwrap.wrap(' '.join(d['footnotes']), width=20)) # Formatte et limite les dimensions à 15 caractères par ligne pour une meilleure lisibilité d'une liste de chaines

                        # Formatte et limite les dimensions à 15 caractères par ligne pour une meilleure lisibilité,
                        # d'une liste de dictionnaires
                        tab_of_dimensions = []
                        for element in d['dimensions']:
                            tab_of_dimensions.append(f'{element}: {d["dimensions"][element]}')
                        d['dimensions'] = '\n'.join(textwrap.wrap(' '.join(tab_of_dimensions), width=15))

                    data_sans_colonnes = supprimer_colonnes_inutiles(data['data'])  # suprimer les collones encombrants
                    print(tabulate(data_sans_colonnes, headers="keys", tablefmt="grid"))
                    export = input("Voulez-vous exporter en fichier CSV ? (y/n): ").strip().lower()[:1]
                    if export == "y":
                        exporter_en_csv(data_complet['data'], data['data'][0]['geoAreaName'], indicator)
                        print("Exporté avec succès")

                    accept = input("Voulez-vous essayer à nouveau ? (y/n): ").strip().lower()[:1]
                    if accept != "y":
                        break
                else:
                    print("Entrée incorrecte")
            else:
                continue
        except BaseException as e:
            print(e)
            break


# Fonction pour exporter les données en fichier CSV
def exporter_en_csv(tableau_dicts: list, nom_zone: str, indicateur: str):
    """
    Exporte une liste de dictionnaires en fichier CSV.
    """
    fieldnames = tableau_dicts[0].keys()
    with open(f'{nom_zone}_{indicateur}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        writer.writeheader()
        for dic in tableau_dicts:
            writer.writerow(dic)


# Fonction qui gère les choix de l'utilisateur dans le menu
def gestion_choix_utilisateur():
    """
    Gère le choix de l'utilisateur dans le menu principal et exécute les actions correspondantes.
    """
    while True:
        try:
            choix_menu = int(input("Choisissez une option (1-4) : "))
            if choix_menu == 1:
                afficher_objectifs_et_cibles()
                break
            elif choix_menu == 2:
                afficher_zones_geographiques()
                break
            elif choix_menu == 3:
                afficher_series_odd()
                break
            elif choix_menu == 4:
                trouver_valeur_indicateur_pays()
                break
            else:
                print("Choix invalide. Veuillez choisir entre 1 et 4.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")


if __name__ == "__main__":
    main()
