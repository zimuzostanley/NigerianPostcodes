import csv
import urllib
import urllib2
import json
import copy

GMAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
GMAPS_API_KEY = 'AIzaSyCjZ0YSGy8g74tqMHmFhCbiXQQWUIgIQcg'
#AIzaSyDuX9RuGmHR3tRXOlxqbvrqfhaxXXEC624

def geocode_address(address):
    qs = urllib.urlencode({'address': address, 'key': GMAPS_API_KEY})
    response = urllib2.urlopen(GMAPS_GEOCODE_URL + qs)
    rhtml = response.read()
    rjson = json.loads(rhtml)
    try:
        temp = rjson['results'][0]['geometry']['location']
    except KeyError:
        return None, None
    return temp['lat'], temp['lng']

def geocode_file(csv_filename, csv_filename_write, offset):
    rows = []
    with open(csv_filename) as csv_file, open(csv_filename_write, 'a') as csv_file_write:
        reader = csv.DictReader(csv_file)
        writer_fieldnames = ['town', 'state', 'street', 'postcode', 'area', 'lat', 'lng']
        writer = csv.DictWriter(csv_file_write, fieldnames=writer_fieldnames)
        i = 0
        for row in reader:
            if i >= offset:
                address = row['street'] + ' ' + row['town'] + ' ' + row['state']
                print 'Geocoding adress: ' + address
                lat, lng = geocode_address(address)
                print 'Geocoded! Lat: ' + str(lat) + '. Lng: ' + str(lng)
                print str(i)
                if lat is not None and lng is not None:
                    row['lat'] = lat
                    row['lng'] = lng
                    writer.writerow(row)
            i = i + 1
    return rows
    
def write_csv(csv_filename, rows):
    pass
                    
#print geocode_address('Onitsha,Anambra Jagwa St')
geocode_file('../data/urban_postcodes.csv', '../data/urban_postcodes_lat.csv', 941)
