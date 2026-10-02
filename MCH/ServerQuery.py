from tkinter import *
from mcstatus import MinecraftServer as ms, MinecraftBedrockServer as mbs
import re
def sq():
    if __name__ == '__main__':
        t = Tk()
    else:
        t = Toplevel()
    t.title('服务器查询')
    v1 = IntVar()
    v1.set(1)
    def c1():
        v1.set(1)
    def c2():
        v1.set(2)
    r1 = Radiobutton(t, text = 'Java版', variable = v1, value = 1, command = c1)
    r2 = Radiobutton(t, text = '基岩版', variable = v1, value = 2, command = c2)
    r1.grid(row = 0, column = 0)
    r2.grid(row = 0, column = 1)
    l1 = Label(t, text = '服务器IP:')
    l1.grid(row = 1, column = 0)
    e1 = Entry(t)
    e1.grid(row = 1, column = 1)
    t1 = Text(t)
    def process():
        t1.delete(1.0, 'end')
        if v1.get() == 1:
            svr = ms.lookup(e1.get())
        else:
            svr = mbs.lookup(e1.get())
        try:
            st = svr.status()
        except:
            t1.insert('end', 'Not found!\nIf you believe this IP exists, please check your network connection\nIf ServerType is Bedrock try adding default port 19132')
        if v1.get() == 1:
            desc = st.description
            ping = st.latency
            players = st.players
            ver = st.version
            other = st.raw
            rawdesc = re.sub(re.compile('§.'), '', desc)
            del other['version']
            del other['players']
            del other['description']
            del other['favicon']
            t1.insert('end', '服务器MOTD: {}\n不含格式字符的MOTD: {}\n延迟: {}ms\n玩家: {}/{}\n版本: {}(协议版本 {})\n其它: {}'.format(desc, rawdesc, ping, players.online, players.max, ver.name, ver.protocol, other))
        else:
            desc = st.motd
            mp = st.map
            ping = st.latency
            gm = st.gamemode
            po = st.players_online
            pm = st.players_max
            ver = st.version
            rawdesc = re.sub(re.compile('§.'), '', desc)
            t1.insert('end', '服务器MOTD: {}\n不含格式字符的MOTD: {}\n游戏模式: {}\n延迟: {}ms\n玩家: {}/{}\n版本: {} {} {}(协议版本 {})'.format(desc, rawdesc, gm, round(ping, 3), po, pm, mp, ver.brand, ver.version, ver.protocol))
    b1 = Button(t, text = '查询', command = process)
    b1.grid(row = 2, column = 0, columnspan = 2)
    t1.grid(row = 3, column = 0, columnspan = 2)
    t.mainloop()
if __name__ == '__main__':
    sq()
