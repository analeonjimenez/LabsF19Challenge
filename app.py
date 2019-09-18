from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv() # loading API key as stored in .env

building_dict = {} # the name-key dictionary for each building
AUTH = "?auth_token=" + os.getenv("API_KEY") # API key
URL_LATEST = "http://density.adicu.com/latest" # API for accessing latest data of all buildings
URL_BUILDING = "http://density.adicu.com/latest/building/" # API for accessing latest data of a certain building


# scans data from current and connected urls
def get_building_info(url):
    building_info = []
    while (True):
        buildings = requests.get(url + AUTH).json()
        building_info.extend(buildings['data'])
        if ('next_page' not in list(buildings.keys())): break;
        url = buildings['next_page']

    return building_info


# before each request, scans building list and generates name-key dictionary
@app.before_request
def get_building_keys():
    if (len(building_dict) > 0): return

    buildings = get_building_info(URL_LATEST)
    for building in buildings:
        building_name = building['building_name'].strip().lower()
        if (building_name not in list(building_dict.keys())):
            if (' ' in building_name):
                building_name = building_name.replace(' ', '_')
            building_dict[building_name] = building['parent_id']


# render information about a certain building
@app.route('/information/<string:building_name>', methods=['GET'])
def print_buildings(building_name):
    building_name_std = building_name.strip().lower()
    # catching key error (the user input is not part of the listed buildings)
    try:
        queried_building = get_building_info(URL_BUILDING + str(building_dict[building_name_std]))
    except:
        return "building " + building_name + " not found :("

    return render_template('building_page.html', buildings = queried_building, title = building_name + " information")


# render list of k emptiest places
@app.route('/information/<int:k>', methods=['GET'])
def print_k_emptiest(k):
    buildings = get_building_info(URL_LATEST)
    buildings.sort(key = lambda x : x['percent_full'])
    return render_template('building_page.html', buildings = buildings[:k], title = str(k) + " emptiest places")


# saying hi
@app.route('/information')
def print_all_buildings():
    return "hi, this is Yuanyuting Wang's ADI Lab Technical Challenge project :)"


if __name__ == '__main__':
    app.run()
