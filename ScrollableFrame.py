# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 17:30:33 2020

@author: anhtr
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbary = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbarx = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        
        scrollbary.pack(side="right", fill="y")
        scrollbarx.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        
        
    def clear(self):
        self.scrollable_frame.clear()
        
    def add_image(self,file_name):
        load = Image.open(file_name)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.scrollable_frame,image=render)
        img.image = render
        img.pack(fill='both')
        
        
    def add_table(self, data_frame):
        headers = list(data_frame.keys())
        for i in range(len(headers)):
            self.scrollable_frame.grid_columnconfigure(i,minsize=15*len(headers[i]))
            tk.Button(self.scrollable_frame,text=headers[i],fg='black',bg='yellow').grid(row=0,column=i,sticky='we')
            for j in range(len(data_frame[headers[i]])):
                tk.Label(self.scrollable_frame,text=str(data_frame[headers[i]][j]),borderwidth=1,relief='solid',height=3,wraplength=100).grid(row=j+1,column=i,sticky='we')
        
def test():
    top = tk.Tk()
    frame = ScrollableFrame(top)
    frame.add_image('incidents_2017.png')
    frame.pack(fill='both',expand=True)
    top.mainloop()
    
if __name__=="__main__":
    test()