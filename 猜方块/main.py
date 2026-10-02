import md
from random import choice
import mcwiki
import json
from tkinter import *
t = Tk()
t.title('猜方块 Java 1.19.2')
inst = md('1.19.2').blocks_list
inst2 = md('1.19.2').items_list
blocks = []
items = []
for i in inst:
    blocks.append(i['name'])
for i in inst2:
    items.append(i['name'])
def translate(name):
    with open('names.json', encoding='utf-8') as f:
        j = json.load(f)
        if 'block.minecraft.' + name in j:
            return j['block.minecraft.' + name]
        return j['item.minecraft.' + name]
def get(block=''):
    res = {}
    if not block:
        block = choice(blocks)
    wiki = mcwiki.load('https://minecraft.fandom.com/zh/wiki/' + translate(block))
    info = list(wiki.extract_all(mcwiki.TextExtractor('tbody')))[0].split('\n\n\n\n')
    s = ''
    res['name'] = ','.join([i for i in list(wiki.extract_all(mcwiki.TextExtractor('b'))) if '(' in i])
    if block == 'TNT':
        res['name'] = 'TNT,' + res['name']
    for i in info:
        if '挖掘工具' in i or '命名空间ID' in i or (':' in i and '创造' not in i):
            continue
        j = i.split('\n\n\n')
        s += f'{j[-2]}:{j[-1]}\n'
    res['info'] = s
    try:
        s = ''
        for i in wiki['获取'].extract_all(mcwiki.PARAGRAPH):
            if 'Java' in i or '基岩' in i:
                continue
            s += i + '\n'
        for i in wiki['获取'].extract_all(mcwiki.TextExtractor('h3')):
            s += i + '\n'
        res['get'] = s
    except:
        res['get'] = '无'
    try:
        s = ''
        for i in wiki['自然生成'].extract_all(mcwiki.PARAGRAPH):
            s += i + '\n'
        res['spawn'] = s
    except:
        res['spawn'] = '无'
    try:
        s = ''
        for i in wiki['用途'].extract_all(mcwiki.PARAGRAPH):
            s += i + '\n'
        res['usage'] = s
    except:
        res['usage'] = '无'
    res['craft'] = ('合成' in wiki)
    return res
Label(t, text='方块ID:').grid(row=0, column=0)
b = Entry(t)
b.grid(row=0, column=1)
def do():
    txt.delete(1.0, 'end')
    res = get(b.get())
    txt.insert('end', '名称:' + res['name'] + '\n')
    txt.insert('end', '信息:\n' + res['info'] + '\n')
    txt.insert('end', '获取:\n' + res['get'] + '\n')
    txt.insert('end', '生成:\n' + res['spawn'] + '\n')
    txt.insert('end', '用途:\n' + res['usage'] + '\n')
    txt.insert('end', '可合成:' + str(res['craft']) + '\n')
Button(t, text='获取', command=do).grid(row=0, column=2)
txt = Text(t)
txt.grid(row=1, column=0, columnspan=3)
t.mainloop()