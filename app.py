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
        # if returned information contains key "next_page",
        # repeats this process for the connected url
        url = buildings['next_page']

    return building_info

# before each request, scans building list and generates name-key dictionary
@app.before_request
def get_building_keys():
    # core function should only be executed once
    if (len(building_dict) > 0): return

    buildings = get_building_info(URL_LATEST)
    for building in buildings:
        # convert all building names to lowercase with "_" in place of " "
        building_name = building['building_name'].strip().lower()
        if (building_name not in list(building_dict.keys())):
            if (' ' in building_name):
                building_name = building_name.replace(' ', '_')
            building_dict[building_name] = building['parent_id']

# render information about a certain building
@app.route('/information/<string:building_name>', methods=['GET'])
def print_buildings(building_name):
    building_name_std = building_name.strip().lower()
    # query building information by looking up its building key
    queried_building = get_building_info(URL_BUILDING + str(building_dict[building_name_std]))
    return render_template('building_page.html', buildings = queried_building, title = building_name + " information")

# render list of k emptiest places
@app.route('/information/<int:k>', methods=['GET'])
def print_k_emptiest(k):
    buildings = get_building_info(URL_LATEST)
    # sort and render first k elements
    buildings.sort(key = lambda x : x['percent_full'])
    return render_template('building_page.html', buildings = buildings[:k], title = str(k) + " emptiest places")

# render information about all buildings for reference
@app.route('/information', methods=['GET'])
def print_all_buildings():
    buildings = get_building_info(URL_LATEST)
    return render_template('building_page.html', buildings = buildings, title = "study places @ columbia")

@app.route('/', methods = ['GET'])
def main():
    r = requests.get("https://density.adicu.com/auth")
    return str(r)


if __name__ == '__main__':
    app.run()
