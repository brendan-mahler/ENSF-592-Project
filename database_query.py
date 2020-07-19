# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:42:28 2020

@author: anhtr
"""
import string
import pandas as pd
import pymongo
import operator

class DBQuery(dict):
    def __init__(self, database, type='volume', year='2016'):
        self.headers = []
        if type == 'volume':
            if year == '2016':
                collection = database["traffic_volume_2016"]
                self.headers = ['secname','the_geom','year_vol','shape_leng','volume']
            elif year == '2017':
                collection = database["traffic_volume_2017"]
                self.headers = ['year','segment_name','the_geom','length_m','volume']
            else:
                collection = database["traffic_volume_2018"]
                self.headers = ['YEAR','SECNAME','Shape_Leng','VOLUME','multilinestring']
        else:
            collection = database["traffic_incidents"]
            self.headers = ['INCIDENT INFO','DESCRIPTION','START_DT','MODIFIED_DT','QUADRANT','Longitude','Latitude','location','Count','id']
        read_table = collection.find({},{'_id':0})
        dictionary = collection.find_one()
        for key in dictionary.keys():
            self[key] = []
        for x in read_table:
            self.count(x)
    
    def data_frame(self):
        return pd.DataFrame(self)
            
    def count(self, dictionary):
        strippables = string.ascii_letters + string.whitespace + '()\'\"'
        for key in dictionary.keys():
            if key == 'the_geom' or key == 'multilinestring':
                coordinate_list = dictionary[key].strip(strippables).split(',')
                location_list = []
                for coordinates in coordinate_list:
                    num = coordinates.split()
                    tp = (float(num[1].strip(strippables)), float(num[0].strip(strippables)))
                    location_list.append(tp)
                self[key].append(location_list)
            elif 'volume' in key.lower() or key.lower() == 'count':
                self[key].append(int(dictionary[key]))
            elif key.lower() == 'latitude' or key.lower() == 'longitude':
                self[key].append(float(dictionary[key]))
            else: self[key].append(dictionary[key])
        
    #Returns value(s) to be used to draw plot
    def total_max(self):
        amount = 0
        amount_list = [0, 0, 0]
        for key in self.keys():
            if 'volum' in key.lower():
                amount = max(self[key])
                return amount
            elif key.lower() == 'count':
                for i in range(len(self[key])):
                    if '2016' in self['START_DT'][i]: amount_list[0] += self[key][i]
                    elif '2017' in self['START_DT'][i]: amount_list[1] += self[key][i]
                    elif '2018' in self['START_DT'][i]: amount_list[2] += self[key][i]
                return amount_list
        return amount
    
    def get_incident_info(self,year='2016'):
        dict_unique = {}
        for i in range(len(self['INCIDENT INFO'])):
            if year in self['START_DT'][i]:
                dict_unique[self['INCIDENT INFO'][i]] = dict_unique.get(self['INCIDENT INFO'][i],0)+int(self['Count'][i])
        return dict_unique

    def max_accident(self, year='2020'):
        dict_unique = self.get_incident_info(year=year)
        max_count = max(dict_unique.items(), key=operator.itemgetter(1))
        return max_count
            
    def sort_incident_info(self,year='2016'):
        dict_unique = self.get_incident_info(year=year)
        new_dict = {k:v for k,v in sorted(dict_unique.items(), key=lambda item:item[1],reverse=True)}
        return new_dict
        
    def get_coordinates(self, year='2016'):
        list_coordinates = []
        headers = list(self.keys())
        for i in range(len(headers)):
            key = headers[i]
            if key.lower() == 'latitude':
                incident_info = self.get_incident_info(year=year)
                highest_accident_count = max(incident_info.items(), key=operator.itemgetter(1))[1]
                for i in range(len(self['INCIDENT INFO'])):
                    if  year in self['START_DT'][i]:
                        if incident_info[self['INCIDENT INFO'][i]]==highest_accident_count:
                            tp = (self['Latitude'][i],self['Longitude'][i])
                            list_coordinates.append(tp)
                break
            elif key == 'the_geom':
                data = self[key]
                list_coordinates = data[self['volume'].index(max(self['volume']))]
                break
            elif key == 'multilinestring':
                list_coordinates = self[key][self['VOLUME'].index(max(self['VOLUME']))]
                break
        return list_coordinates
#This function inquire the 'traffic_indicents' collection for year match
def find_year(collection, year='', limit=1):
    return collection.find({"START_DT":{"$regex":year}}).limit(limit)

def test():
    secret = open('confidentials.txt')
    info = []
    for line in secret:
        info.append(line.strip())
    myclient = pymongo.MongoClient("mongodb+srv://"+info[1]+":"+info[0]+"@cluster0.oyu7v.mongodb.net/"+info[2]+"?retryWrites=true&w=majority")
    mydb = myclient["calgary_traffic"]
    print(mydb.list_collection_names())
    query = DBQuery(mydb,type='incident')      
    print(query.get_coordinates(year='2016'))
    
if __name__ == '__main__':
    test()
                