#!/usr/bin/env python3
from pypps.PyPPSPC import *
from code import interact
import configparser
from tkinter import *
from tkinter import simpledialog, messagebox
from threading import Timer

def get_credentials():
    # inspired by https://gist.github.com/Nircek/4d32a447a6783a4e63ee3cf6dbb1afb7
    creds = []
    tk = Tk()
    tk.title('Log in')
    Label(tk, text='Server URL: ').grid(column=0, row=0, sticky=W)
    Label(tk, text='Username: ').grid(column=0, row=1, sticky=W)
    Label(tk, text='Password: ').grid(column=0, row=2, sticky=W)
    u = Entry(tk)
    u.focus_set()
    u.grid(column=1, row=0, pady=2)
    n = Entry(tk)
    n.grid(column=1, row=1, pady=2)
    u.bind('<Return>', lambda x:n.focus_set())
    p = Entry(tk, show='*')
    p.grid(column=1, row=2, pady=2)
    n.bind('<Return>', lambda x:p.focus_set())
    b = Button(tk, text='Log in!', command=lambda:(lambda x:tk.quit())(creds.extend([u.get(), n.get(), p.get()])))
    b.grid(column=0, row=3, columnspan=2, pady=5)
    p.bind('<Return>', lambda x: b.invoke())
    tk.mainloop()
    tk.destroy()
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
        Button(self, text='Connect', command=self.client.makePPSPC).pack()
        Button(self, text='Quit', command=self.client.on_quit).pack()

class BattleshipClient:
    def __init__(self):
        self.frames = FrameHolder(lambda x:Main(x,self))
        self.frames.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.p = None
        self.connected = False
        self.t = None

    def on_quit(self):
        print('on_quit')
        self.interval = -1
        self.frames.destroy()

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, x):
        if self.t is not None:
            self.t.cancel()
        self.__interval = x
        if self.interval >= 0 and (self.t is None or not self.t.is_alive()):
            self.t = Timer(self.interval, self.intervalFunc)
            self.t.start()

    def intervalFunc(self):
        ev = self.p.refreshj()
        print(ev)
        if self.interval >= 0:
            if ev['cmd'] == 'error()':
                messagebox.showerror(ev['type']+' error', str(ev['data']))
                self.t = Timer(self.interval, self.intervalFunc)
                self.t.start()

    def makePPSPC(self):
        url, username, password = get_credentials()
        self.p = PyPPSPC(url)
        self.p.input = lambda x,y:simpledialog.askstring(x, y, parent=self.frames)
        self.p.bool = lambda x,y:messagebox.askokcancel(x, y, parent=self.frames)
        print('Connecting... ', end='')
        self.p.connect()
        print('done.')
        self.p.login(username, password)
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
