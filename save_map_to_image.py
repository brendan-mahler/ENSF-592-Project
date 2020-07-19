# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:23:55 2020

@author: anhtr
"""


import folium
import pymongo
from database_query import *
import io
from PIL import Image


def save_to_img(m, file_name):
    img_data = m._to_png(10)
    img = Image.open(io.BytesIO(img_data))
    img.save(file_name)


def find_midpoint(coordinates_list):
    n = len(coordinates_list)
    x = 0
    y = 0
    for coord in coordinates_list:
        x += coord[0]/n
        y += coord[1]/n
    return (x,y)

def add_markers(m, coordinates_list):
    for coord in coordinates_list:
        folium.Marker(coord).add_to(m)

def test():
    secret = open('confidentials.txt')
    info = []
    for line in secret:
        info.append(line.strip())
    myclient = pymongo.MongoClient("mongodb+srv://"+info[1]+":"+info[0]+"@cluster0.oyu7v.mongodb.net/"+info[2]+"?retryWrites=true&w=majority")
    mydb = myclient["calgary_traffic"]
    """
    q_incidents = DBQuery(mydb,type='incident') 
    c_incidents_16 = q_incidents.get_coordinates(year='2016')
    c_incidents_17 = q_incidents.get_coordinates(year='2017')
    c_incidents_18 = q_incidents.get_coordinates(year='2018')
    """
    q_flow_16 = DBQuery(mydb)
    c_flow_16 = q_flow_16.get_coordinates()
    q_flow_17 = DBQuery(mydb,year='2017')
    c_flow_17 = q_flow_17.get_coordinates()
    q_flow_18 = DBQuery(mydb,year='2018')
    c_flow_18 = q_flow_18.get_coordinates()
    """
    m_incidents_16 = folium.Map(location=find_midpoint(c_incidents_16),zoom_start=13)
    add_markers(m_incidents_16,c_incidents_16)
    save_to_img(m_incidents_16,'incidents_2016.png')
    
    m_incidents_17 = folium.Map(location=find_midpoint(c_incidents_17),zoom_start=13)
    add_markers(m_incidents_17,c_incidents_17)
    save_to_img(m_incidents_17,'incidents_2017.png')
    
    m_incidents_18 = folium.Map(location=find_midpoint(c_incidents_18),zoom_start=13)
    add_markers(m_incidents_18,c_incidents_18)
    save_to_img(m_incidents_18,'incidents_2018.png')
    """
    mid_flow_16 = find_midpoint(c_flow_16)
    mid_flow_17 = find_midpoint(c_flow_17)
    mid_flow_18 = find_midpoint(c_flow_18)
    
    
    m_flow_16 = folium.Map(location=mid_flow_16,zoon_start=13)
    add_markers(m_flow_16,c_flow_16)
    save_to_img(m_flow_16,'traffic_2016.png')
    
    m_flow_17 = folium.Map(location=mid_flow_17,zoom_start=13)
    add_markers(m_flow_17,c_flow_17)
    save_to_img(m_flow_17,'traffic_2017.png')
    
    m_flow_18 = folium.Map(location=mid_flow_18,zoom_start=13)
    add_markers(m_flow_18,c_flow_18)
    save_to_img(m_flow_18,'traffic_2018.png')
         
    
if __name__ == '__main__':
    test()
          