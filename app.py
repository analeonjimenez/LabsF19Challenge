from flask import Flask, render_template
import requests

app = Flask(__name__)

building_dict = {}
AUTH = "FQDYGZr3mDQ36ce7Rm405LhVO4xRwXx47EAM0LcHLZf2-zO7Gf9BoohK2w0o7cM6"

@app.before_request
def get_building_info():
    if (len(building_dict) > 0): return

    print('hiiiii')
    buildings = requests.get("http://density.adicu.com/latest?auth_token=" + AUTH).json()['data']
    for building in buildings:
        building_name = building['building_name'].strip().lower()
        if (building_name not in list(building_dict.keys())):
            if (' ' in building_name):
                building_name.replace(' ', '_')
            building_dict[building_name] = building['parent_id']
    print(building_dict.keys())

@app.route('/information/<string:building_name>', methods=['GET'])
def print_buildings(building_name):
    building_name = building_name.strip().lower()
    queried_building = requests.get("http://density.adicu.com/latest/building/" + str(building_dict[building_name]) + "?auth_token=" + AUTH).json()['data']
    return render_template('building_page.html', buildings = queried_building)

@app.route('/information/<int:k>', methods=['GET'])
def print_k_emptiest(k):
    buildings = requests.get("http://density.adicu.com/latest?auth_token=" + AUTH).json()['data']
    buildings.sort(key = lambda x : x['percent_full'])
    return render_template('building_page.html', buildings = buildings[:k])

@app.route('/', methods=['GET'])
def main():
    # buildings = requests.get("http://density.adicu.com/latest?auth_token=FQDYGZr3mDQ36ce7Rm405LhVO4xRwXx47EAM0LcHLZf2-zO7Gf9BoohK2w0o7cM6").json()['data']
    # # return render_template('building_page.html', buildings = buildings)
    # return str(buildings[0].keys())
    return str(len(building_dict))

if __name__ == '__main__':
    app.run()
