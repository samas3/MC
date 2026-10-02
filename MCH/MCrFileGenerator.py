import json
def mfg(file, modid, modname, ver, author, url, generator, package, mcrver):
    with open(file + '.mcreator', 'w') as f:
        res = {'workspaceSettings':{'modid':modid, 'modName':modname, 'version':ver,
            'author':author, 'license':'Academic Free License v3.0',
        'disableForgeVersionCheck':True, 'serverSideOnly':False,
        'requiredMods':[], 'dependencies':[], 'dependants':[],
        'mcreatorDependencies':[], 'currentGenerator':generator,
        'modElementsPackage':package, 'lockBaseModFiles':False},
        'mcreatorVersion':mcrver}
        json.dump(res, f)
if __name__ == '__main__':
    file = input('mcreator文件名:')
    modid = input('Mod ID:')
    modname = input('Mod名称:')
    ver = input('版本:')
    author = input('作者:')
    url = input('Mod URL:')
    generator = input('生成器版本:')
    package = input('Mod包名:')
    mcrver = input('Mcreator版本(格式:主版本+0+副版本+开发版本 如202100103117):')
    mfg(file, modid, modname, ver, author, url, generator, package, mcrver)
