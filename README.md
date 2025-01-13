# ODD Data Retrieval Project

#### Video Demo:  [SDG data retrieval  CLI demo](https://youtu.be/wRnMhu2xAJU)

#### Description:
This project allows for retrieving data related to the **Sustainable Development Goals (SDGs)** from the United Nations `API`. It offers various functionalities to explore **goals, targets, indicator series, and geographical areas associated with the SDGs.**
## Functionalities :

- **List SDG Goals and Targets** : *Displays all SDG goals and their associated targets in a tabular format.*
- **List Geographical Areas** : _Displays a list of geographical areas along with their associated codes._
- **Retrieve Zone Code from Area** : *Finds the geographical code associated with a specific area.*
- **Retrieve Indicator Data for a Zone** : *Fetches SDG indicator data for a given geographical area.*
- **List Indicator Series** : *Displays the list of SDG indicator series with details such as description, goal, targets, and related indicators.*
- **Export Data to CSV File** : _Allows exporting the retrieved data to a CSV file.._

## Installation :

1. Clone this repository to your machine:
   ```bash
   git clone ..........
   
2. IInstall the necessary Python dependencies by running one of the following commands :
   ```bash
   pip install requests tabulate
   

   pip install -r requirements.txt
   
## Utilisation :

1. Run the script with Python :
    ```bash
    python project.py

2. Choose one of the menu options to interact with the SDG data. *(See the Functionality section)*

## API Source :

he data is retrieved via the United Nations SDG API: **https://unstats.un.org/sdgs/UNSDGAPIV5**

## How it Works
Once the script is launched, the main menu presents several options:
        MENU

    1- List of SDG Goals and Targets
    2- List and Codes of Geographic Areas (GeA)
    3- List of SDG Series
    4- Find the Value of an Indicator for a Country or a GeA
      

*Choose an option between `(1-4)`,  allowing you to:* 

   

### Option 1- List of SDG Goals and Targets :
*Example of lists of **SDG goals** and **targets:***

      List of SDG Goals and Targets
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      | N° | Goal code | Goal title          | Target code   | Target title                                                  |
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      |  1 | 1         | End poverty in all  | 1.1           | By 2030, eradicate extreme poverty for all people everywhere, |
      |    |           | its forms everywhere|               | currently measured as people living on less than $1.25 a day  |
      +----+-----------+---------------------+---------------+---------------------------------------------------------------+
      ...


### Option 2- List and Code of Areas :
*Example of **geographical areas** and **codes** lists*

      List of SDG Geographic Areas
      +-------------+-------------------------------------------------------------+
      | geoAreaCode | geoAreaName                                                 |
      +-------------+-------------------------------------------------------------+
      |  4          | Afghanistan                                                 |
      +-------------+-------------------------------------------------------------+
      |  248        | Åland Islands                                               |
      +-------------+-------------------------------------------------------------+      
      ...


### Option 3- List of SDG Series :
*Example of lists of **SDG Series***

      List of SDG Series
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
### Option 4- Find the Value of an Indicator for a Country or zone:
#### Find the value of the SDG indicator : 
1. Once option `4` is entered and confirmed, the `terminal` or `CLI` displays :

         Name of geographic area / Area code: 
   You are invited to provide the `geoAreaName` or the `geoAreaCode` of the area for which you are seeking **SDG information** *(eg: Benin or 204)*.
2. The prompt then asks to provide the **indicator code** *(eg: 1.1.1)*:

         Indicator code (#.#.#): 
3. Finally, you get the information form the [official API](https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data)
      
         Indicator N° 11.a.1 for Afghanistan (4)
         +--------+----------+-------------+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+---------------+---------------+-------------------+---------+-------------+---------------+----------------+--------------+--------------+--------------+-----------------+--------------+---------------------------------------------------------------------+-----------------+-------------------------+
         | goal   | target   | indicator   | series       | seriesDescription                                                                                                                                                                                         |   seriesCount |   geoAreaCode | geoAreaName   |   timePeriodStart |   value | valueType   | time_detail   | timeCoverage   | upperBound   | lowerBound   | basePeriod   | source          | geoInfoUrl   | footnotes                                                           | attributes      | dimensions              |
         +========+==========+=============+==============+===========================================================================================================================================================================================================+===============+===============+===============+===================+=========+=============+===============+================+==============+==============+==============+=================+==============+=====================================================================+=================+=========================+
         | ['11'] | ['11.a'] | ['11.a.1']  | SD_CPA_UPRDP | Countries that have national urban policies or regional development plans that respond to population dynamics; ensure balanced territorial development; and increase local fiscal space (1 = YES; 0 = NO) |           265 |             4 | Afghanistan   |              2020 |       1 | Float       |               |                |              |              |              | NUP 2020 Status |              | ['UN-Habitat Global Survey on National Urban Policies 2018 & 2020'] | {'Nature': 'C'} | {'Reporting Type': 'G'} |
         +--------+----------+-------------+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+---------------+---------------+-------------------+---------+-------------+---------------+----------------+--------------+--------------+--------------+-----------------+--------------+---------------------------------------------------------------------+-----------------+-------------------------+
         Would you want to export in CSV file? (y/n): 

#### Export data to CSV :
   *You can choose to export the retrieved data as a `CSV` file or not.
The file will be saved with the following name :*

      <geographical_area_name>_<indicator_code>.csv
You can open it with *MS Excel* or *Numbers* to work on it.
## Licence :

This project is under an [`Unlicense`](UNLICENSE.txt) , developed by [MnserX](https://github.com/MnserXiapeace) 


