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


# Save folium map to image and html
def save_to_img(m, file_name):
    img_data = m._to_png(10)
    img = Image.open(io.BytesIO(img_data))
    img.save(file_name)
    html_img = file_name.split(".")
    m.save(html_img[0] + ".html")


# Find where center of the map should be
def find_midpoint(coordinates_list):
    n = len(coordinates_list)
    x = 0
    y = 0
    for coord in coordinates_list:
        x += coord[0] / n
        y += coord[1] / n
    return (x, y)


def add_markers(m, coordinates_list):
    for coord in coordinates_list:
        folium.Marker(coord).add_to(m)


def test():
    info = []
    f = open('credentials')
    lines = f.readlines()
    user = lines[0]
    password = lines[1]
    database = lines[2]

    myclient = pymongo.MongoClient('mongodb+srv://' + user.rstrip('\n') + ':' + password.rstrip(
        '\n') + '@cluster0.oyu7v.mongodb.net/' + database + '?retryWrites=true&w=majority')
    mydb = myclient["calgary_traffic"]

    q_incidents = DBQuery(mydb, type='incident')
    c_incidents_16 = q_incidents.get_coordinates(year='2016')
    c_incidents_17 = q_incidents.get_coordinates(year='2017')
    c_incidents_18 = q_incidents.get_coordinates(year='2018')

    q_flow_16 = DBQuery(mydb)
    c_flow_16 = q_flow_16.get_coordinates()
    q_flow_17 = DBQuery(mydb, year='2017')
    c_flow_17 = q_flow_17.get_coordinates()
    q_flow_18 = DBQuery(mydb, year='2018')
    c_flow_18 = q_flow_18.get_coordinates()

    m_incidents_16 = folium.Map(location=find_midpoint(c_incidents_16), zoom_start=13)
    add_markers(m_incidents_16, c_incidents_16)
    m_incidents_16.save('incidents_2016.html')

    m_incidents_17 = folium.Map(location=find_midpoint(c_incidents_17), zoom_start=13)
    add_markers(m_incidents_17, c_incidents_17)
    m_incidents_17.save('incidents_2017.html')

    m_incidents_18 = folium.Map(location=find_midpoint(c_incidents_18), zoom_start=13)
    add_markers(m_incidents_18, c_incidents_18)
    m_incidents_18.save('incidents_2018.html')

    mid_flow_16 = find_midpoint(c_flow_16)
    mid_flow_17 = find_midpoint(c_flow_17)
    mid_flow_18 = find_midpoint(c_flow_18)

    m_flow_16 = folium.Map(location=mid_flow_16, zoon_start=13)
    add_markers(m_flow_16, c_flow_16)
    m_flow_16.save('traffic_2016.html')

    m_flow_17 = folium.Map(location=mid_flow_17, zoom_start=13)
    add_markers(m_flow_17, c_flow_17)
    m_flow_17.save('traffic_2017.html')

    m_flow_18 = folium.Map(location=mid_flow_18, zoom_start=13)
    add_markers(m_flow_18, c_flow_18)
    m_flow_18.save('traffic_2018.html')


if __name__ == '__main__':
    test()
