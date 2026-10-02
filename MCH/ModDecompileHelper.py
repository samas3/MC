from tkinter import *
import tkinter.messagebox
import csv
def mdk():
    t = Tk()
    t.title('主窗口')
    tkinter.messagebox.showwarning(title = '警告', message = '请先下载一个java反编译器(推荐java-decompiler.github.io)反编译mod源代码后使用!')
    # 0 -> client
    # 2 -> server
    c1 = csv.reader(open('fields.csv', 'r'))
    c2 = csv.reader(open('methods.csv', 'r'))
    c3 = csv.reader(open('params.csv', 'r'))
    field = [i for i in c1][1:]
    method = [i for i in c2][1:]
    param = [i for i in c3][1:]
    fd = [[i[0] for i in field], [i[1] for i in field], [i[2] for i in field], [i[3] for i in field]]
    md = [[i[0] for i in method], [i[1] for i in method], [i[2] for i in method], [i[3] for i in method]]
    pd = [[i[0] for i in param], [i[1] for i in param], [i[2] for i in param]]
    tkinter.messagebox.showinfo(title = '提示', message = '加载了{}个变量, {}个方法, {}个参数'.format(len(fd[0]), len(md[0]), len(pd[0])))
    def ff(txt):
        if txt not in fd[0]:
            return -1
        ind = fd[0].index(txt)
        return fd[0][ind], fd[1][ind], fd[2][ind], fd[3][ind]
    def fm(txt):
        if txt not in md[0]:
            return -1
        ind = md[0].index(txt)
        return md[0][ind], md[1][ind], md[2][ind], md[3][ind]
    def fp(txt):
        if txt not in pd[0]:
            return -1
        ind = pd[0].index(txt)
        return pd[0][ind], pd[1][ind], pd[2][ind]#, pd[3][ind]
    def button1():
        t1 = Tk()
        t1.title('文档')
        l1_1 = Label(t1, text = '输入名称(如field_XXXXXX_xx、func_XXXXXX_xx、p_XXXXXX_x_)')
        l1_1.pack()
        e1_1 = Entry(t1, exportselection = 0, width = 20)
        e1_1.pack()
        tx1_1 = Text(t1, width = 50, height = 8)
        def que():
            tx1_1.delete(1.0, 'end')
            txt = e1_1.get()
            result = ''
            if 'field_' in txt:
                res = ff(txt)
                if res == -1:
                    result = '暂无数据......请检查输入或输入网址export.mcpbot.bspk.rs查询！'
                else:
                    result = '原名:{}\n真名:{}\n平台:{}\n描述:{}'.format(res[0], res[1], '客户端' if res[2] == '0' else '服务端', '暂无' if not res[3] else res[3])
            elif 'func_' in txt:
                res = fm(txt)
                if res == -1:
                    result = '暂无数据......请检查输入或输入网址export.mcpbot.bspk.rs查询！'
                else:
                    result = '原名:{}\n真名:{}\n平台:{}\n描述:{}'.format(res[0], res[1], '客户端' if res[2] == '0' else '服务端', '暂无' if not res[3] else res[3])
            elif 'p_' in txt:
                res = fp(txt)
                if res == -1:
                    result = '暂无数据......请检查输入或输入网址export.mcpbot.bspk.rs查询！'
                else:
                    result = '原名:{}\n真名:{}\n平台:{}'.format(res[0], res[1], '客户端' if res[2] == '0' else '服务端')
            else:
                result = '格式错误!'
            tx1_1.insert(1.0, result)
        b1_1 = Button(t1, text = '查询', command = que)
        b1_1.pack()
        tx1_1.pack()
        t1.mainloop()
    def button2():
        t2 = Tk()
        t2.title('翻译')
        l2_1 = Label(t2, text = '输入反编译后代码\n(可能无法正确运行，如遇到该情况，请更改字符串内代码和/或参数)')
        l2_1.pack()
        sb2_1 = Scrollbar(t2)
        sb2_1.pack(side='right', fill='y')
        tx2_1 = Text(t2, width = 100, height = 30, yscrollcommand = sb2_1.set)
        def trans():

            txt = tx2_1.get(0.0, 'end')
            for i in range(len(fd[0])):
                if fd[0][i] in txt:
                    txt = txt.replace(fd[0][i], fd[1][i])
            for i in range(len(md[0])):
                if md[0][i] in txt:
                    txt = txt.replace(md[0][i], md[1][i])
            for i in range(len(pd[0])):
                if pd[0][i] in txt:
                    txt = txt.replace(pd[0][i], pd[1][i])
            tx2_1.delete(1.0, 'end')
            tx2_1.insert(1.0, txt)
            tkinter.messagebox.showinfo(title = '提示', message = '完成!')
        sb2_1.config(command = tx2_1.yview)
        tx2_1.pack()
        b2_1 = Button(t2, text = '翻译(替换原代码)', command = trans)
        b2_1.pack()
        t2.mainloop()
    b1 = Button(t, text = '变量/函数/参数文档', command = button1)
    b2 = Button(t, text = '翻译反编译后代码', command = button2)
    b1.pack()
    b2.pack()
    t.mainloop()
if __name__ == '__main__':
    mdk()
