#!/usr/bin/env python3
from pypps.PyPPSPC import *
from code import interact
import configparser
from tkinter import *
from tkinter import simpledialog, messagebox
from threading import Timer

def get_credentials():
    # SRC: https://gist.github.com/Nircek/4d32a447a6783a4e63ee3cf6dbb1afb7
    creds = []
    tk = Tk()
    tk.title('Log in')
    Label(tk, text='Username: ').grid(column=0, row=0, sticky=W)
    Label(tk, text='Password: ').grid(column=0, row=1, sticky=W)
    u = Entry(tk)
    u.focus_set()
    u.grid(column=1, row=0, pady=2)
    p = Entry(tk, show='*')
    p.grid(column=1, row=1, pady=2)
    u.bind('<Return>', lambda x:p.focus_set())
    b = Button(tk, text='Log in!', command=lambda:(lambda x:tk.destroy())(creds.extend([u.get(), p.get()])))
    b.grid(column=0, row=2, columnspan=2, pady=5)
    p.bind('<Return>', lambda x: b.invoke())
    tk.mainloop()
    return creds if creds else None

class FrameHolder(Tk):
    # inspired by https://stackoverflow.com/a/49325719/6732111
    def __init__(self, main):
        Tk.__init__(self)
        self._fr = None
        self.switch(main)
    def switch(self, fr):
        n = fr(self)
        if self._fr is not None:
            self._fr.destroy()
        self._fr = n
        self._fr.pack()

class Main(Frame):
    def __init__(self, master, client):
        Frame.__init__(self, master)
        self.client = client
        Button(self, text='Log in', command = lambda: (lambda x: client.p.login(x[0], x[1]) if x is not None else None)(get_credentials())).pack()
        # TODO: ask about url
        # TODO: client.p can be None because of initialising PPSPC after 'Connect' button clickin
        Button(self, text='Connect', command=self.client.makePPSPC).pack()
        Button(self, text='Quit', command=self.master.destroy).pack()

class BattleshipClient:
    def __init__(self):
        self.frames = FrameHolder(lambda x:Main(x,self))
        self.p = None
        self.interval_set = False
        self.connected = False

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, x):
        self.__interval = x
        if self.interval >= 0 and not self.interval_set:
            print(Timer(self.interval, self.intervalFunc).start())

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

    def makePPSPC(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.p = PyPPSPC(config['PseudoPHPServer']['url'])
        self.p.input = lambda x,y:simpledialog.askstring(x, y, parent=master)
        self.p.bool = lambda x,y:messagebox.askokcancel(x, y)
        self.p.connect()
        self.connected = True
        self.interval = 5

if __name__ == '__main__':
    BattleshipClient().frames.mainloop()
'''
getRooms()
newRoom() player
joinRoom() i
build() i, pos

error() type, data
setRoom() data={info,uBoard,pBoard}
setRooms() data=[info]
'''
