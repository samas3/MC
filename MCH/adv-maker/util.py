import os
from functools import partial
from typing import Iterable
from urllib.request import urlopen
import requests
# import time
from bs4 import BeautifulSoup
from traceback import format_exc
import re, html
DEBUG = 0
def debug(x: int):
    global DEBUG
    DEBUG = x
def copy_url(url: str, path: str = '.\\', maxsize: int = 32768):
    """Copy data from a url to a local file."""
    response = urlopen(url)
    size = response.info()['Content-length']
    file = url.split('/')[-1]
    path = os.path.join(path, file)
    with open(path, 'wb') as dest_file:
        for data in iter(partial(response.read, maxsize), b""):
            dest_file.write(data)
            if DEBUG:
                print('Downloaded {}/{} bytes'.format(os.path.getsize(path), size))
            if os.path.getsize(path) == size:
                return
'''def findStr(string, subStr, findCnt):
    listStr = string.split(subStr, findCnt)
    if len(listStr) <= findCnt:
        return -1
    return len(string) - len(listStr[-1]) - len(subStr)'''
sub = "&__cf_chl_jschl_tk__=e370c2bf6f0b0062cb95c67b5028273c4b2e3f7d-1590543375-0-AZx7xIyGHM3BMOuSQvOr_DkA6mvkweFvko2F1bSzLyFhUFA4fV4bo9roeIxfPhUhQbqQcnCTYDM0hv-jgBijPoOeKExKLC2gRy1D-li1L0EbKvXSK9hOvS8_VCC6IJ3sWUkqnMFCA049SSSlS3Ov1voN1m58y2OVExmc3PR-YvY0BFF87dfMt6QHl437cIHpyYIFhxRBlXP1EzxyHAwySHthbqV8um5b7-UD5FEo5-eJkXmkhzalniOsjRZfEyTXIi6NTLDSB-H82KI0LR9_a-62QtIRQBSfPB-k7abX7iudr0sVCVyI9tXCCV0Fkutsu0GzycJxaUWxEjTDNnHkEjU"
def findSubstring(string, substring, times = 1, begin = 0):
    current = begin
    for i in range(1, times + 1):
        current = string.find(substring, current + 1)
        if current == -1:
            return -1
    return current
def get_html(url, agent = 'random'):
    try:
        res = requests.get(url = url)
        res.encoding = 'utf-8'
        return res.text
    except:
        return format_exc()
def get_info(url, agent = 'random'):
    try:
        res = requests.get(url = url)
        res.encoding = 'utf-8'
        # time.sleep(2)
        soup = BeautifulSoup(res.text, 'html.parser')
        if 'mcmod' in url:
            # print("mcmod附加功能")
            t = res.text
            beg = t.find('<ul class="col-lg-12">')
            end = findSubstring(t, '</ul>', 15, 0)
            link = t.find('<li class="col-lg-12 urllink">')
            ver = t.find('支持的MC版本:') + len('支持的MC版本:')
            vere = t.find('</ul>', ver)
            version = t[ver:vere]
            version = version.replace('<li class="text-danger">', '').replace('<ul>', '') \
                .replace('</li>', ' ').replace('<li >', '')
            version = version.split()
            curse = t.find('CurseForge', link)
            if curse < 0:
                clink = '-1'
            else:
                clb = t.find('//', curse) + 2
                cl = t.find('</', clb)
                clink = t[clb:cl]
            # https://wiki.biligame.com/mc
            git = t.find('GitHub', link)
            if git < 0:
                glink = '-1'
            else:
                glb = t.find('//', git) + 2
                gl = t.find('</', glb)
                glink = t[glb:gl]
            guanfang = t.find('官方', link)
            if guanfang < 0:
                flink = '-1'
            else:
                flb = t.find('//', guanfang) + 2
                fl = t.find('</', flb)
                flink = t[flb:fl]
            mf = t.find('Minecraft Forum', link)
            if mf < 0:
                mlink = '-1'
            else:
                mlb = t.find('//', mf) + 2
                ml = t.find('</', mlb)
                mlink = t[mlb:ml]
            wiki = t.find('WIKI', link)
            if wiki < 0:
                wlink = '-1'
            else:
                wlb = t.find('//', wiki) + 2
                wl = t.find('</', wlb)
                wlink = t[wlb:wl]
            other = t.find('其他', link)
            if other < 0:
                olink = '-1'
            else:
                olb = t.find('//', other) + 2
                ol = t.find('</', olb)
                olink = t[olb:ol]
            bbs = t.find('MCBBS', link)
            if bbs < 0:
                blink = '-1'
            else:
                blb = t.find('//', bbs) + 2
                bl = t.find('</', blb)
                blink = t[blb:bl]
            lnkend = t.find('</ul>', link)
            if clink + glink + flink + mlink + wlink + olink + blink == 7 * '-1':
                return soup.title.text, version, '没有友情链接'
            ver = t.find('支持的MC版本:<ul>') + len('支持的MC版本:<ul>')
            ver_end = t.find('</ul>', ver)
            return soup.title.text, version, {'CurseForge':clink, 'GitHub':glink, 'Official':flink, 'Minecraft Forum':mlink, 'WIKI':wlink, 'Other':olink, 'MCBBS':blink} # res.text[beg:end + len('</ul>')]
        return soup.title.text, '-1', '-1'
    except Exception as e:
        # raise(e)
        return "出现错误! 错误: \n" + format_exc()
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=html.unescape(s)
    return s
def chinese_to_pinyin(x):
    y = ''
    dic = {}
    with open("unicode_pinyin.txt") as f:
        for i in f.readlines():
            dic[i.split()[0]] = i.split()[1]
    for i in x:
        i = str(i.encode('unicode_escape'))[-5:-1].upper()
        try:
            y += dic[i] + ' '
        except:
            y += str(i)+' '
    return y
def capital_unicode(x):
    y = []
    dic = {}
    with open("unicode_pinyin.txt") as f:
        for i in f.readlines():
            dic[i.split()[0].lower()] = i.split()[1:]
    cnt = 0
    lst = []
    tmp = []
    for i in x:
        i = i.encode('unicode_escape')
        q = str(i)[-5:-1]
        try:
            y.append([i[0] for i in dic[q]])
            tmp.append(cnt)
        except:
            y.append(i.decode())
            if tmp:
                lst.append(tmp)
                tmp = []
        cnt += 1
    if tmp:
        lst.append(tmp)
        tmp = []
    return y, lst
def capital(x):
    y = ''
    dic = {}
    with open("gbk.txt") as f:
        for i in f.readlines():
            dic[i.split()[0]] = i.split()[1].upper()
    cnt = 0
    lst = []
    tmp = []
    for i in x:
        try:
            y += dic[i][0]
            tmp.append(cnt)
        except:
            y += i
            if tmp:
                lst.append(tmp)
                tmp = []
        cnt += 1
    if tmp:
        lst.append(tmp)
        tmp = []
    return y, lst

if __name__ == '__main__':
    print(get_info("https://www.mcmod.cn/class/2.html"))
