import os, shutil
from tkinter import *
import tkinter.messagebox, tkinter.ttk
import util
from urllib.request import urlopen
from functools import partial
def maven():
    t = Tk()
    mode = 1
    t.title('一个垃圾的Maven依赖下载器')
    l1 = Label(t, text = 'Maven库地址（留空为默认：maven.aliyun.com/repository/public）：')
    e1 = Entry(t)
    l2 = Label(t, text = '包名：')
    e2 = Entry(t)
    l3 = Label(t, text = '版本：')
    e3 = Entry(t)
    v1 = IntVar()
    v1.set(1)
    l4 = Label(t, text = '下载模式：')
    def c1():
        global mode
        mode = 1
    def c2():
        global mode
        mode = 2
    r1 = Radiobutton(t, variable = v1, text = '已编译', value = 1, command = c1)
    r2 = Radiobutton(t, variable = v1, text = '源代码', value = 2, command = c2)
    l1.pack()
    e1.pack()
    l2.pack()
    e2.pack()
    l3.pack()
    e3.pack()
    l4.pack()
    r1.pack()
    r2.pack()
    def download():
        p = e1.get()
        x = e2.get()
        v = e3.get()
        if not p:
            p = 'https://maven.aliyun.com/repository/public'
        else:
            p = 'https://' + p
        net = '{}/{}/{}'.format(p, '/'.join(x.split('.')), v)
        file = '{}-{}{}.jar'.format(x.split('.')[-1], v, '' if mode == 1 else '-sources')
        copy_url('{}/{}'.format(net, file))
        cmd = 'certutil -hashfile .\\{}'.format(file)
        cmd = os.popen(cmd)
        sha1 = cmd.readlines()[1].replace('\n', '')
        os.mkdir(sha1)
        shutil.move(file, '.\\{}'.format(sha1))
        tkinter.messagebox.showinfo('INFO', 'DONE')
    b1 = Button(t, text = '下载', command = download)
    b1.pack()
    t.mainloop()
if __name__ == '__main__':
    maven()
