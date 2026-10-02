DEBUG = True
import zipfile, json, os
from util import *
isdir = 1
def all_file(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files
if not isdir:
    file = zipfile.ZipFile(name, 'r')
    # infolist = list(file.infolist())
    filelist = file.namelist()
def get_mod_type(zip_fl):
    if 'mcmod.info' in zip_fl:
        return 0
    if 'fabric.mod.json' in zip_fl:
        return 1
    if 'litemod.json' in zip_fl:
        return 2
    return -1
def get_mod_info(fname, mod_type):
    '''
    mod_type: 0 is forge mod, 1 is fabric mod, 2 is litemod
    '''
    file = zipfile.ZipFile(fname, 'r')
    # infolist = list(file.infolist())
    zip_fl = file.namelist()
    if mod_type == -1:
        return '没有模组介绍文件'
    if mod_type == 0:
        idx = zip_fl.index('mcmod.info')
        try:
            mcinfo = str(file.read(zip_fl[idx]), 'utf-8').replace('\n', '')
            js = json.loads(mcinfo)[0]
            if DEBUG:
                print(mcinfo)
        except json.decoder.JSONDecodeError:
            return 'mcmod.info不是合法的json格式'
        except KeyError:
            js = json.loads(mcinfo)
        except Exception as e:
            return '发生错误! ' + str(e)
        if 'modListVersion' in js and js['modListVersion'] == 2 or 'modListVersion' in js and js['modListVersion'] == '2':
            js = js['modList'][0]
        # print(js)
        mn = js['name']
        html = get_html('https://www.mcmod.cn/s?key=' + mn, 'random')
        npos = html.find('没有')
        nposend = html.find('。', npos) + 1
        link = None
        if html[npos:nposend]:
            link = '暂无'
        else:
            pos = html.find('地址：</span><span class="value">') + len('地址：</span><span class="value">')
            href = html.find('href="', pos) + len('href="')
            posend = html.find('">', pos)
            link = html[href:posend]
            if 'class' not in link:
                link = '暂无'
        keys = ['name', 'description', 'version', 'mcversion', 'url', 'authorList', 'parent', \
            'requiredMods', 'dependencies']
        for i in keys:
            if i not in js and i != 'authorList' and i != 'requiredMods' and i != 'dependencies':
                js[i] = '无'
            elif i not in js:
                js[i] = ['无']
        for k in js:
            if js[k] == '':
                js[k] = '无'
            elif js[k] == []:
                js[k] = ['无']
                # parent: {}\nrequiredMods: {}\n
                #  js['parent'], ','.join(js['requiredMods']),
        return '模组ID: {}\n模组名: {}\n描述: {}\n版本: {}\n适用的MC版本: {}\n模组URL: {}\n\
作者: {}\n依赖: {}\nMCMOD链接: {}'.format(js['modid'], js['name'], \
            js['description'], js['version'], js['mcversion'], js['url'], \
            js['authorList'], \
            ', '.join(js['dependencies']), link)
    elif mod_type == 2:
        idx = zip_fl.index('litemod.json')
        try:
            lm = str(file.read(zip_fl[idx]), 'utf-8').replace('\n', '')
            js = json.loads(lm)
            if DEBUG:
                print(lm)
        except Exception as e:
            return '发生错误! ' + str(e)
        mn = js['name']
        html = get_html('https://www.mcmod.cn/s?key=' + mn, 'random')
        npos = html.find('没有')
        nposend = html.find('。', npos) + 1
        link = None
        if html[npos:nposend]:
            link = '暂无'
        else:
            pos = html.find('地址：</span><span class="value">') + len('地址：</span><span class="value">')
            href = html.find('href="', pos) + len('href="')
            posend = html.find('">', pos)
            link = html[href:posend]
            if 'class' not in link:
                link = '暂无'
        return '名称: {}\n适用的MC版本: {}\n版本: {} 修订 \n作者: {}\n描述: {}\n\
类转换器类名: {}\nMCMOD链接: {}'.format(js['name'], js['mcversion'], js['version'], js['revision'], js['author'], \
            js['description'], ', '.join(js['classTransformerClasses']), link)
    else:
        idx = zip_fl.index('fabric.mod.json')
        try:
            fb = str(file.read(zip_fl[idx]), 'utf-8').replace('\n', '')
            js = json.loads(fb)
            if DEBUG:
                print(fb)
        except Exception as e:
            return '发生错误! ' + str(e)
        mn = js['name']
        html = get_html('https://www.mcmod.cn/s?key=' + mn, 'random')
        npos = html.find('没有')
        nposend = html.find('。', npos) + 1
        link = None
        keys = ['name', 'id', 'version', 'authors', 'contact', 'license', 'description', 'depends']
        for i in keys:
            if i not in js:
                js[i] = '暂无'
        if html[npos:nposend]:
            link = '暂无'
        else:
            pos = html.find('地址：</span><span class="value">') + len('地址：</span><span class="value">')
            href = html.find('href="', pos) + len('href="')
            posend = html.find('">', pos)
            link = html[href:posend]
            if 'class' not in link:
                link = '暂无'
        # entrypoints入口点
        return '名称: {}\nID: {}\n版本: {}\n作者: {}\n联系: {}\n许可: {}\n\
描述: {}\n依赖: {}\nMCMOD链接: {}'.format(js['name'], js['id'], js['version'], js['authors'], js['contact'],\
            js['license'], js['description'], js['depends'], link)
def dirget(d):
    global isdir
    s = ''
    if not os.path.isdir(d):
        return '不是目录'
    files = all_file(d)
    for i in files:
        ext = i.split('.')[-1]
        if ext != 'jar' and ext != 'zip' and ext != 'litemod':
            files.remove(i)
    # infos = []
    for i in files:
        fn = d + os.sep + i
        file = zipfile.ZipFile(fn, 'r')
        filelist = file.namelist()
        # infos.append(fn + '信息:')
        # print(fn + '信息:')
        s += fn + '信息:'
        # infos.append(get_mod_info(fn, get_mod_type(filelist)))
        # print(get_mod_info(fn, get_mod_type(filelist)))
        s += get_mod_info(fn, get_mod_type(filelist))
    # return '\n'.join(infos)
    return s
if __name__ == '__main__':
    name = input('输入目录名:')
    if not isdir:
        mt = get_mod_type(filelist)
        # print(get_mod_info(filelist, mt))
        get_mod_info(filelist, mt)
    else:
        print(dirget(name))
