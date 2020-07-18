# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 00:07:45 2020

@author: anhtr
"""
import string
import pandas as pd

class Traffic_Reader():
    
    def __init__(self,file_name):
        self.data_list = []
        self.headers = []
        data = pd.read_csv(file_name)
        for col in data.columns:
            self.headers.append(col)
        for index, rows in data.iterrows():
            self.data_list.append(rows.tolist())
      
    def compile(self):
        compiled_list = []
        for i in range(len(self.data_list)):
            entry = {}
            j = 0
            for header in self.headers:
                entry[header] = self.data_list[i][j]
                j += 1
            compiled_list.append(entry)
        return compiled_list
                

def test():
    reader = Traffic_Reader('Traffic_Volumes_for_2018.csv')
    print(reader.compile()[:3])
    reader2 = Traffic_Reader('TrafficFlow2016_OpenData.csv')
    print(reader2.compile()[:3])
    
if __name__ == '__main__':
    test()

    