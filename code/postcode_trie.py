import marisa_trie as mt
import csv
import string


def get_urban_postcodes_tuple_from_csv(csv_filename, location=[], location_dict={}):
    with open(csv_filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if len(row['postcode']) != 6:
                continue
            location_dict[row['postcode'] + '-' + row['street'].lower()] = row['street'].lower() + ', ' \
                                                                           + row['area'].lower() + ', ' \
                                                                           + row['town'].lower() + ', ' \
                                                                           + row['state'].lower()
            location_dict[row['postcode'] + '-' + row['area'].lower()] = row['area'].lower() + ', ' \
                                                                         + row['town'].lower() + ', ' \
                                                                         + row['state'].lower()
            
            item = (unicode(row['street'].lower(), 'utf-8'), row['postcode'])
            location.append(item)
            item = (unicode(row['area'].lower(), 'utf-8'), row['postcode'])
            location.append(item)
    return location, location_dict


def get_rural_postcodes_tuple_from_csv(csv_filename, location=[], location_dict={}):
    with open(csv_filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if len(row['postcode']) != 6:
                continue
            location_dict[row['postcode'] + '-' + row['town'].lower()] = row['town'].lower() + ', ' + row['district'].lower() + ', ' + row['lga'].lower() + ', ' + row['state'].lower()
            location_dict[row['postcode'] + '-' + row['district'].lower()] = row['district'].lower() + ', ' + row['lga'].lower() + ', ' + row['state'].lower()
            
            item = (unicode(row['town'].lower(), 'utf-8'), row['postcode'])
            location.append(item)
            item = (unicode(row['district'].lower(), 'utf-8'), row['postcode'])
            location.append(item)
    return location, location_dict

def build_trie(locations):
    fmt = '<ssssss' #https://docs.python.org/3/library/struct.html#format-strings
    trie = mt.RecordTrie(fmt, locations)
    return trie

def retrieve_by_prefix(trie, prefix):
    return trie.items(prefix)

def format_result(pre_result, location_dict):
    result = []
    for pr in pre_result:
        postcode = string.join(pr[1]).replace(' ', '')
        other_address = location_dict.get(postcode + '-' + pr[0])
        print other_address
        if other_address is not None:
            result.append(other_address + ' - ' + postcode)
    return result

# locations, location_dict = get_postcodes_tuple_from_csv('../data/urban_postcodes.csv')

# trie = build_trie(locations)

# retrieved = retrieve_by_prefix(trie, 'zai')

# formatted = format_result(retrieved)

# for f in formatted:
#     print f




