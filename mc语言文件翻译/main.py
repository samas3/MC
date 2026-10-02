import os
import json
import time
import zipfile
import translate
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter import ttk

t = Tk()
t.title('MC语言文件翻译工具')
choose = Frame(t)
choose.pack()
process = Frame(t)
default = font.nametofont('TkDefaultFont')
default.configure(family='微软雅黑', size=12)

def choose_folder():
    folder_path = filedialog.askdirectory(title='选择已有项目文件夹')
    if not folder_path:
        return
    if not os.path.exists(folder_path + '/pack.mcmeta'):
        messagebox.showerror('错误', '该文件夹不是有效的MC语言文件项目')
        return
    os.chdir(folder_path)
    start_process()
Button(choose, text='选择已有项目文件夹', command=choose_folder).pack()
def choose_file():
    jar_path = filedialog.askopenfilename(title='选择mod文件', filetypes=[('jar文件', '*.jar')])
    if not jar_path:
        return
    folder = '.'.join(jar_path.split('/')[-1].split('.')[:-1])
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    with open('pack.mcmeta', 'w', encoding='utf-8') as f:
        f.write('{\n  "pack": {\n    "pack_format": 15,\n    "description": "' + folder + '翻译文件"\n  }\n}')
    with zipfile.ZipFile(jar_path, 'r') as z:
        for i in z.namelist():
            if i.startswith('assets/') and i.endswith('.json') and '/lang/' in i:
                os.makedirs(os.path.dirname(i), exist_ok=True)
                z.extract(i)
    start_process()
Button(choose, text='选择新的mod文件', command=choose_file).pack()

folders = []
current = ''
menu = Menu(t)
def start_process():
    global folders, current
    choose.pack_forget()
    process.pack()
    cwd = os.getcwd()
    t.title('MC语言文件翻译工具 - ' + cwd.split(os.sep)[-1])
    os.chdir('assets')
    for i in os.listdir():
        if os.path.isdir(i):
            folders.append(i)
    current = folders[0]
    t.config(menu=menu)
    load()
Label(process, text='目标语言').grid(row=0, column=0)
target = StringVar()
target.set('zh_cn')
lang = 'zh_cn'
target_entry = Entry(process, textvariable=target)
target_entry.grid(row=0, column=1)
current_label = Label(process)
current_label.grid(row=2, column=0, columnspan=2)
def prev():
    global current
    current = folders[(folders.index(current) - 1) % len(folders)]
    load()
Button(process, text='上一个文件夹', command=prev).grid(row=1, column=0)
def next():
    global current
    current = folders[(folders.index(current) + 1) % len(folders)]
    load()
Button(process, text='下一个文件夹', command=next).grid(row=1, column=1)
def save():
    with open(current + '/lang/' + lang + '.json', 'w', encoding='utf-8') as f:
        dic = {}
        for i in tree.get_children():
            key = str(tree.item(i)['values'][0])
            value = str(tree.item(i)['values'][1]).replace('\\n', '\n').replace("\\'", "'")
            if value:
                dic[key] = value
        if dic:
            json.dump(dic, f, ensure_ascii=False, indent=2)
menu2 = Menu(menu, tearoff=False)
menu2.add_command(label='保存', command=save, accelerator='Ctrl+S')
def find():
    t2 = Toplevel(t)
    t2.title('查找文本')
    Label(t2, text='请输入要查找的文本：').pack()
    text = StringVar()
    entry = Entry(t2, textvariable=text)
    entry.focus_set()
    entry.pack()
    def find_next(event=None):
        index = tree.index(tree.focus())
        for i, j in enumerate(tree.get_children()):
            if i > index:
                key = str(tree.item(j)['values'][0])
                value = str(tree.item(j)['values'][1])
                if text.get() in key or text.get() in value:
                    tree.see(j)
                    tree.selection_set(j)
                    tree.focus(j)
                    messagebox.showinfo('提示', '已跳转到对应文本')
                    t2.destroy()
                    return
        messagebox.showinfo('提示', '未找到对应文本')
        t2.destroy()
    Button(t2, text='查找下一个', command=find_next).pack()
    entry.bind('<Return>', find_next)
    t2.mainloop()
menu2.add_command(label='查找', command=find, accelerator='Ctrl+F')
def replace():
    t2 = Toplevel(t)
    t2.title('替换文本')
    Label(t2, text='请输入要替换的文本：').pack()
    old_text = StringVar()
    old_entry = Entry(t2, textvariable=old_text)
    old_entry.focus_set()
    old_entry.pack()
    Label(t2, text='请输入替换后的文本：').pack()
    new_text = StringVar()
    new_entry = Entry(t2, textvariable=new_text)
    new_entry.pack()
    def set_focus(event=None):
        new_entry.focus_set()
    old_entry.bind('<Return>', set_focus)
    def replace_all(event=None):
        cnt = 0
        for i in tree.get_children():
            key = str(tree.item(i)['values'][0])
            value = str(tree.item(i)['values'][1])
            if old_text.get() in value:
                tree.item(i, values=(key, value.replace(old_text.get(), new_text.get())))
                cnt += 1
                save()
        messagebox.showinfo('替换完成', '共替换 ' + str(cnt) + ' 个文本')
        t2.destroy()
    Button(t2, text='替换全部', command=replace_all).pack()
    new_entry.bind('<Return>', replace_all)
    t2.mainloop()
menu2.add_command(label='替换', command=replace, accelerator='Ctrl+R')
def close():
    choose.pack()
    process.pack_forget()
    t.title('MC语言文件翻译工具')
    t.config(menu='')
menu2.add_command(label='关闭', command=close, accelerator='Ctrl+W')
menu.add_cascade(menu=menu2, label='文件')
t.bind('<Control-s>', lambda _: save())
t.bind('<Control-f>', lambda _: find())
t.bind('<Control-r>', lambda _: replace())
t.bind('<Control-w>', lambda _: close())
running = False
def translate_all():
    global running
    running = not running
    l = lang.replace('_', '-')
    l = l.split('-')[0] + '-' + l.split('-')[1].upper()
    def trans():
        global running
        for j, i in enumerate(tree.get_children()):
            key = str(tree.item(i)['values'][0])
            value = str(tree.item(i)['values'][1])
            if any(u'\u4e00' <= char <= u'\u9fff' for char in value):
                continue
            translated = ''
            while not translated and running:
                try:
                    #trans_button.config(text='翻译中: 共' + str(len(strs)))
                    trans_button.config(text='翻译中: ' + str(j + 1) + '/' + str(len(tree.get_children())))
                    translated = translate.remove_unprintable_chars(translate.translate(value, l, {'https': '127.0.0.1:7890', 'http': '127.0.0.1:7890'}))
                    time.sleep(1)
                    tree.item(i, values=(key, translated))
                    save()
                except ConnectionAbortedError:
                    pass
                except Exception as e:
                    #print(e)
                    #trans_button.config(text='翻译全部')
                    #return
                    continue
            if not running:
                trans_button.config(text='翻译全部')
                return
        trans_button.config(text='翻译全部')
        running = False
        messagebox.showinfo('提示', '翻译完成')
    th = threading.Thread(target=trans, daemon=True)
    th.start()
trans_button = Button(process, text='翻译全部', command=translate_all)
trans_button.grid(row=2, column=1)
def compare():
    global lang
    if lang != 'en_us':
        lang = 'en_us'
    else:
        lang = target.get()
    load()
Button(process, text='对比', command=compare).grid(row=2, column=0)
def load(event=None):
    with open(current + '/lang/en_us.json', 'r', encoding='utf-8') as f:
        en_us = json.load(f)
    keys = list(en_us.keys())
    not_exist = False
    if not os.path.exists(current + '/lang/' + lang + '.json'):
        with open(current + '/lang/' + lang + '.json', 'w', encoding='utf-8') as f:
            f.write('{}')
    with open(current + '/lang/' + lang + '.json', 'r', encoding='utf-8') as f:
        try:
            target_dict = json.load(f)
        except:
            target_dict = {}
    if not target_dict:
        not_exist = True
    keys2 = list(target_dict.keys())
    extra_keys = set(keys2) - set(keys)
    extra_dict = {k: target_dict[k] for k in extra_keys if target_dict[k]}
    for k in extra_keys:
        del target_dict[k]
    current_label.config(text='当前文件夹：' + current + ', 条目数：' + str(len(en_us)))
    need_keys = set(keys) - set(keys2)
    need_dict = {k: en_us[k] for k in need_keys if en_us[k]}
    if not_exist:
        target_dict = need_dict
        need_dict = {}
    tree.delete(*tree.get_children())
    for key in keys:
        value = target_dict.get(key, '')
        if value:
            add_item(key, value)
    if need_dict:
        add_item('以下为缺失的键值对', '')
        for key, value in need_dict.items():
            if value:
                add_item(key, value)
    if extra_dict:
        add_item('以下为多余的键值对', '')
        for key, value in extra_dict.items():
            if value:
                add_item(key, value)
menu2.add_command(label='刷新', command=load, accelerator='F5')
t.bind('<F5>', load)
target_entry.bind('<Return>', load)
def edit_cell(event):
    row = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    t = Toplevel(process)
    t.title('编辑文本')
    text = Text(t, width=100)
    text.pack()
    def apply_edit(event=None):
        new_value = text.get(1.0, 'end').replace('&', '\u00a7').strip()
        tree.set(row, column, new_value)
        save()
        t.destroy()
    value = tree.set(row, column)
    text.insert('end', value)
    text.bind('<Return>', apply_edit)
    text.focus_set()
    t.protocol('WM_DELETE_WINDOW', apply_edit)
    t.mainloop()
def delete_line(event):
    rows = tree.selection()
    if not rows:
        return
    tree.delete(rows)
    save()
def add_line(event):
    rows = tree.selection()
    if not rows:
        return
    tree.insert(rows[0], 'end', values=('', ''))
tree = ttk.Treeview(process, columns=('key', 'value'), show='headings')
tree.grid(row=4, column=0, columnspan=2, sticky='nsew')
tree.heading('key', text='键')
tree.heading('value', text='值')
tree.column('#0', width=0, stretch=NO)
tree.column('key', width=300)
tree.column('value', width=800)
tree.bind('<Double-1>', edit_cell)
tree.bind('<Delete>', delete_line)
tree.bind('<Return>', add_line)
operation = Menu(menu, tearoff=False)
operation.add_command(label='编辑', accelerator='Double-click')
operation.add_command(label='删除行', accelerator='Delete')
operation.add_command(label='插入行', accelerator='Enter')
menu.add_cascade(menu=operation, label='操作')
scroll = Scrollbar(process, orient='vertical', command=tree.yview)
scroll.grid(row=4, column=2, sticky='ns')
tree.configure(yscrollcommand=scroll.set)
def add_item(key, value):
    tree.insert('', 'end', values=(key, repr(value)[1:-1].replace('\\\\', '\\')))
t.mainloop()