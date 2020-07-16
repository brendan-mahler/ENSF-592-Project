
import pymongo
import string

client = pymongo.MongoClient('localhost', 27017)
db = client['ENSF592_Project']
location = db.Files

s = location.find_one({'year': 2017},{'the_geom'})
s = s.get('the_geom')


s.strip()
strippables = string.ascii_letters + '()' + string.whitespace
s2 = s.strip(strippables)
coordinates_pairs = s2.split(',')
coordinates_list = []
for coordinates in coordinates_pairs:
    coord_str = coordinates.split()
    coordinates_list.append((float(coord_str[1]), float(coord_str[0])))
print(coordinates_list)