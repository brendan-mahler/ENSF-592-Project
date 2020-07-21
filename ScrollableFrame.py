# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 17:30:33 2020

@author: anhtr
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Create scrollable frame
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbary = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbarx = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        
        scrollbary.pack(side="right", fill="y")
        scrollbarx.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.temp_frame = tk.Frame(self.scrollable_frame)
        self.temp_frame.pack(fill="both",expand=True)
        
    # Destroy the current frame
    def clear(self):
        self.temp_frame.destroy()

     # Add map image to the frame
    def add_image(self,file_name):
        self.clear()
        self.temp_frame = tk.Frame(self.scrollable_frame)
        self.temp_frame.pack(fill="both",expand=True)
        load = Image.open(file_name)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.temp_frame,image=render)
        img.image = render
        img.pack(fill='both')
        
    # Add table to scrollable frame
    def add_table(self, data_frame):
        self.clear()
        self.temp_frame = tk.Frame(self.scrollable_frame)
        self.temp_frame.pack(fill="both",expand=True)
        headers = list(data_frame.keys())
        for i in range(len(headers)):
            self.temp_frame.grid_columnconfigure(i,minsize=20*len(headers[i]),weight=1)
            tk.Label(self.temp_frame,text=headers[i],fg='black',bg='yellow').grid(row=0,column=i,sticky='we')
            for j in range(len(data_frame[headers[i]])):
                tk.Label(self.temp_frame,text=str(data_frame[headers[i]][j]),borderwidth=1,relief='solid',height=3,wraplength=200).grid(row=j+1,column=i,sticky='we')

def test():
    top = tk.Tk()
    frame = ScrollableFrame(top)
    frame.add_image('incidents_2017.png')
    frame.pack(fill='both',expand=True)
    top.mainloop()
    
if __name__=="__main__":
    test()