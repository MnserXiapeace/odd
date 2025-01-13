# Import necessary libraries
import requests
import re
from tabulate import tabulate
import csv
import textwrap


# Main function to display the main menu and prompt user input
def main():
    """
    Displays the main menu and prompts the user to select an option
    among the SDG goals, targets, geographic areas, SDG series, or indicators for a country.
    """
    print(
        """
            MENU

    1- List of SDG Goals and Targets
    2- List and Codes of Geographic Areas (GeA)
    3- List of SDG Series
    4- Find the Value of an Indicator for a Country or a GeA
        """
    )
    handle_user_choice()


# Data retrieval functions section

# Function to retrieve and display SDG goals and targets
def get_sdg_goals_and_targets():
    """
    Retrieves and returns the list of SDG goals and targets via the UN API.
    Formats the data by adding line breaks for long titles.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Goal/List?includechildren=true"
    response = requests.get(base_url)
    goals_targets_list = []

    if response.status_code == 200:
        data = response.json()
        number = 0

        if data:
            for goal in data:
                for target in goal["targets"]:
                    goal_target = {}
                    number += 1
                    goal_target["No."] = number
                    goal_target["Goal Code"] = goal["code"]
                    goal_target["Goal Title"] = '\n'.join(
                        textwrap.wrap(goal["title"], width=20))  # Line break every 20 characters
                    goal_target["Target Code"] = target["code"]
                    goal_target["Target Title"] = '\n'.join(textwrap.wrap(target["title"], width=20))
                    goals_targets_list.append(goal_target)
            return tuple(goals_targets_list)

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# Function to retrieve the list of geographic areas
def get_geographic_areas():
    """
    Retrieves the list of geographic areas via the UN API and formats the area names with line breaks.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List"
    response = requests.get(base_url)

    if response.status_code == 200:
        geo_area_list = response.json()
        for area_dict in geo_area_list:
            area_dict['geoAreaName'] = '\n'.join(textwrap.wrap(area_dict['geoAreaName'], width=30))
        return geo_area_list
    else:
        print(f"Error {response.status_code} : {response.text}")
        return None


# Function to retrieve the geographic area code based on the country name
def get_geographic_area_code(country_name: str):
    """
    Retrieves the geographic area code for a given country name via the UN API.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List"
    response = requests.get(base_url)

    if response.status_code == 200:
        geo_area_list = response.json()
        country_name = country_name.strip()

        for geo_area in geo_area_list:
            if country_name == geo_area["geoAreaName"]:
                return str(geo_area["geoAreaCode"])

        print("Invalid country name")
    else:
        print(f"Error {response.status_code} : {response.text}")
        return str(1)


# Function to retrieve indicator data for a given geographic area
def get_indicator_data(indicator_code: str, area_code: str):
    """
    Retrieves specific indicator data for a given geographic area via the UN API.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/Data"
    params = {
        "indicator": indicator_code,
        "areaCode": area_code,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code} : {response.text}")
        return None


# Function to retrieve the list of SDG series
def get_sdg_series():
    """
    Retrieves and returns the list of SDG indicator series via the UN API.
    """
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/List"
    response = requests.get(base_url)
    sdg_series_list = []
    global number
    number = 0

    if response.status_code == 200:
        indicators_list = response.json()

        for indicator in indicators_list:
            for series in indicator["series"]:
                number += 1
                serie = {}
                serie["Number"] = number
                serie["Series Code"] = series["code"]
                serie["Description"] = '\n'.join(textwrap.wrap(series["description"], 50))
                serie["Goal"] = ", ".join(series["goal"])
                serie["Targets"] = ", ".join(series["target"])
                serie["Indicators"] = ", ".join(series["indicator"])
                serie["Version"] = series["release"]
                sdg_series_list.append(serie)
        return sdg_series_list
    else:
        print(f"Error {response.status_code} : {response.text}")
        return None


# Display functions section

# Function to display the list of SDG goals and targets
def display_goals_and_targets():
    """
    Displays the list of SDG goals and targets in a table format.
    """
    print("\nList of SDG Goals and Targets")
    print(tabulate(get_sdg_goals_and_targets(), headers="keys", tablefmt="grid"))


# Function to display the list of SDG series
def display_sdg_series():
    """
    Displays the list of SDG series in a table format.
    """
    print("\nList of SDG Series")
    print(tabulate(get_sdg_series(), headers="keys", tablefmt="grid"))


# Function to display the list of geographic area codes
def display_geographic_areas():
    """
    Displays the list of geographic areas and their codes in a table format.
    """
    print("\nList of SDG Geographic Areas")
    print(tabulate(get_geographic_areas(), headers="keys", tablefmt="grid"))


# User interaction functions section

# Function to remove unnecessary columns
def remove_unnecessary_columns(dict_list: list):
    """
    Removes unnecessary items (column in tabulate) from a list of dictionaries.
    """
    new_list = []
    keys_to_remove = ['goal', 'target', 'geoAreaCode', 'geoAreaName', 'valueType', 'time_detail', 'upperBound',
                      'lowerBound', 'geoInfoUrl']
    for element_dict in dict_list:
        new_dict = {k: v for k, v in element_dict.items() if k not in keys_to_remove}
        new_list.append(new_dict)
    return new_list


# Function to find an SDG indicator value for a country
def find_country_indicator_value():
    """
    Allows finding an SDG indicator value for a given geographic area by interacting with the user.
    """
    areas = [geo_area["geoAreaName"] for geo_area in get_geographic_areas()]
    area_codes = [geo_area["geoAreaCode"] for geo_area in get_geographic_areas()]

    while True:
        try:
            pattern = r"^([1-9]{1,2}|10)\.([1-9]{1,2}|[a-d]{1}|10)\.([1-9]{1,2})$"
            area = input("Name of geographic area / Area code: ").strip().title()
            indicator = input("Indicator code (#.#.#): ").strip()
            match = re.fullmatch(pattern, indicator, re.IGNORECASE)

            if (match is not None) and (area in areas or area in area_codes):
                area_code = area if area.isnumeric() else get_geographic_area_code(area)
                data = get_indicator_data(indicator, area_code)

                if len(data["data"]) > 0:
                    print(f"\nIndicator No. {indicator} for {data['data'][0]['geoAreaName']} ({data['data'][0]['geoAreaCode']})")
                    for d in data['data']:
                        d['seriesDescription'] = '\n'.join(textwrap.wrap(d['seriesDescription'], width=22))  # Formats and limits to 15 characters per line for better readability
                        d['source'] = '\n'.join(textwrap.wrap(d['source'], width=15))
                        d['footnotes'] = '\n'.join(textwrap.wrap(' '.join(d['footnotes']), width=20))

                        # Formats and limits dimensions to 15 characters per line for better readability
                        tab_of_dimensions = []
                        for element in d['dimensions']:
                            tab_of_dimensions.append(f'{element}: {d["dimensions"][element]}')
                        d['dimensions'] = '\n'.join(textwrap.wrap(' '.join(tab_of_dimensions), width=15))

                    filtered_data = remove_unnecessary_columns(data['data'])
                    print(tabulate(filtered_data, headers="keys", tablefmt="grid"))
                    export = input("Do you want to export to CSV? (y/n): ").strip().lower()[:1]
                    if export == "y":
                        export_to_csv(data["data"], data['data'][0]['geoAreaName'], indicator)
                        print("Successfully exported")

                    accept = input("Do you want to try again? (y/n): ").strip().lower()[:1]
                    if accept != "y":
                        break
                else:
                    print("Incorrect entry")
            else:
                continue
        except BaseException as e:
            print(e)
            break


# Function to export data to CSV file
def export_to_csv(dict_list: list, area_name: str, indicator: str):
    """
    Exports a list of dictionaries to a CSV file.
    """
    fieldnames = dict_list[0].keys()
    with open(f'{area_name}_{indicator}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        writer.writeheader()
        for dic in dict_list:
            writer.writerow(dic)


# Function that handles user choices from the menu
def handle_user_choice():
    """
    Handles the user's choice in the main menu and executes the corresponding actions.
    """
    while True:
        try:
            menu_choice = int(input("Choose an option (1-4): "))
            if menu_choice == 1:
                display_goals_and_targets()
                break
            elif menu_choice == 2:
                display_geographic_areas()
                break
            elif menu_choice == 3:
                display_sdg_series()
                break
            elif menu_choice == 4:
                find_country_indicator_value()
                break
            else:
                print("Invalid choice. Please choose between 1 and 4.")
        except ValueError:
            print("Invalid entry. Please enter a number.")


if __name__ == "__main__":
    main()
