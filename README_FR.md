# Projet de récupération de données ODD (ODD Data Retrieval Project)

#### Video Demo:  [ODData Retrieval video demo](https://www.youtube.com/watch?v=LfaMVlDaQ24)

#### Description:
Ce projet permet de récupérer des données relatives aux **Objectifs de Développement Durable (ODD)** à partir de l'`API` des Nations Unies. Il offre diverses fonctionnalités pour explorer les **objectifs, les cibles, les séries d'indicateurs et les zones géographiques associées aux ODD**.

## Fonctionnalités :

- **Lister les Objectifs et les Cibles ODD** : *Affiche tous les objectifs et les cibles des ODD dans un format tabulaire.*
- **Lister les Zones Géographiques** : _Affiche une liste des zones géographiques avec leurs codes associés._
- **Récupérer un Code de Zone à partir d'une Zone** : *Trouve le code géographique associé à une zone spécifique.*
- **Récupérer les Données d'un Indicateur pour une Zone** : *Récupère les données d'un indicateur ODD pour une zone géographique donnée.*
- **Lister les Séries d'Indicateurs** : *Affiche la liste des séries d'indicateurs ODD avec des détails comme leur description, objectif, cibles, et indicateurs liés.*
- **Exporter les Données en Fichier CSV** : _Permet d'exporter les données récupérées vers un fichier CSV._

## Installation :

1. Cloner ce dépôt sur votre machine.
2. Installez les dépendances Python nécessaires en exécutant :
   ```bash
   pip install requests tabulate

## Utilisation :

1. Exécutez le script avec Python :
    ```bash
    python odd.py

2. Choisissez l'une des options du menu pour interagir avec les données ODD. *(Voir rubrique Fonctionnement)*

## API Source :

Les données sont récupérées via l'API des Nations Unies pour les ODD: **https://unstats.un.org/sdgs/UNSDGAPIV5**

## Fonctionnement
Une fois le script lancé, le menu principal vous propose plusieurs options :

        MENU

    1- List of SDG Goals and Targets
    2- List and Codes of Geographic Areas (GeA)
    3- List of SDG Series
    4- Find the Value of an Indicator for a Country or a GeA
      

*Choisir une option entre `(1-4)`, permet de :* 

    1- Lister les Objectifs et Cibles : Affiche les objectifs et cibles des ODD dans un tableau.
    2- Lister et Codes des Zones Géographiques : Affiche une liste de zones géographiques avec leurs codes.
    3- Lister les Séries ODD : Affiche une liste des séries d'indicateurs avec leurs descriptions et détails.
    4- Trouver la Valeur d'un Indicateur pour un Pays : Récupère les données d'un indicateur spécifique pour une zone géographique.

### Choix 1- List the Goals and Targets :
*Exemple de listes des **objectifs** et des **cibles ODD***

      ODD Goals & targets list
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      | N° | Goal code | Goal title          | Target code   | Target title                                                  |
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      |  1 | 1         | End poverty in all  | 1.1           | By 2030, eradicate extreme poverty for all people everywhere, |
      |    |           | its forms everywhere|               | currently measured as people living on less than $1.25 a day  |
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      ...


### Choix 2- List and Code of Areas :
*Exemple de listes et code des zones géographiques*

      ODD GEO LIST
      +-------------+-------------------------------------------------------------+
      | geoAreaCode | geoAreaName                                                 |
      +-------------+-------------------------------------------------------------+
      |  4          | Afghanistan                                                 |
      +-------------+-------------------------------------------------------------+
      |  248        | Åland Islands                                               |
      +-------------+-------------------------------------------------------------+      
      ...


### Choix 3- List of SDG Series :
*Exemple de listes des **Series SDG***

      ODD SERIES LIST
      +----------+----------------------+---------------------------------------------------------------------------------+------------+-----------------+-----------------------+--------------+
      |   Numero | Code serie           | Description                                                                     | Objectif   | Cibles          | Indicateurs           | Version      |
      +==========+======================+=================================================================================+============+=================+=======================+==============+
      |        1 | SI_POV_DAY1          | Proportion of population below international poverty line (%)                   | 1          | 1.1             | 1.1.1                 | 2024.Q2.G.03 |
      +----------+----------------------+---------------------------------------------------------------------------------+------------+-----------------+-----------------------+--------------+
      |        2 | SI_POV_EMP1          | Employed population below international poverty line, by sex and age (%)        | 1          | 1.1             | 1.1.1                 | 2024.Q2.G.03 |
      +----------+----------------------+---------------------------------------------------------------------------------+------------+-----------------+-----------------------+--------------+
      |        3 | SI_POV_NAHC          | Proportion of population living below the national poverty line (%)             | 1          | 1.2             | 1.2.1                 | 2024.Q2.G.03 |
      +----------+----------------------+---------------------------------------------------------------------------------+------------+-----------------+-----------------------+--------------+
      ...
### Choix 4- Find the Value of an Indicator for a Country :
#### Trouver la valeur de l'indicateur : 
1. Une fois l'option `4` saisi et validé, le `terminal` ou votre `CLI` vous affiche :

         Geo area name / Geo area code: 
   Vous êtes invités à renseigner le `geoAreaName` ou le `geoAreaCode` de la zone dont vous cherchez les **informations ODD** *(eg: Benin ou 204)*.
2. Ensuite le prompt demande de renseigner le **code de l'indicateur** *(eg: 1.1.1 ou 5.2.1)*:

         Indicator code (#.#.#): 
3. Enfin, vous obtenez les informations depuis l'API officiel "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data"
      
         Indicator N° 11.a.1 for Afghanistan (4)
         +--------+----------+-------------+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+---------------+---------------+-------------------+---------+-------------+---------------+----------------+--------------+--------------+--------------+-----------------+--------------+---------------------------------------------------------------------+-----------------+-------------------------+
         | goal   | target   | indicator   | series       | seriesDescription                                                                                                                                                                                         |   seriesCount |   geoAreaCode | geoAreaName   |   timePeriodStart |   value | valueType   | time_detail   | timeCoverage   | upperBound   | lowerBound   | basePeriod   | source          | geoInfoUrl   | footnotes                                                           | attributes      | dimensions              |
         +========+==========+=============+==============+===========================================================================================================================================================================================================+===============+===============+===============+===================+=========+=============+===============+================+==============+==============+==============+=================+==============+=====================================================================+=================+=========================+
         | ['11'] | ['11.a'] | ['11.a.1']  | SD_CPA_UPRDP | Countries that have national urban policies or regional development plans that respond to population dynamics; ensure balanced territorial development; and increase local fiscal space (1 = YES; 0 = NO) |           265 |             4 | Afghanistan   |              2020 |       1 | Float       |               |                |              |              |              | NUP 2020 Status |              | ['UN-Habitat Global Survey on National Urban Policies 2018 & 2020'] | {'Nature': 'C'} | {'Reporting Type': 'G'} |
         +--------+----------+-------------+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+---------------+---------------+-------------------+---------+-------------+---------------+----------------+--------------+--------------+--------------+-----------------+--------------+---------------------------------------------------------------------+-----------------+-------------------------+
         Would you want to export in CSV file? (y/n): 

#### Export des données en CSV :
   *Vous pouvez choisir d'exporter ou pas les données récupérées sous forme de fichier `CSV`.
Le fichier sera enregistré avec le nom suivant :*

      <nom_de_la_zone_geographique>_<code_indicateur>.csv

## Licence :

Ce projet est sous licence `MIT`, developpé par  Serge ADANDE.


