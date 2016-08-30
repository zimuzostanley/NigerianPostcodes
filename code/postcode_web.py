from flask import Flask, request, url_for, render_template
import postcode_trie as pt
import json


locations, location_dict = pt.get_urban_postcodes_tuple_from_csv('../data/urban_postcodes.csv')
locations, location_dict = pt.get_rural_postcodes_tuple_from_csv('../data/rural_postcodes.csv', locations, location_dict)
trie = pt.build_trie(locations)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/postcodes')
def get_postcodes():
    street = request.args.get('term')
    if street is not None:
        if len(street) < 3:
            return json.dumps([])
        retrieved = pt.retrieve_by_prefix(trie, street)
        formatted = pt.format_result(retrieved, location_dict)
        if len(formatted) == 0:
            return json.dumps(['No postcode found'])
        return json.dumps(formatted)
    else:
        return json.dumps(['No location provided'])

if __name__ == '__main__':
    app.run()

