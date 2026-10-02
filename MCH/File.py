from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import os, subprocess
t = Tk()
def run(cmd):
    return subprocess.run(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('gbk')
t.title('certutil')
t1 = Text(t)
def showinfo(s, t):
    t1.delete(1.0, 'end')
    t1.insert('end', str(t))
l1 = Label(t, text = 'Filename:')
l1.grid(row = 0, column = 0)
e1 = Entry(t)
e1.grid(row = 0, column = 1)
l2 = Label(t)
def size(file):
    sz = os.path.getsize(file)
    if sz < 1024:
        return f'{sz} B'
    if sz < 1024 ** 2:
        return f'{round(sz / 1024, 2)} KB'
    if sz < 1024 ** 3:
        return f'{round(sz / 1024 ** 2, 2)} MB'
    if sz < 1024 ** 4:
        return f'{round(sz / 1024 ** 3, 2)} GB'
def openfile():
    e1.delete(0, 'end')
    e1.insert('end', askopenfilename())
    l2['text'] = f'Filesize: {size(e1.get())}'
b1 = Button(t, text = 'Open...', command = openfile)
b1.grid(row = 0, column = 2)
l2.grid(row = 1, column = 0, columnspan = 3)
def enc():
    ext = os.path.splitext(e1.get())
    out = run(f'certutil -f -v -seconds -encode "{e1.get()}" "{"".join(ext[:-1])}_encode{ext[-1]}"')
    showinfo('Info', out)
b2 = Button(t, text = 'Encode', command = enc)
b2.grid(row = 3, column = 0)
def dec():
    ext = os.path.splitext(e1.get())
    out = run(f'certutil -f -v -seconds -decode "{e1.get()}" "{"".join(ext[:-1])}_decode{ext[-1]}"')
    showinfo('Info', out)
b3 = Button(t, text = 'Decode', command = dec)
b3.grid(row = 3, column = 2)
s1 = StringVar()
s1.set('MD5')
def choose():
    s = s1.get()
    t1.delete(1.0, 'end')
    out = os.popen(f'certutil -v -seconds -hashfile "{e1.get()}" {s}')
    t1.insert('end', s + ': ' + out.read().split('\n')[1])
hashes = ['MD2', 'MD4', 'MD5', 'SHA1', 'SHA256', 'SHA384', 'SHA512']
c1 = ttk.Combobox(t, state='readonly', textvariable=s1, values=hashes)
c1.grid(row = 2, column = 0)
b4 = Button(t, text = 'Hash', command = choose)
b4.grid(row = 2, column = 2)
t1.grid(row = 4, column = 0, columnspan = 3)
t.mainloop()
