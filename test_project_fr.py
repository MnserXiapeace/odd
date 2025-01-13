# Importation de toutes les fonctions et variables du module 'odd'
# et de la bibliothèque 'requests', 'textwrap
from project_fr import *
import requests
import textwrap
import io
import sys
from tabulate import tabulate


# Test de la fonction recuperer_objectifs_et_cibles
def test_recuperer_objectifs_et_cibles():
    # Appel direct à l'API pour récupérer la réponse brute
    response = requests.get("https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Goal/List?includechildren=true")
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

            # Comparer les résultats de la fonction avec ceux traités localement
            assert recuperer_objectifs_et_cibles() == tuple(list_goals_targets)
        else:
            # Si les données retournées par l'API sont vides
            assert False, "Les données retournées par l'API sont vides."
    else:
        # Si l'API ne répond pas correctement, on échoue le test
        assert False, f"Erreur API {response.status_code} : {response.text}"


# Test de la fonction recuperer_zones_geographiques
def test_recuperer_zones_geographiques():
    # Appel direct à l'API pour récupérer la réponse brute
    reponse = requests.get('https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List')

    if reponse.status_code == 200:
        list_geo_area_api = reponse.json()

        # On effectue le même traitement sur la réponse brute que celui de la fonction 'recuperer_zones_geographiques'
        for dico_area in list_geo_area_api:
            dico_area['geoAreaName'] = '\n'.join(textwrap.wrap(dico_area['geoAreaName'], width=30))

        # Vérification que la fonction retourne bien les mêmes données après traitement
        assert recuperer_zones_geographiques() == list_geo_area_api
    else:
        # Si l'API ne répond pas correctement, on échoue le test
        assert False, f"Erreur API {reponse.status_code} : {reponse.text}"


# Test de la fonction recuperer_code_zone_geographique On teste différents noms de pays avec des espaces en début et
# fin, et on vérifie que fetch_area_code renvoie les bons codes.
def test_recuperer_code_zone_geographique():
    assert get_geographic_area_code('     Benin') == '204'
    assert get_geographic_area_code('Qatar    ') == '634'
    assert get_geographic_area_code('Sudan') == '729'
    assert get_geographic_area_code('    State of Palestine   ') == '275'
    assert get_geographic_area_code('New Zealand ') == '554'
    assert get_geographic_area_code('SIDS Americas') == '932'
    assert get_geographic_area_code('United States of America') == '840'
    assert get_geographic_area_code('Ascension') == '655'
    assert get_geographic_area_code('World (total) by SDG regions') == '935'
    assert get_geographic_area_code('World (total) by continental regions') == '936'
    assert get_geographic_area_code('Western Sahara ') == '732'


# Test de la fonction recuperer_donnees_series_odd
def test_recuperer_series_odd():
    # Appel direct à l'API pour récupérer la réponse brute
    response = requests.get("https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/List")
    list_indi_series = []
    numero = 0

    if response.status_code == 200:
        list_indicators = response.json()

        # Appliquer le même traitement que dans la fonction 'recuperer_series_odd'
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

        # Comparer les résultats de la fonction avec ceux traités localement
        assert recuperer_series_odd() == list_indi_series
    else:
        # Si l'API ne répond pas correctement, on échoue le test
        assert False, f"Erreur API {response.status_code} : {response.text}"


# Test de la fonction recuperer_donnees_indicateur
def test_recuperer_donnees_indicateur():
    # On vérifie que la fonction fetch_indicator_data renvoie les mêmes données que la requête API pour divers indicateurs et codes de zones.
    assert get_indicator_data('1.1.1', '204') == requests.get(
        'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data?indicator=1.1.1&areaCode=204').json()
    assert get_indicator_data('11.a.1', '732') == requests.get(
        f'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data?indicator=11.a.1&areaCode=732').json()
    assert get_indicator_data('3.2.1', '840') == requests.get(
        f'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data?indicator=3.2.1&areaCode=840').json()
    assert get_indicator_data('6.1.1', '340') == requests.get(
        f'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data?indicator=6.1.1&areaCode=340').json()
    assert get_indicator_data('15.2.1', '162') == requests.get(
        f'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data?indicator=15.2.1&areaCode=162').json()


# Test de la fonction afficher_objectifs_et_cibles
def test_afficher_objectifs_et_cibles():
    # Capturer la sortie standard (le print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Appel de la fonction qui doit imprimer
    afficher_objectifs_et_cibles()

    # Récupérer les données de l'API pour comparaison
    expected_data = recuperer_objectifs_et_cibles()

    if expected_data:
        # Créer la sortie attendue sous forme de tableau avec tabulate
        expected_output = "\nListe des objectifs et cibles ODD\n" + tabulate(expected_data, headers="keys",
                                                                             tablefmt="grid") + "\n"

        # Comparer la sortie capturée avec la sortie attendue
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Erreur dans la récupération des données d'objectifs et cibles."

    # Remettre stdout à son état normal
    sys.stdout = sys.__stdout__


# Test de la fonction afficher_series_odd
def test_afficher_series_odd():
    # Capturer la sortie standard (le print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Appel de la fonction qui doit imprimer
    afficher_series_odd()

    # Récupérer les données de l'API pour comparaison
    expected_data = recuperer_series_odd()

    if expected_data:
        # Créer la sortie attendue sous forme de tableau avec tabulate
        expected_output = "\nListe des séries ODD\n" + tabulate(expected_data, headers="keys", tablefmt="grid") + "\n"

        # Comparer la sortie capturée avec la sortie attendue
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Erreur dans la récupération des séries ODD."

    # Remettre stdout à son état normal
    sys.stdout = sys.__stdout__


# Test de la fonction afficher_zones_geographiques
def test_afficher_zones_geographiques():
    # Capturer la sortie standard (le print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Appel de la fonction qui doit imprimer
    afficher_zones_geographiques()

    # Récupérer les données de l'API pour comparaison
    expected_data = recuperer_zones_geographiques()

    if expected_data:
        # Créer la sortie attendue sous forme de tableau avec tabulate
        expected_output = "\nListe des zones géographiques ODD\n" + tabulate(expected_data, headers="keys",
                                                                             tablefmt="grid") + "\n"

        # Comparer la sortie capturée avec la sortie attendue
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Erreur dans la récupération des zones géographiques."

    # Remettre stdout à son état normal
    sys.stdout = sys.__stdout__


if __name__ == '__main__':
    test_recuperer_zones_geographiques()
    test_recuperer_donnees_indicateur()
    test_recuperer_series_odd()
    test_recuperer_code_zone_geographique()
    test_recuperer_objectifs_et_cibles()
    test_afficher_series_odd()
    test_afficher_zones_geographiques()
    test_afficher_objectifs_et_cibles()

