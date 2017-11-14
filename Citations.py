#!/usr/bin/python
import sys
import os
import Tkinter
from Tkinter import *
import tkMessageBox
top=Tkinter.Tk()
top.geometry("700x500")


var = StringVar()
textbox = Entry(top, textvariable=var)
textbox.focus_set()
textbox.pack(pady=10, padx=10)

def helloCallBack():
    global var, Text
    command = "python citations10.py %s" % str(var.get())
    Outputfileobject=os.popen(command)
    Output=Outputfileobject.read()
    Outputfileobject.close()
    Text.insert(END, Output)


B=Tkinter.Button(top,text="run",command= helloCallBack)
B.pack()
Text=Tkinter.Text(top,height=50)
Text.pack()


top.mainloop()