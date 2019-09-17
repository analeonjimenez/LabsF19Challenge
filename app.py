from flask import Flask, render_template
import requests

app = Flask(__name__)

building_dict = {}
AUTH = "?auth_token=FQDYGZr3mDQ36ce7Rm405LhVO4xRwXx47EAM0LcHLZf2-zO7Gf9BoohK2w0o7cM6"
API_LATEST = "http://density.adicu.com/latest"
API_BUILDING = "http://density.adicu.com/latest/building/"

def get_building_info(url):
    building_info = []
    while (True):
        buildings = requests.get(url + AUTH).json()
        building_info.extend(buildings['data'])
        if ('next_page' not in list(buildings.keys())): break;
        url = buildings['next_page']
    return building_info


@app.before_request
def get_building_keys():
    if (len(building_dict) > 0): return

    buildings = get_building_info(API_LATEST)
    for building in buildings:
        building_name = building['building_name'].strip().lower()
        if (building_name not in list(building_dict.keys())):
            if (' ' in building_name):
                building_name.replace(' ', '_')
            building_dict[building_name] = building['parent_id']


@app.route('/information/<string:building_name>', methods=['GET'])
def print_buildings(building_name):
    building_name_std = building_name.strip().lower()
    queried_building = get_building_info(API_BUILDING + str(building_dict[building_name_std]))
    return render_template('building_page.html', buildings = queried_building, title = building_name + " information")


@app.route('/information/<int:k>', methods=['GET'])
def print_k_emptiest(k):
    buildings = get_building_info(API_LATEST)
    buildings.sort(key = lambda x : x['percent_full'])
    return render_template('building_page.html', buildings = buildings[:k], title = str(k) + " emptiest places")


@app.route('/', methods=['GET'])
def main():
    # buildings = requests.get("http://density.adicu.com/latest?auth_token=FQDYGZr3mDQ36ce7Rm405LhVO4xRwXx47EAM0LcHLZf2-zO7Gf9BoohK2w0o7cM6").json()['data']
    # # return render_template('building_page.html', buildings = buildings)
    # return str(buildings[0].keys())
    return str(len(building_dict))

if __name__ == '__main__':
    app.run()
