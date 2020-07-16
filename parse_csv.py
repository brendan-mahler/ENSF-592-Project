import csv
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['ENSF_592_Project-database']
traffic_data = db.Traffic


class Database:

    def insert_into_database(self, filename):

        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # header_list = []

            headers = next(csv_file)
            header = headers.split(',')

            for line in csv_reader:
                one_file = tuple(zip(header, line))
                dictionary = dict(one_file)
                input_data = traffic_data.insert_one(dictionary)
            if input_data.acknowledged:
                print("Successful Insertion")


    # def retrieve_data(self):
    #     data = traffic_data.find(
    #         { 'DESCRIPTION': "Eastbound Glenmore Trail at Centre Street SE"})
    #     print(data)


if __name__ == '__main__':
    first = Database()
    file = ['Traffic_Incidents.csv', 'Traffic_Incidents_Archive_2016.csv']

    for filename in file:
        first.insert_into_database(filename)

    # first.retrieve_data()
