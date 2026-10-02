import os, zipfile, json
ver = input('版本名称: ')
p = f'.minecraft/versions/{ver}/mods'
files = os.listdir(p)
lastid = ''
lastver = ''
fn = ''
for i in files:
    file = p + '/' + i
    f = zipfile.ZipFile(file)
    if os.path.getsize(file) == 0:
        print('删除空文件 ' + i)
        os.remove(file)
    elif 'fabric.mod.json' in f.namelist():
        mod_file = f.read('fabric.mod.json')
        js = json.loads(mod_file, strict=False)
        if 'depends' in js and 'minecraft' in js['depends']:
            print(js['id'] + '@' + js['version'], 'Minecraft 版本:', js['depends']['minecraft'])
        if js['id'] == lastid:
            print('重复Mod: %s@%s 和 %s@%s' % (lastid, lastver, js['id'], js['version']))
            ch = input('删除第(1)个/第(2)个:')
            if ch == '1':
                os.remove(fn)
            else:
                os.remove(file)
        lastid = js['id']
        lastver = js['version']
        fn = file
print('共 %s 个Mod' % len(os.listdir(p)))
