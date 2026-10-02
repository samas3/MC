from tkinter import *
from tkinter.messagebox import *
from util import *
import os #, win32clipboard
def google():
    if __name__ == '__main__':
        t = Tk()
    else:
        t = Toplevel()
    t.title('Google Grass Maker')
    grass = PhotoImage(file = 'grass.png')
    l1 = Label(t, image = grass)
    l1.pack()

    s1 = Scrollbar(t)
    s1.pack(side = LEFT, fill = Y)
    t1 = Text(t, width = 50, height = 5, yscrollcommand = s1.set)
    s1.config(command = t1.yview)
    t1.pack()
    t1.insert('end', '输入翻译内容...')

    v1 = StringVar()
    v1.set('翻译语言(格式:xx>xx)')
    e1 = Entry(t, textvariable = v1, exportselection = 0)
    e1.pack()

    s2 = Scrollbar(t)
    s2.pack(side = RIGHT, fill = Y)
    t2 = Text(t, width = 50, height = 5, yscrollcommand = s2.set)
    s2.config(command = t2.yview)
    t2.pack()
    t2.insert('end', '翻译结果...')

    def do_trans():
        val = t1.get(1.0, 'end')
        lang = e1.get().split('>')
        t2.delete(1.0, 'end')
        t2.insert('end', trans(val, lang[0], lang[1]))
    b1 = Button(t, text = '生草', command = do_trans)
    b1.pack()

    def turn():
        lang = e1.get().split('>')
        e1.delete(0, END)
        e1.insert(END, lang[1] + '>' + lang[0])
        t1get = t1.get(1.0, 'end')
        t2get = t2.get(1.0, 'end')
        t1.delete(1.0, 'end')
        t2.delete(1.0, 'end')
        t1.insert('end', t2get)
        t2.insert('end', t1get)
    b2 = Button(t, text = '切换语言&内容', command = turn)
    b2.pack()

    '''def copy(): 
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, t2.get(1.0, 'end')) 
        win32clipboard.CloseClipboard()
    b3 = Button(t, text = '复制翻译内容', command = copy)
    b3.pack()'''

    '''def paste():
        t1.delete(1.0, 'end')
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        t1.insert('end', win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT))
        win32clipboard.CloseClipboard()
    b4 = Button(t, text = '将剪贴板内容粘贴至翻译区', command = paste)
    b4.pack()
    '''
    def view():
        showinfo('语言代码', str(LANG))
    b5 = Button(t, text = '查看语言代码', command = view)
    b5.pack()
    t.mainloop()
if __name__ == '__main__':
    google()
