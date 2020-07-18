# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 00:04:29 2020

@author: anhtr
"""
import Traffic_Reader as tr

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol_1 = mydb["traffic_flow_2018"]
mycol_1_1 = mydb["traffic_flow_2016"]
mycol_1_2 = mydb["traffic_flow_2017"]

reader_1 = tr.Traffic_Reader('Traffic_Volumes_for_2018.csv')
reader_1_1 = tr.Traffic_Reader('TrafficFlow2016_OpenData.csv')
reader_1_2 = tr.Traffic_Reader('2017_Traffic_Volume_Flow.csv')
x_1 = mycol_1.insert_many(reader_1.compile())
x_1_1 = mycol_1_1.insert_many(reader_1_1.compile())
x_1_2 = mycol_1_2.insert_many(reader_1_2.compile())
print(x_1.inserted_ids, x_1_1.inserted_ids, x_1_2.inserted_ids)

mycol_2 = mydb["traffic_indicents"]
reader_2 = tr.Traffic_Reader('Traffic_Incidents.csv')
x_2 = mycol_2.insert_many(reader_2.compile())
print(x_2.inserted_ids)