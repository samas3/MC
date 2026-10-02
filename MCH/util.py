import os
from functools import partial
from typing import Iterable
from urllib.request import urlopen
import requests
# import time
from bs4 import BeautifulSoup
from traceback import format_exc
import re, html, json, sys
DEBUG = 0
def debug(x: int):
    global DEBUG
    DEBUG = x
def copy_url(url: str, path: str = '.\\', maxsize: int = 1048576):
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
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        return r.text
    except Exception as e:
        print("Get HTML Text Failed!", e)
        return 0
def translate(to_translate, from_language, to_language):
    base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}"
    url = base_url.format(to_language, from_language, to_translate)
    html = getHTMLText(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
    try:
        result = soup.find_all("div", {"class":"result-container"})[0].text
    except Exception as e:
        print("Translation Failed!", e)
        result = ""
    return result
def trans(text, f, dest):
    txt = text
    try:
        return translate(txt, f, dest)
    except Exception as e:
        raise e
LANG = {'af': '南非语', 'af-ZA': '南非语', 'ar': '阿拉伯语', 'ar-AE': '阿拉伯语(阿联酋)', 'ar-BH': '阿拉伯语(巴林)', 'ar-DZ': '阿拉伯语(阿尔及利亚)', 'ar-EG': '阿拉伯语(埃及)', 'ar-IQ': '阿拉伯语(伊拉克)', 'ar-JO': '阿拉伯语(约旦)', 'ar-KW': '阿拉伯语(科威特)', 'ar-LB': '阿拉伯语(黎巴嫩)', 'ar-LY': '阿拉伯语(利比亚)', 'ar-MA': '阿拉伯语(摩洛哥)', 'ar-OM': '阿拉伯语(阿曼)', 'ar-QA': '阿拉伯语(卡塔尔)', 'ar-SA': '阿拉伯语(沙特阿拉伯)', 'ar-SY': '阿拉伯语(叙利亚)', 'ar-TN': '阿拉伯语(突尼斯)', 'ar-YE': '阿拉伯语(也门)', 'az': '阿塞拜疆语', 'az-AZ': '阿塞拜疆语(西里尔文)', 'be': '比利时语', 'be-BY': '比利时语', 'bg': '保加利亚语', 'bg-BG': '保加利亚语', 'bs-BA': '波斯尼亚语(拉丁文，波斯尼亚和黑塞哥维那)', 'ca': '加泰隆语', 'ca-ES': '加泰隆语', 'cs': '捷克语', 'cs-CZ': '捷克语', 'cy': '威尔士语', 'cy-GB': '威尔士语', 'da': '丹麦语', 'da-DK': '丹麦语', 'de': '德语', 'de-AT': '德语(奥地利)', 'de-CH': '德语(瑞士)', 'de-DE': '德语(德国)', 'de-LI': '德语(列支敦士登)', 'de-LU': '德语(卢森堡)', 'dv': '第维埃语', 'dv-MV': '第维埃语', 'el': '希腊语', 'el-GR': '希腊语', 'en': '英语', 'en-AU': '英语(澳大利亚)', 'en-BZ': '英语(伯利兹)', 'en-CA': '英语(加拿大)', 'en-CB': '英语(加勒比海)', 'en-GB': '英语(英国)', 'en-IE': '英语(爱尔兰)', 'en-JM': '英语(牙买加)', 'en-NZ': '英语(新西兰)', 'en-PH': '英语(菲律宾)', 'en-TT': '英语(特立尼达)', 'en-US': '英语(美国)', 'en-ZA': '英语(南非)', 'en-ZW': '英语(津巴布韦)', 'eo': '世界语', 'es': '西班牙语', 'es-AR': '西班牙语(阿根廷)', 'es-BO': '西班牙语(玻利维亚)', 'es-CL': '西班牙语(智利)', 'es-CO': '西班牙语(哥伦比亚)', 'es-CR': '西班牙语(哥斯达黎加)', 'es-DO': '西班牙语(多米尼加共和国)', 'es-EC': '西班牙语(厄瓜多尔)', 'es-ES': '西班牙语(国际)', 'es-GT': '西班牙语(危地马拉)', 'es-HN': '西班牙语(洪都拉斯)', 'es-MX': '西班牙语(墨西哥)', 'es-NI': '西班牙语(尼加拉瓜)', 'es-PA': '西班牙语(巴拿马)', 'es-PE': '西班牙语(秘鲁)', 'es-PR': '西班牙语(波多黎各(美))', 'es-PY': '西班牙语(巴拉圭)', 'es-SV': '西班牙语(萨尔瓦多)', 'es-UY': '西班牙语(乌拉圭)', 'es-VE': '西班牙语(委内瑞拉)', 'et': '爱沙尼亚语', 'et-EE': '爱沙尼亚语', 'eu': '巴士克语', 'eu-ES': '巴士克语', 'fa': '法斯语', 'fa-IR': '法斯语', 'fi': '芬兰语', 'fi-FI': '芬兰语', 'fo': '法罗语', 'fo-FO': '法罗语', 'fr': '法语', 'fr-BE': '法语(比利时)', 'fr-CA': '法语(加拿大)', 'fr-CH': '法语(瑞士)', 'fr-FR': '法语(法国)', 'fr-LU': '法语(卢森堡)', 'fr-MC': '法语(摩纳哥)', 'gl': '加里西亚语', 'gl-ES': '加里西亚语', 'gu': '古吉拉特语', 'gu-IN': '古吉拉特语', 'he': '希伯来语', 'he-IL': '希伯来语', 'hi': '印地语', 'hi-IN': '印地语', 'hr': '克罗地亚语', 'hr-BA': '克罗地亚语(波斯尼亚和黑塞哥维那)', 'hr-HR': '克罗地亚语', 'hu': '匈牙利语', 'hu-HU': '匈牙利语', 'hy': '亚美尼亚语', 'hy-AM': '亚美尼亚语', 'id': '印度尼西亚语', 'id-ID': '印度尼西亚语', 'is': '冰岛语', 'is-IS': '冰岛语', 'it': '意大利语', 'it-CH': '意大利语(瑞士)', 'it-IT': '意大利语(意大利)', 'ja': '日语', 'ja-JP': '日语', 'ka': '格鲁吉亚语', 'ka-GE': '格鲁吉亚语', 'kk': '哈萨克语', 'kk-KZ': '哈萨克语', 'kn': '卡纳拉语', 'kn-IN': '卡纳拉语', 'ko': '朝鲜语', 'ko-KR': '朝鲜语', 'kok': '孔卡尼语', 'kok-IN': '孔卡尼语', 'ky': '吉尔吉斯语', 'ky-KG': '吉尔吉斯语(西里尔文)', 'lt': '立陶宛语', 'lt-LT': '立陶宛语', 'lv': '拉脱维亚语', 'lv-LV': '拉脱维亚语', 'mi': '毛利语', 'mi-NZ': '毛利语', 'mk': '马其顿语', 'mk-MK': '马其顿语(FYROM)', 'mn': '蒙古语', 'mn-MN': '蒙古语(西里尔文)', 'mr': '马拉地语', 'mr-IN': '马拉地语', 'ms': '马来语', 'ms-BN': '马来语(文莱达鲁萨兰)', 'ms-MY': '马来语(马来西亚)', 'mt': '马耳他语', 'mt-MT': '马耳他语', 'nb': '挪威语(伯克梅尔)', 'nb-NO': '挪威语(伯克梅尔)(挪威)', 'nl': '荷兰语', 'nl-BE': '荷兰语(比利时)', 'nl-NL': '荷兰语(荷兰)', 'nn-NO': '挪威语(尼诺斯克)(挪威)', 'ns': '北梭托语', 'ns-ZA': '北梭托语', 'pa': '旁遮普语', 'pa-IN': '旁遮普语', 'pl': '波兰语', 'pl-PL': '波兰语', 'pt': '葡萄牙语', 'pt-BR': '葡萄牙语(巴西)', 'pt-PT': '葡萄牙语(葡萄牙)', 'qu': '克丘亚语', 'qu-BO': '克丘亚语(玻利维亚)', 'qu-EC': '克丘亚语(厄瓜多尔)', 'qu-PE': '克丘亚语(秘鲁)', 'ro': '罗马尼亚语', 'ro-RO': '罗马尼亚语', 'ru': '俄语', 'ru-RU': '俄语', 'sa': '梵文', 'sa-IN': '梵文', 'se': '北萨摩斯语', 'se-FI': '伊那里萨摩斯语(芬兰)', 'se-NO': '南萨摩斯语(挪威)', 'se-SE': '南萨摩斯语(瑞典)', 'sk': '斯洛伐克语', 'sk-SK': '斯洛伐克语', 'sl': '斯洛文尼亚语', 'sl-SI': '斯洛文尼亚语', 'sq': '阿尔巴尼亚语', 'sq-AL': '阿尔巴尼亚语', 'sr-BA': '塞尔维亚语(西里尔文，波斯尼亚和黑塞哥维那)', 'sr-SP': '塞尔维亚(西里尔文)', 'sv': '瑞典语', 'sv-FI': '瑞典语(芬兰)', 'sv-SE': '瑞典语', 'sw': '斯瓦希里语', 'sw-KE': '斯瓦希里语', 'syr': '叙利亚语', 'syr-SY': '叙利亚语', 'ta': '泰米尔语', 'ta-IN': '泰米尔语', 'te': '泰卢固语', 'te-IN': '泰卢固语', 'th': '泰语', 'th-TH': '泰语', 'tl': '塔加路语', 'tl-PH': '塔加路语(菲律宾)', 'tn': '茨瓦纳语', 'tn-ZA': '茨瓦纳语', 'tr': '土耳其语', 'tr-TR': '土耳其语', 'ts': '宗加语', 'tt': '鞑靼语', 'tt-RU': '鞑靼语', 'uk': '乌克兰语', 'uk-UA': '乌克兰语', 'ur': '乌都语', 'ur-PK': '乌都语', 'uz': '乌兹别克语', 'uz-UZ': '乌兹别克语(西里尔文)', 'vi': '越南语', 'vi-VN': '越南语', 'xh': '班图语', 'xh-ZA': '班图语', 'zh': '中文', 'zh-CN': '中文(简体)', 'zh-HK': '中文(香港)', 'zh-MO': '中文(澳门)', 'zh-SG': '中文(新加坡)', 'zh-TW': '中文(繁体)', 'zu': '祖鲁语', 'zu-ZA': '祖鲁语'}

if __name__ == '__main__':
    print(get_info("https://www.mcmod.cn/class/2.html"))
