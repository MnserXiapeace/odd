# Importing all functions and variables from the module 'odd'
# and the libraries 'requests', 'textwrap'

from project import *
import requests
import textwrap
import io
import sys
from tabulate import tabulate


# Test of the function get_sdg_goals_and_targets
def test_get_sdg_goals_and_targets():
    # Direct API Call to Retrieve the Raw Response
    response = requests.get("https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Goal/List?includechildren=true")
    list_goals_targets = []

    if response.status_code == 200:
        data = response.json()
        numerous = 0

        if data:
            for goal in data:
                for target in goal["targets"]:
                    goal_target = {}
                    numerous += 1
                    goal_target["No."] = numerous
                    goal_target["Goal Code"] = goal["code"]
                    goal_target["Goal Title"] = '\n'.join(
                        textwrap.wrap(goal["title"], width=20))  # Line break every 20 characters.
                    goal_target["Target Code"] = target["code"]
                    goal_target["Target Title"] = '\n'.join(textwrap.wrap(target["title"], width=20))
                    list_goals_targets.append(goal_target)

            # Compare the results of the function with those processed locally
            assert get_sdg_goals_and_targets() == tuple(list_goals_targets)
        else:
            # If the data returned by the API is empty
            assert False, "The data returned by the API is empty."
    else:
        # If the API does not respond correctly, the test fails
        assert False, f"Error API {response.status_code} : {response.text}"


# Test of the function get_geographic_areas
def test_get_geographic_areas():
    # Direct API Call to Retrieve the Raw Response
    reponse = requests.get('https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/GeoArea/List')

    if reponse.status_code == 200:
        list_geo_area_api = reponse.json()

        # We perform the same processing on the raw response as the function get_geographic_areas
        for dico_area in list_geo_area_api:
            dico_area['geoAreaName'] = '\n'.join(textwrap.wrap(dico_area['geoAreaName'], width=30))

        # Check that the function returns the same data after processing
        assert get_geographic_areas() == list_geo_area_api
    else:
        # If the API does not respond correctly, we fail the test
        assert False, f"Error API {reponse.status_code} : {reponse.text}"


# Test of the function get_geographic_area_code
# We test different country names with leading and trailing spaces,
# and verify that `fetch_area_code` returns the correct codes.
def test_get_geographic_area_code():
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


# Test of the function get_sdg_series
def test_get_sdg_series():
    # Direct API call to retrieve the raw response
    response = requests.get("https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Indicator/List")
    list_indi_series = []
    nmerous = 0

    if response.status_code == 200:
        list_indicators = response.json()

        # Apply the same processing as in the 'get_sdg_series' function
        for indicator in list_indicators:
            for series in indicator["series"]:
                nmerous += 1
                serie = {"Number": nmerous, "Series Code": series["code"],
                         "Description": '\n'.join(textwrap.wrap(series["description"], 50)),
                         "Goal": ", ".join(series["goal"]), "Targets": ", ".join(series["target"]),
                         "Indicators": ", ".join(series["indicator"]), "Version": series["release"]}
                list_indi_series.append(serie)

        # Compare the function's results with those processed locally
        assert get_sdg_series() == list_indi_series
    else:
        # If the API does not respond correctly, we fail the test
        assert False, f"Error API {response.status_code} : {response.text}"


# Test of the function 'get_indicator_data'
def test_get_indicator_data():
    # We verify that the function fetch_indicator_data returns the same data as the API request for various
    # indicators and area codes.
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


# Test of the function display_goals_and_targets
def test_display_goals_and_targets():
    # Capture the standard output (the print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Call of the function that must print
    display_goals_and_targets()

    # Retrieve the data from the API for comparison
    expected_data = get_sdg_goals_and_targets()

    if expected_data:
        # Create the expected output in table form using tabulate
        expected_output = "\nList of SDG Goals and Targets\n" + tabulate(expected_data, headers="keys",
                                                                             tablefmt="grid") + "\n"

        # Compare the captured output with the expected output
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Error in retrieving goals and targets data"

    # Restore stdout to its normal state
    sys.stdout = sys.__stdout__


# Test of the function display_sdg_series
def test_display_sdg_series():
    # Capture the standard output (the print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Call of the function that must print
    display_sdg_series()

    # Retrieve the data from the API for comparison
    expected_data = get_sdg_series()

    if expected_data:
        # Create the expected output in table form using tabulate
        expected_output = "\nList of SDG Series\n" + tabulate(expected_data, headers="keys", tablefmt="grid") + "\n"

        # Compare the captured output with the expected output
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Error in retrieving ODD series"

    # Restore stdout to its normal state.
    sys.stdout = sys.__stdout__


# Test of the function display_geographic_areas
def test_display_geographic_areas():
    # Capture the standard output (the print)
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Call of the function that must print.
    display_geographic_areas()

    # Retrieve the data from the API for comparison
    expected_data = get_geographic_areas()

    if expected_data:
        # Create the expected output in table form using tabulate
        expected_output = "\nList of SDG Geographic Areas\n" + tabulate(expected_data, headers="keys",
                                                                             tablefmt="grid") + "\n"

        # Compare the captured output with the expected output
        assert captured_output.getvalue() == expected_output
    else:
        assert False, "Error in retrieving geographical areas"

    # Restore stdout to its normal state.
    sys.stdout = sys.__stdout__


if __name__ == '__main__':
    test_get_geographic_areas()
    test_get_indicator_data()
    test_get_sdg_series()
    test_get_geographic_area_code()
    test_get_sdg_goals_and_targets()
    test_display_sdg_series()
    test_display_geographic_areas()
    test_display_goals_and_targets()

