# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:47:29 2020

@author: anhtr
"""
import random
import pymongo
from database_query import *
import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ScrollableFrame import *


# Parses table into GUI frame
def parse_to_frame(cur, headers):
    new_dict = {}
    for header in headers:
        new_dict[header] = []
    for row in cur:
        for header in headers:
            new_dict[header].append(row[header])
    return new_dict

#Sets the max amount of rows displayed
def limit(old_dict, num):
    new_dict = dict(old_dict)
    for key in old_dict.keys():
        n = len(old_dict[key])
        if n <= num:
            return new_dict
        for i in range(num, n, 1):
            new_dict[key].pop(num)
    return new_dict


# Read database credentials from txt file
f = open('credentials')
lines = f.readlines()
user = lines[0]
password = lines[1]
database = lines[2]

myclient = pymongo.MongoClient(
    'mongodb+srv://' + user.rstrip('\n') + ':' + password.rstrip(
        '\n') + '@cluster0.oyu7v.mongodb.net/' + database + '?retryWrites=true&w=majority')
mydb = myclient["calgary_traffic"]

# Volume collections
col_v_16 = mydb["traffic_volume_2016"]
col_v_17 = mydb["traffic_volume_2017"]
col_v_18 = mydb["traffic_volume_2018"]

# Create lsit of header names
h_v_16 = []
h_v_17 = []
h_v_18 = []
for key in col_v_16.find_one():
    if key == '_id': continue
    h_v_16.append(key)
for key in col_v_17.find_one():
    if key == '_id': continue
    h_v_17.append(key)
for key in col_v_18.find_one():
    if key == '_id': continue
    h_v_18.append(key)

# Parse volume data to frame
d_v_16 = parse_to_frame(col_v_16.find().limit(100), h_v_16)
d_v_17 = parse_to_frame(col_v_17.find().limit(100), h_v_17)
d_v_18 = parse_to_frame(col_v_18.find().limit(100), h_v_18)

# Parse sorted volume data to frame
d_v_16_s = parse_to_frame(col_v_16.find().sort('volume', -1).limit(100), h_v_16)
d_v_17_s = parse_to_frame(col_v_17.find().sort('volume', -1).limit(100), h_v_17)
d_v_18_s = parse_to_frame(col_v_18.find().sort('VOLUME', -1).limit(100), h_v_18)

# Get volume data
volume_2016 = DBQuery(mydb, year='2016')
volume_2017 = DBQuery(mydb, year='2017')
volume_2018 = DBQuery(mydb, year='2018')


# find the highest volume for a given year
m_v_16 = volume_2016.total_max()
m_v_17 = volume_2017.total_max()
m_v_18 = volume_2018.total_max()

# Get headers for incident table
col_a = mydb["traffic_incidents"]
h_a = []
for key in col_a.find_one():
    if key == '_id': continue
    h_a.append(key)


# Parse accident data to frame. Show first 100 rows
d_a_16 = parse_to_frame(col_a.find({'START_DT': {'$regex': '2016'}}).limit(100), h_a)
d_a_17 = parse_to_frame(col_a.find({'START_DT': {'$regex': '2017'}}).limit(100), h_a)
d_a_18 = parse_to_frame(col_a.find({'START_DT': {'$regex': '2018'}}).limit(100), h_a)

# Sort accident data. Show top 20 accident locations
traffic_accidents = DBQuery(mydb, type='accident')
d_a_16_s = limit(traffic_accidents.get_sorted_incident(year='2016'), 20)
d_a_17_s = limit(traffic_accidents.get_sorted_incident(year='2017'), 20)
d_a_18_s = limit(traffic_accidents.get_sorted_incident(year='2018'), 20)

# Get the max amount of accidents for a given year
m_a_16 = traffic_accidents.max_accident(year='2016')[1]
m_a_17 = traffic_accidents.max_accident(year='2017')[1]
m_a_18 = traffic_accidents.max_accident(year='2018')[1]


# Find Button
def b1CallBack():
    try:
        label2.configure(text='Executing...', bg='yellow')
        try:
            canvas.get_tk_widget().pack_forget()
        except:
            pass
        try:
            scrollable_frame.pack(fill='both', expand=True)
        except:
            pass
        scrollable_frame.clear()
        choice_1 = combo1.get()
        choice_2 = combo2.get()
        table = {}
        if choice_1 == 'Traffic Volume':
            if choice_2 == '2016':
                table = d_v_16
            elif choice_2 == '2017':
                table = d_v_17
            else:
                table = d_v_18
        else:
            if choice_2 == '2016':
                table = d_a_16
            elif choice_2 == '2017':
                table = d_a_17
            else:
                table = d_a_18
        scrollable_frame.add_table(table)
        label2.configure(text='Success', bg='green')
    except:
        label2.configure(text='Failure', bg='red')


# Sort button
def b2CallBack():
    try:
        label2.configure(text='Executing...', bg='yellow')
        try:
            canvas.get_tk_widget().pack_forget()
        except:
            pass
        try:
            scrollable_frame.pack(fill='both', expand=True)
        except:
            pass
        scrollable_frame.clear()
        choice_1 = combo1.get()
        choice_2 = combo2.get()
        table = {}
        if choice_1 == 'Traffic Volume':
            if choice_2 == '2016':
                table = d_v_16_s
            elif choice_2 == '2017':
                table = d_v_17_s
            else:
                table = d_v_18_s
        else:
            if choice_2 == '2016':
                table = d_a_16_s
            elif choice_2 == '2017':
                table = d_a_17_s
            else:
                table = d_a_18_s
        scrollable_frame.add_table(table)
        label2.configure(text='Success', bg='green')
    except:
        label2.configure(text='Failure', bg='red')


# Analyze button
def b3CallBack():
    try:
        label2.configure(text='Executing...', bg='yellow')
        try:
            scrollable_frame.pack_forget()
        except:
            pass
        choice_1 = combo1.get()
        x_axis = [2016, 2017, 2018]
        y_axis = [0, 0, 0]
        y_label = ''
        if choice_1 == 'Traffic Volume':
            y_axis = [m_v_16, m_v_17, m_v_18]
            y_label = 'Highest traffic volume'
            title = 'Traffic Volume'
        else:
            y_axis = [m_a_16, m_a_17, m_a_18]
            y_label = 'Highest concentration of accidents'
            title = 'Accidents'

        fig.clear()
        a = fig.add_subplot(111)
        a.plot(x_axis, y_axis, '-o')
        a.set_ylabel(y_label)
        a.set_xlabel("Year", fontsize=14)
        a.set_xticks(np.arange(2016, 2019, 1.0))
        a.set_title(title)

        try:
            canvas.get_tk_widget().pack()
        except:
            pass
        canvas.draw()
        label2.configure(text='Success', bg='green')
    except:
        label2.configure(text='Failure', bg='red')


# Map button
def b4CallBack():
    try:
        label2.configure(text='Executing...', bg='yellow')
        try:
            canvas.get_tk_widget().pack_forget()
        except:
            pass
        try:
            scrollable_frame.pack(fill='both', expand=True)
        except:
            pass
        scrollable_frame.clear()
        choice_1 = combo1.get()
        choice_2 = combo2.get()
        file_name = ''
        if choice_1 == 'Traffic Volume':
            if choice_2 == '2016':
                file_name = 'traffic_2016.png'
            elif choice_2 == '2017':
                file_name = 'traffic_2017.png'
            else:
                file_name = 'traffic_2018.png'
        else:
            if choice_2 == '2016':
                file_name = 'incidents_2016.png'
            elif choice_2 == '2017':
                file_name = 'incidents_2017.png'
            else:
                file_name = 'incidents_2018.png'
        scrollable_frame.add_image(file_name)
        label2.configure(text='Success', bg='green')
    except:
        label2.configure(text='Failure', bg='red')


# Create tkinter GUI
top = tk.Tk()
top.geometry("2000x600")
left_frame = tk.Frame(top, height=480, width=240, bg='grey', borderwidth=50)
left_frame.pack(side=tk.LEFT, fill='both')
right_frame = tk.Frame(top, height=480, width=840)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
c = tk.Canvas(right_frame, bg='white', height=500, width=800)
c.pack(fill=tk.BOTH, expand=True)
col_count, row_count = left_frame.grid_size()
for col in range(col_count):
    left_frame.grid_columnconfigure(col, minsize=20)
for row in range(row_count):
    left_frame.grid_rowconfigure(row, minsize=20)
combo1 = ttk.Combobox(left_frame, value=['Traffic Volume', 'Traffic Accident'], state='readonly', width=30)
combo1.grid(row=1, column=1, padx=10, pady=10)
combo1.current(0)
combo2 = ttk.Combobox(left_frame, value=['2016', '2017', '2018'], state='readonly', width=30)
combo2.grid(row=3, column=1, padx=10, pady=10)
combo2.current(0)
button1 = tk.Button(left_frame, text='Read', width=30, command=b1CallBack, highlightbackground='#3E4149')
button1.grid(row=5, column=1, padx=10, pady=10)
button2 = tk.Button(left_frame, text='Sort', width=30, command=b2CallBack, highlightbackground='#3E4149')
button2.grid(row=7, column=1, padx=10, pady=10)
button3 = tk.Button(left_frame, text='Analyze', width=30, command=b3CallBack, highlightbackground='#3E4149')
button3.grid(row=9, column=1, padx=10, pady=10)
button4 = tk.Button(left_frame, text='Map', width=30, command=b4CallBack, highlightbackground='#3E4149')
button4.grid(row=11, column=1, padx=10, pady=10)

fig = Figure(figsize=(7, 7))
fig.clear()
a = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=c)
canvas.get_tk_widget().pack()

scrollable_frame = ScrollableFrame(c)

label = tk.Label(left_frame, text='Status:', fg='white', bg='grey')
label.grid(row=14, column=1, padx=10, pady=10)
label2 = tk.Label(left_frame, text='Pending...', bg='yellow', width=30, height=3)
label2.grid(row=15, column=1, pady=5)


top.mainloop()
