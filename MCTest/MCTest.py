import md
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json, random, copy
t = Tk()
t.title('MC知识测试')
t.resizable(0, 0)
md_inst = md('1.18')
blocks = []
effects = []
enchantments = []
entities = []
items = []
v14 = {}
v16 = {}
v17 = {}
v18 = {}
l1 = Label(t, text = '版本:')
l1.grid(row = 0, column = 0)
verlst = ttk.Combobox(t)
verlst['value'] = ('1.14.4', '1.16.5', '1.17.1', '1.18')
verlst.grid(row = 0, column = 1)
verlst.current(3)
def ret_lang(ver):
    with open(f'lang/{ver}.json') as f:
        s = f.read()
    s = json.loads(s)
    return s
def init():
    global v14, v16, v17, v18
    v14 = ret_lang('1.14.4')
    v16 = ret_lang('1.16.5')
    v17 = ret_lang('1.17.1')
    v18 = ret_lang('1.18')
def gen_data():
    global blocks, effects, enchantments, entities, items
    blocks = [['方块', i['name'], get_key(verlst.get(), f'block.minecraft.{i["name"]}'), i['id']] for i in md_inst.blocks_list if get_key(verlst.get(), f'block.minecraft.{i["name"]}')]
    effects = [['状态效果', i['name'], get_key(verlst.get(), f'effect.minecraft.{i["name"]}'), i['id']] for i in md_inst.effects_list if get_key(verlst.get(), f'effect.minecraft.{i["name"]}')]
    enchantments = [['附魔', i['name'], get_key(verlst.get(), f'enchantment.minecraft.{i["name"]}'), i['id']] for i in md_inst.enchantments_list if get_key(verlst.get(), f'enchantment.minecraft.{i["name"]}')]
    entities = [['实体', i['name'], get_key(verlst.get(), f'entity.minecraft.{i["name"]}'), i['id']] for i in md_inst.entities_list if get_key(verlst.get(), f'entity.minecraft.{i["name"]}')]
    items = [['物品', i['name'], get_key(verlst.get(), f'item.minecraft.{i["name"]}'), i['id']] for i in md_inst.items_list if get_key(verlst.get(), f'item.minecraft.{i["name"]}')]
def get_name(num):
    res = md_inst.find_item_or_block(num)
    if res:
        return res['name']
    return ''
def get_key(ver, key):
    s = eval(f'v{ver.split(".")[1]}')
    if key in s:
        return s[key]
    if key.split('.')[0] == 'item':
        key = 'block.' + '.'.join(key.split('.')[1:])
        if key in s:
            return s[key]
    return ''
def changeVer(event):
    global md_inst
    md_inst = md(verlst.get())
    gen_data()
verlst.bind('<<ComboboxSelected>>', changeVer)
init()
gen_data()
# -------------------------------------------
problem = StringVar()
def test_name():
    global all_things, problems, tries, score, right, total, entry
    all_things = blocks + effects + enchantments + entities + items
    problems = 1
    tries = 4
    score = 0
    right = 0
    total = 25
    entry = random.sample(all_things, 1)[0]
    t2 = Toplevel()
    t2.resizable(0, 0)
    problem.set(f'{problems}/{total}: {entry[0]} {entry[1]} #{entry[3]}')
    l1 = Label(t2, textvariable = problem)
    l1.pack()
    e1 = Entry(t2)
    e1.pack()
    def next_problem():
        global problem, entry, problems, tries, score
        e1.delete(0, 'end')
        if problems == total:
            messagebox.showinfo('', f'得分: {score}\n正确题数: {right}')
            t2.destroy()
        else:
            problems += 1
            tries = 4
            del all_things[all_things.index(entry)]
            entry = random.sample(all_things, 1)[0]
            problem.set(f'{problems}/{total}: {entry[0]} {entry[1]} #{entry[3]}')
    def pass_problem():
        messagebox.showinfo('', f'本题跳过\n答案是{entry[2]}')
        next_problem()
    def submit():
        global tries, score, right
        if e1.get() == entry[2]:
            messagebox.showinfo('', '正确')
            score += tries
            right += 1
            next_problem()
        else:
            if tries > 1:
                messagebox.showinfo('', f'错误\n剩余{tries - 1}次机会')
                tries -= 1
            else:
                messagebox.showinfo('', f'本题错误\n答案是{entry[2]}')
                next_problem()
    b1 = Button(t2, text = '确定', command = submit)
    b1.pack()
    b2 = Button(t2, text = '跳过', command = pass_problem)
    b2.pack()
    t2.mainloop()
b1 = Button(t, text = '测试名称熟练度', command = test_name)
b1.grid(row = 1, column = 0)
# -------------------------------------------
def parse_recipe(recipe):
    res = [[int(i), [j for j in recipe[i]]] for i in recipe]
    for i in res:
        rlist = []
        for j in i[1]:
            del j['result']
            if 'inShape' in j:
                ent = j['inShape']
                for k in range(len(ent)):
                    for l in range(len(ent[k])):
                        ent[k][l] = get_name(ent[k][l])
                    if len(ent[k]) != 3:
                        ent[k] += [''] * (3 - len(ent[k]))
                if len(ent) != 3:
                    ent += [['', '', '']] * (3 - len(ent))
            else:
                ent = [get_name(k) for k in j['ingredients']]
            rlist.append(ent)
        i[1] = rlist
        i[0] = get_name(i[0])
    return res
problem2 = StringVar()
def flatten(li):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in li), [])
def ans_right(input_item):
    recipes = entry2[1]
    for i in recipes:
        if isinstance(i[0], list):
            if flatten(i) == input_item:
                return True
        else:
            if sorted([j for j in input_item if j]) == sorted(i):
                return True
    return False
def test_recipe():
    global all_recipe, problems2, tries2, score2, right2, total2, entry2
    all_recipe = parse_recipe(copy.deepcopy(md_inst.recipes))
    problems2 = 1
    tries2 = 5
    score2 = 0
    right2 = 0
    total2 = 10
    entry2 = random.sample(all_recipe, 1)[0]
    t2 = Toplevel()
    t2.resizable(0, 0)
    problem2.set(f'{problems2}/{total2}: 合成 {entry2[0]}\n有序且未占满3x3的配方请写在左上角')
    l1 = Label(t2, textvariable = problem2)
    l1.grid(row = 0, column = 0, columnspan = 3)
    e1 = Entry(t2)
    e1.grid(row = 1, column = 0)
    e2 = Entry(t2)
    e2.grid(row = 1, column = 1)
    e3 = Entry(t2)
    e3.grid(row = 1, column = 2)
    e4 = Entry(t2)
    e4.grid(row = 2, column = 0)
    e5 = Entry(t2)
    e5.grid(row = 2, column = 1)
    e6 = Entry(t2)
    e6.grid(row = 2, column = 2)
    e7 = Entry(t2)
    e7.grid(row = 3, column = 0)
    e8 = Entry(t2)
    e8.grid(row = 3, column = 1)
    e9 = Entry(t2)
    e9.grid(row = 3, column = 2)
    def next_problem():
        global problem2, entry2, problems2, tries2, score2
        e1.delete(0, 'end')
        e2.delete(0, 'end')
        e3.delete(0, 'end')
        e4.delete(0, 'end')
        e5.delete(0, 'end')
        e6.delete(0, 'end')
        e7.delete(0, 'end')
        e8.delete(0, 'end')
        e9.delete(0, 'end')
        if problems2 == total2:
            messagebox.showinfo('', f'得分: {score2}\n正确题数: {right2}')
            t2.destroy()
        else:
            problems2 += 1
            tries2 = 5
            del all_recipe[all_recipe.index(entry2)]
            entry2 = random.sample(all_recipe, 1)[0]
            problem2.set(f'{problems2}/{total2}: 合成 {entry2[0]}\n有序且未占满3x3的配方请写在左上角')
    def pass_problem():
        messagebox.showinfo('', f'本题跳过\n答案是{"或".join([str(i) for i in entry2[1]])}')
        next_problem()
    def submit():
        global tries2, score2, right2
        if ans_right([e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get(), e8.get(), e9.get()]):
            messagebox.showinfo('', '正确')
            score2 += tries2 * 2
            right2 += 1
            next_problem()
        else:
            if tries2 > 1:
                messagebox.showinfo('', f'错误\n剩余{tries2 - 1}次机会')
                tries2 -= 1
            else:
                messagebox.showinfo('', f'本题错误\n答案是{"或".join([str(i) for i in entry2[1]])}')
                next_problem()
    b1 = Button(t2, text = '确定', command = submit)
    b1.grid(row = 4, column = 0)
    b2 = Button(t2, text = '跳过', command = pass_problem)
    b2.grid(row = 4, column = 2)
    t2.mainloop()
b2 = Button(t, text = '测试配方熟练度', command = test_recipe)
b2.grid(row = 1, column = 1)
problem3 = StringVar()
def test_calc():
    global problem3, score3, total3, num, right3, problems3, tries3
    problems3 = 1
    tries3 = 5
    score3 = 0
    right3 = 0
    total3 = 20
    num = random.randint(65, 3456)
    t2 = Toplevel()
    t2.resizable(0, 0)
    problem3.set(f'{problems3}/{total3}: {num}个64堆叠物品是多少组多少个\n(若a组+b个则填入a+b)')
    l1 = Label(t2, textvariable = problem3)
    l1.pack()
    e1 = Entry(t2)
    e1.pack()
    def next_problem():
        global problem3, problems3, tries3, score3, num
        e1.delete(0, 'end')
        if problems3 == total3:
            messagebox.showinfo('', f'得分: {score3}\n正确题数: {right3}')
            t2.destroy()
        else:
            problems3 += 1
            tries3 = 5
            num = random.randint(65, 3456)
            problem3.set(f'{problems3}/{total3}: {num}个64堆叠物品是多少组多少个\n(若a组+b个则填入a+b)')
    def pass_problem():
        messagebox.showinfo('', f'本题跳过\n答案是{num // 64}+{num % 64}')
        next_problem()
    def submit():
        global tries3, score3, right3
        if e1.get() == f'{num // 64}+{num % 64}':
            messagebox.showinfo('', '正确')
            score3 += tries3
            right3 += 1
            next_problem()
        else:
            if tries3 > 1:
                messagebox.showinfo('', f'错误\n剩余{tries3 - 1}次机会')
                tries3 -= 1
            else:
                messagebox.showinfo('', f'本题错误\n答案是{num // 64}+{num % 64}')
                next_problem()
    b1 = Button(t2, text = '确定', command = submit)
    b1.pack()
    b2 = Button(t2, text = '跳过', command = pass_problem)
    b2.pack()
    t2.mainloop()
b3 = Button(t, text = '测试计算熟练度', command = test_calc)
b3.grid(row = 2, column = 0)
def find_name():
    t2 = Tk()
    l1 = Label(t2, text = '数字ID:')
    l1.grid(row = 0, column = 0)
    e1 = Entry(t2)
    e1.grid(row = 0, column = 1)
    t1 = Text(t2)
    def process_get():
        t1.delete(1.0, 'end')
        t1.insert('end', get_name(int(e1.get())))
    b1 = Button(t2, text = '查询', command = process_get)
    b1.grid(row = 0, column = 2)
    t1.grid(row = 1, column = 0, columnspan = 3)
b0 = Button(t, text = '通过数字ID查询物品ID', command = find_name)
b0.grid(row = 2, column = 1)#, columnspan = 2)
t.mainloop()
