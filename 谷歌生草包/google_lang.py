from multiprocessing.dummy import Pool as ThreadPool
import re, json, sys, requests
#from fake_useragent import UserAgent
#TIMES = int(sys.argv[1])
TIMES = 6
'''def translate(text,dest):
    if text:
        aim_lang = dest
        try:
                #t = google_translator(timeout = 10,url_suffix = 'cn')
                t = Translator()
                translate_text = t.translate(text, aim_lang)
                return translate_text
        except Exception as e:
            print(e)'''
from bs4 import BeautifulSoup
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)#, header = {'User-Agent':str(UserAgent().random)})
        #r.raise_for_status()
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
with open('zh_cn.json') as f:
    dic = f.read()
dic = json.loads(dic)
# process
def dotrans(text, times):
    ans = text
    for i in range(times + times % 2):
        if i % 2:
            ans = trans(ans, 'en', 'zh-CN')
        else:
            ans = trans(ans, 'zh-CN', 'en')
    return ans.replace('％', '%').replace(' $ s', '$s').replace('%S', '%s').replace('% s', '%s').replace(' $', '$s')
for k, v in dic.items():
    end = dotrans(v, TIMES)
    while end == '':
        end = dotrans(v, TIMES)
    dic[k] = end
    print(k, end)
# end
dic = json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
with open('zh_cn2.json', 'w') as f:
    f.write(dic)
