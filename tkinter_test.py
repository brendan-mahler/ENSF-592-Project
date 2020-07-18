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
from cursors import *

matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ScrollableFrame import *


def b1CallBack():
    display_table()


def b2CallBack():

    sort_table_by_volume()


def b3CallBack():
    if button3.cget('text') == 'Analyze':
        button3.configure(text='Generalize')
    else:
        button3.config(text='Analyze')


def b4CallBack():
    if button4.cget('text') == 'Map':
        button4.configure(text='Compass')
    else:
        button4.config(text='Map')


top = tk.Tk(className='Testing')
left_frame = tk.Frame(top, height=480, width=240, bg='grey', borderwidth=50)
left_frame.pack(side=tk.LEFT, fill='both')
right_frame = tk.Frame(top, height=480, width=1200)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
c = tk.Canvas(right_frame, bg='white', height=500, width=700)
c.pack(fill=tk.BOTH, expand=True)
col_count, row_count = left_frame.grid_size()
for col in range(col_count):
    left_frame.grid_columnconfigure(col, minsize=20)
for row in range(row_count):
    left_frame.grid_rowconfigure(row, minsize=20)
combo1 = ttk.Combobox(left_frame, value=['Traffic Volume', 'Traffic Accident'], state='readonly', width=30)
combo1.grid(row=1, column=1, padx=10, pady=10)
combo1.current(0)
combo2 = ttk.Combobox(left_frame, value=['2016', '2017', '2018', 'All years'], state='readonly', width=30)
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
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
v = np.array([16, 16.31925, 17.6394, 16.003, 17.2861, 17.3131, 19.1259, 18.9694, 22.0003, 22.81226])
p = np.array([16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368,
              19.32125, 19.31756, 21.20247, 22.41444, 22.11718, 22.12453])

fig = Figure(figsize=(6, 6))
fig.clear()
a = fig.add_subplot(111)
a.scatter(v, x, color='red')
a.plot(p, range(2 + max(x)), color='blue')
a.invert_yaxis()

a.set_title("Estimation Grid", fontsize=16)
a.set_ylabel("Y", fontsize=14)
a.set_xlabel("X", fontsize=14)
"""
canvas = FigureCanvasTkAgg(fig, master=c)
canvas.get_tk_widget().pack()
canvas.draw()
"""

label = tk.Label(left_frame, text='Status:', fg='white', bg='grey')
label.grid(row=14, column=1, padx=10, pady=10)
label2 = tk.Label(left_frame, text='Pending...', bg='yellow', width=30, height=3)
label2.grid(row=15, column=1, pady=5)


def get_header():
    if combo1.get() == 'Traffic Volume' and combo2.get() == '2016':
        headers = ['secname', 'the_geom', 'year_vol', 'shape_leng', 'volume']
        table = cursors.rows_2016
    elif combo1.get() == 'Traffic Volume' and combo2.get() == '2017':
        headers = ['year', 'segment_name', 'the_geom', 'length_m', 'volume']
        table = cursors.rows_2017
    elif combo1.get() == 'Traffic Volume' and combo2.get() == '2018':
        headers = ['YEAR', 'SECNAME', 'Shape_Leng', 'VOLUME', 'multilinestring']
        table = cursors.rows_2018
    elif combo1.get() == 'Traffic Accident' and combo2.get() == 'All years':
        headers = ['INCIDENT INFO', 'DESCRIPTION', 'START_DT',
                   'MODIFIED_DT', 'QUADRANT', 'Longitude', 'Latitude', 'location', 'Count']
        table = cursors.accident_rows
    return headers, table


def display_table():
    headers, table = get_header()
    data = {}
    for header in headers:
        data[header] = list()

    for row in table:
        for header in headers:
            data[header].append(row[header])

    scrollable_frame = ScrollableFrame(c)
    scrollable_frame.add_table(data)
    scrollable_frame.pack(fill=tk.BOTH, expand=True)


def sort_table_by_volume():
    headers, table = get_header()
    table = cursors.sorted_rows_2016
    data = {}
    for header in headers:
        data[header] = list()

    for row in table:
        for header in headers:
            data[header].append(row[header])

    scrollable_frame = ScrollableFrame(c)
    scrollable_frame.add_table(data)
    scrollable_frame.pack(fill=tk.BOTH, expand=True)


top.mainloop()
