# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:42:28 2020

@author: anhtr
"""
import string

import pymongo

class DBQuery(dict):
    def __init__(self, database, type='volume', year='2016'):
        col_year = ''
        if type == 'volume':
            if year == '2016':
                collection = database["traffic_flow_2016"]
            elif year == '2017':
                collection = database["traffic_flow_2017"]
            else:
                collection = database["traffic_flow_2018"]
        else:
            collection = database["traffic_indicents"]
        read_table = collection.find({},{'_id':0})
        dictionary = collection.find_one()
        for key in dictionary.keys():
            self[key] = []
        for x in read_table:
            self.count(x)
            
    def count(self, dictionary):
        strippables = string.ascii_letters + string.whitespace + '()\'\"'
        for key in dictionary.keys():
            if key == 'the_geom' or key == 'multilinestring':
                coordinate_list = dictionary[key].strip(strippables).split(',')
                location_list = []
                for coordinates in coordinate_list:
                    num = coordinates.split()
                    tp = (float(num[0].strip(strippables)), float(num[1].strip(strippables)))
                    location_list.append(tp)
                self[key].append(location_list)
            elif key.lower() == 'volume' or key.lower() == 'count':
                self[key].append(int(dictionary[key]))
            elif key.lower() == 'latitude' or key.lower() == 'longitude':
                self[key].append(float(dictionary[key]))
            else: self[key].append(dictionary[key])
        
    #Returns value(s) to be used to draw plot
    def total_max(self):
        amount = 0
        amount_list = [0, 0, 0]
        for key in self.keys():
            if key.lower() == 'volume':
                amount = max(self[key])
                return amount
            elif key.lower() == 'count':
                for i in range(len(self[key])):
                    if '2016' in self['START_DT'][i]: amount_list[0] += self[key][i]
                    elif '2017' in self['START_DT'][i]: amount_list[1] += self[key][i]
                    elif '2018' in self['START_DT'][i]: amount_list[2] += self[key][i]
                return amount_list
        return amount
        
    def get_coordinates(self, num=None):
        list_coordinates = []
        headers = list(self.keys())
        for i in range(len(headers)):
            key = headers[i]
            if key.lower() == 'latitude':
                tmp = zip(self[key], self[headers[i+1]])
                return tmp
            if key == 'the_geom' or key == 'multilinestring':
                for coord_list in self[key][:num]:
                    for coord in coord_list:
                        list_coordinates.append(coord)
                break
        return list_coordinates
#This function inquire the 'traffic_indicents' collection for year match
def find_year(collection, year='', limit=1):
    return collection.find({"START_DT":{"$regex":year}}).limit(limit)

def test():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    query_test = DBQuery(mydb, year='2018')
    query = DBQuery(mydb,type='incidents')      
    print(query_test.total_max(), query.total_max())
    
if __name__ == '__main__':
    test()
                