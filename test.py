import operator
import pandas as pd
import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://dbuser:592project@cluster0.oyu7v.mongodb.net/calgary_traffic?retryWrites=true&w=majority')

db = client['calgary_traffic']

traffic_2018 = db['traffic_volume_2018']
traffic_2017 = db['traffic_volume_2017']
traffic_2016 = db['traffic_volume_2016']

volume_2018 = traffic_2018.find({"YEAR": "2018"}, {"VOLUME"})
volume_2017 = traffic_2017.find({"year": "2017"}, {"volume"})
volume_2016 = traffic_2016.find({"year_vol": "2016"}, {"volume"})

#sorts the data by devreasing volume
def sort_table_by_volume(year):
    df = pd.DataFrame(list(year.find()))
    if year == traffic_2018:
        df['VOLUME'] = df['VOLUME'].astype(int)
        df = df.sort_values('VOLUME', ascending=False)
    else:
        df['volume'] = df['volume'].astype(int)
        df = df.sort_values('volume', ascending=False)
    print(df)

sort_table_by_volume(traffic_2017)
# Returns the index and corresponding highest volume
def highest_volume(year):
    sorted_v = {}
    index = 0
    if year == volume_2018:
        for volume in year:
            sorted_v.update({index: (volume["VOLUME"])})
            index += 1
    else:
        for volume in year:
            sorted_v.update({index: (volume["volume"])})
            index += 1
    sorted_v = sorted(sorted_v.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_v[0])


#highest_volume(volume_2017)
