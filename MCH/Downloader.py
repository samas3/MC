from util import copy_url
from tkinter import *
from tkinter.messagebox import *
def down():
    t = Tk()
    t.title('是人都会用的下载器 - 重置版')
    l1 = Label(t, text = 'URL:')
    l1.grid(row = 0, column = 0)
    e1 = Entry(t, width = 50)
    e1.grid(row = 0,  column = 1)
    def download():
        copy_url(e1.get())
        showinfo('提示', '下载完成')
    b1 = Button(t, text = '下载', command = download)
    b1.grid(row = 1, column = 0, columnspan = 2)
    t.mainloop()
if __name__ == '__main__':
    down()
