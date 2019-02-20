#!/usr/bin/env python3
from pypps.PyPPSPC import *
from code import interact
import configparser
from tkinter import *
from tkinter import simpledialog, messagebox
from threading import Timer

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.p = None
        self.interval_set = False

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, x):
        self.__interval = x
        if self.interval >= 0 and not self.interval_set:
            Timer(self.interval, self.intervalFunc).start()

    def intervalFunc(self):
        if self.interval < 0:
            self.interval_set = False
            return
        self.interval_set = True
        # ---
        ev = self.p.refreshj()
        print(ev)
        if ev['cmd'] == 'error()':
            messagebox.showerror(ev['type']+' error', str(ev['data']))
        # ---
        if self.interval >= 0:
            Timer(self.interval, self.intervalFunc).start()
        else:
            self.interval_set = False

    def create_widgets(self):
        self.connect_btn = Button(self)
        self.connect_btn["text"] = "Connect"
        self.connect_btn["command"] = self.makePPSPC
        self.connect_btn.pack(side="top")
        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def makePPSPC(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.p = PyPPSPC(config['PseudoPHPServer']['url'])
        self.p.input = lambda x,y:simpledialog.askstring(x, y, parent=master)
        self.p.bool = lambda x,y:messagebox.askokcancel(x, y)
        self.p.connect()
        self.p.login(config['PseudoPHPServer']['user'], config['PseudoPHPServer']['pass'])
        self.connected = True
        self.interval = 5

root = Tk()
app = Application(master=root)
app.mainloop()
'''
getRooms()
newRoom() player
joinRoom() i
build() i, pos

error() type, data
setRoom() data={info,uBoard,pBoard}
setRooms() data=[info]
'''
