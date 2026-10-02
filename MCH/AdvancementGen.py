from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
import re, string, os, requests

size = 32
listsize = 32
page_url = r'https://minecraft.gamepedia.com/Module:InvSprite'
sprite_url = r'https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/InvSprite.png/revision/latest'
base_url = r'https://i.loli.net/2020/09/27/zwIY6nVJRmqbHaL.png' #使用SM.MS储存成就底图
catdict = {}
itemdict = {}

def init():
    #创建资源文件夹...
    if (not os.path.exists(r'./adv-maker/')):
        os.mkdir(r'./adv-maker/')
    
    #下载图标文件...
    if (not os.path.exists(r'./adv-maker/inv-sprite.png')):
        print('Downloading Sprites file...')
        urlretrieve(sprite_url, './adv-maker/inv-sprite.png')

    #下载成就底图...
    if (not os.path.exists(r'./adv-maker/advancement-base.png')):
        print('Downloading Advancement Background Image...')
        r = requests.get(base_url)
        with open(r'./adv-maker/advancement-base.png','wb') as bim:
            bim.write(r.content)
    
    #把Wiki上的Lua脚本先搞出来...
    if (not os.path.exists(r'./adv-maker/pos-info.txt')):
        resp = urlopen(page_url)
        print('Downloading HTML file...')
        cont = resp.read()
        soup = BeautifulSoup(cont,'html.parser')
        print('Extracting Lua script...')
        src = soup.select(".mw-code")[0].prettify().replace('&','&')
        print('Saving the script...')
        with open(r'./adv-maker/pos-info.txt','w+') as f:
            f.write(src)

    print('Reading Lua script...')
    f = open(r'./adv-maker/pos-info.txt','r')
    src = f.read()

    f.close()
    print('Getting Position Info...')
    #...然后提取物品名称、物品分类、在图中的位置等信息，存起来
    pat1 = re.compile(r'^\s*{ name = \'(.*)\', id = (.*) }',re.M)
    pat2 = re.compile(r'^\s*(.*) = { pos = (.*), section = (.*) }',re.M)

    res1 = pat1.findall(src)
    res2 = pat2.findall(src)

    for cat in res1:
        catdict[str(cat[1])] = cat[0]

    for itm in res2:
        #print('%-45s%-35s%-20s' %(itm[0][2:-2] if(itm[0][0]=='[') else itm[0], catdict[itm[2]], itm[1])) 如果要显示物品列表，把这行的注释符号去掉
        itemdict[(itm[0][2:-2] if(itm[0][0]=='[') else itm[0])] = int(itm[1])

def trans_paste(bg,fg,box=(0,0)):
    trans = Image.new("RGBA",bg.size)
    trans.paste(fg,box,mask=fg)
    nim = Image.alpha_composite(bg,trans)
    return nim

def show(tar="???",text1="Advancement Made!",color1=(255,255,0),text2="Minecraft Advancements!",color2=(255,255,255),file='advancement.png'):
    idx = 1
    if (tar in itemdict):
        idx = itemdict[tar]
    posx = int((idx - 1) // listsize)
    posy = (idx - 1 + listsize) % listsize
    
    print(idx,posx,posy)
    sprite = srci.crop((posy*size,posx*size,(posy+1)*size,(posx+1)*size))

    box = (17, 16, 17 + size, 16 + size)
    resi = trans_paste(advi,sprite,box)
    drw = ImageDraw.Draw(resi)
    drw.text((60, 12), text1, font=fnt, fill=color1)
    drw.text((60, 34), text2, font=fnt, fill=color2)
    resi.show()
    resi.save('.\\{}'.format(file))

def adv(pic,t1,t2,file,t1c=(255,255,0),t2c=(255,255,255)):
    init()
    
    global srci, advi, fnt
    srci = Image.open('./adv-maker/inv-sprite.png').convert('RGBA')
    advi = Image.open('./adv-maker/advancement-base.png').convert('RGBA')
    fnt = ImageFont.truetype(r'minecraft.otf', 20)
    #fnt = ImageFont.truetype("simsun.ttc", 19) Use this to display Chinese characters
    show(tar=pic,text1=t1,text2=t2,file=file)
    #show('Wooden Pickaxe',text2='Stone Age')
if __name__ == '__main__':
    pic = input('输入图标名:')
    t1 = input('文本1:')
    t2 = input('文本2:')
    file = input('保存文件名:')
    adv(pic, t1, t2, file)
