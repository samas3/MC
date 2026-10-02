from tkinter import *
from time import time
t = Tk()
running = 0
tm = 0
rec = []
s1 = StringVar()
s1.set('cleared')
l1 = Label(t, textvariable = s1)
l1.pack()
s2 = StringVar()
def beautify(lst):
    if len(lst) <= 2:
        return lst
    res = str(lst).split(', ')[::len(lst) - 1]
    return ', '.join([res[0], '...', res[1]])
s2.set(f'{len(rec)}, {sum(rec)}: {beautify(rec)}')
s3 = StringVar()
s3.set('start')
l2 = Label(t, textvariable = s2)
l2.pack()
def st():
    global tm, running
    running = not running
    if running:
        s1.set('running')
        s3.set('stop')
        tm = time()
    else:
        s3.set('start')
        lap = round((time() - tm) * 1000000)
        s1.set(str(lap) + 'μs')
        rec.append(lap)
        s2.set(f'{len(rec)}, {sum(rec)}: {beautify(rec)}')
b1 = Button(t, textvariable = s3, command = st)
b1.pack()
def cl():
    global rec, tm
    rec = []
    tm = 0
    s1.set('cleared')
    s2.set(f'{len(rec)}, {sum(rec)}: {beautify(rec)}')
b2 = Button(t, text = 'clear', command = cl)
b2.pack()
t.mainloop()
