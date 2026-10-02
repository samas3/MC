from tkinter import *
import requests, json, time
# https://v1.hitokoto.cn
'''a	动画
b	漫画
c	游戏
d	文学
e	原创
f	来自网络
g	其他
h	影视
i	诗词
j	网易云
k	哲学
l	抖机灵'''
def yiyan():
    lst = {'a':'动画', 'b':'漫画', 'c':'游戏', 'd':'文学', 'e':'原创', 'f':'来自网络', 'g':'其他', 'h':'影视', 'i':'诗词', 'j':'网易云', 'k':'哲学', 'l':'抖机灵'}
    if __name__ == '__main__':
        t = Tk()
    else:
        t = Toplevel()
    t.title('一言')
    v1 = StringVar()
    l1 = Label(t, textvariable = v1, font = ('JetBrains Mono', 10))
    l1.pack()
    def refresh():
        hitokoto = requests.get('https://v1.hitokoto.cn')
        text = json.loads(hitokoto.text)
        idx = text['id']
        val = text['hitokoto']
        typex = lst[text['type']]
        fromx = text['from']
        from_who = '(' + text['from_who'] + ')' if text['from_who'] and text['from_who'] != fromx else ''
        string = f'{idx}: {val}\n——{fromx}{from_who} ({typex})'
        v1.set(string)
    refresh()
    b1 = Button(t, text = '刷新', command = refresh, relief = GROOVE)
    b1.pack()
    t.mainloop()
if __name__ == '__main__':
    yiyan()
