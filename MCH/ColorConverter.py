from tkinter import *
import jsontextmc as jtm
def cc():
    if __name__ == '__main__':
        t = Tk()
    else:
        t = Toplevel()
    t.title('格式字符转JSON')
    l1 = Label(t, text = '含格式字符(&或§)的字符串')
    l1.grid(row = 0, column = 0)
    e1 = Entry(t)
    e1.grid(row = 0, column = 1)
    t1 = Text(t)
    def process():
        t1.delete(1.0, 'end')
        t1.insert('end', str(jtm.translate(e1.get().replace('§', '&'))))
    b1 = Button(t, text = '转换', command = process)
    b1.grid(row = 1, column = 0, columnspan = 2)
    t1.grid(row = 2, column = 0, columnspan = 2)
    t.mainloop()
if __name__ == '__main__':
    cc()
