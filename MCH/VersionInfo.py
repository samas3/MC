from util import *
import json, time, datetime
def ver(num):
    def getTime(timestr):
        return time.strftime("%Y/%m/%d,%H:%M:%S(%a)", time.strptime(timestr[0:-7], '%Y-%m-%dT%H:%M:%S'))
    url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
    req = get_html(url)
    versions = json.loads(req)
    s = ''
    '''print('Welcome to the Minecraft Version Checker!\nThis week is %s%s%s\n' %(datetime.datetime.now().isocalendar()[0]-2000, 'w', str(datetime.datetime.now().isocalendar()[1]).zfill(2)))
    print('Latest Release:  ',versions['latest']['release'])
    print('Latest Snapshot: ',versions['latest']['snapshot'],'\n\nRecent Versions:')
    print('%-21s%-14s%-30s' % ('Version Id:', 'Type:', 'Release Time(GMT):'))'''
    s += 'Welcome to the Minecraft Version Checker!\nThis week is %s%s%s\n' %(datetime.datetime.now().isocalendar()[0]-2000, 'w', str(datetime.datetime.now().isocalendar()[1]).zfill(2))
    s += 'Latest Release:  ' + versions['latest']['release'] + '\n'
    s += 'Latest Snapshot: ' + versions['latest']['snapshot'] + '\n\nRecent Versions:\n'
    s += 'Showing {} versions\n'.format(min(num, len(versions['versions'])))
    s += '%-21s%-14s%-30s\n' % ('Version Id:', 'Type:', 'Release Time(GMT):')
    i = 0
    for ver in versions['versions']:
        # print('%-21s%-14s%-30s' % (ver['id'], ver['type'], getTime(ver['releaseTime'])))
        s += '%-21s%-14s%-30s\n' % (ver['id'], ver['type'], getTime(ver['releaseTime']))
        i += 1
        if i == min(num, len(versions['versions'])):
            return s
if __name__ == '__main__':
    print(ver(10))
