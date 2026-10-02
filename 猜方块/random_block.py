import md
from random import choice
import json
from tkinter import *
t = Tk()
t.title('随机方块/物品 Java 1.19.2')
inst = md('1.19.2').blocks_list
inst2 = md('1.19.2').items_list
blocks = []
items = []
for i in inst:
    blocks.append(i['name'])
for i in inst2:
    items.append(i['name'])
def translate(name, file='names.json'):
    with open(file, encoding='utf-8') as f:
        j = json.load(f)
        if 'block.minecraft.' + name in j:
            return j['block.minecraft.' + name]
        return j['item.minecraft.' + name]
def do():
    txt.delete(1.0, 'end')
    item = choice(blocks + items)
    txt.insert('end', translate(item) + ' ' + translate(item, 'en_us.json'))
Button(t, text='获取', command=do).grid(row=0, column=0)
txt = Text(t)
txt.grid(row=1, column=0)
t.mainloop()