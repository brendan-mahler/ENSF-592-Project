import operator
import pandas as pd
import pymongo


class data:
    client = pymongo.MongoClient(
        'mongodb+srv://dbuser:592project@cluster0.oyu7v.mongodb.net/calgary_traffic?retryWrites=true&w=majority')
    username = "dbuser"
    password = "592project"
    database = "calgary_traffic"
    db = client['calgary_traffic']
    traffic_2018 = db['traffic_volume_2018']
    traffic_2017 = db['traffic_volume_2017']
    traffic_2016 = db['traffic_volume_2016']
    accidents = db['traffic_incidents']

    volume_2018 = traffic_2018.find({"YEAR": 2018}, {"VOLUME"})
    volume_2017 = traffic_2017.find({"year": 2017}, {"volume"})
    volume_2016 = traffic_2016.find({"year_vol": 2016}, {"volume"})

    rows_2016 = traffic_2016.find().limit(50)
    rows_2017 = traffic_2017.find().limit(50)
    rows_2018 = traffic_2018.find().limit(50)
    accident_rows = accidents.find().limit(50)

    sorted_rows_2016 = traffic_2016.find().sort('volume', -1).limit(50)
    sorted_rows_2017 = traffic_2017.find().sort('volume', -1).limit(50)
    sorted_rows_2018 = traffic_2018.find().sort('VOLUME', -1).limit(50)
    sorted_accident_rows = accidents.find().sort('INCIDENT INFO', -1).limit(50)





