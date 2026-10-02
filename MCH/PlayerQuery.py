from util import *
import json, time
from mojang import MojangAPI
def pq(x):
    s = ''
    link = 'https://playerdb.co/api/player/minecraft/{}'.format(x)
    html = json.loads(get_html(link))
    if html['success']:
        data = html['data']['player']
        uuid = data['id']
        name = data['username']
        hist = data['meta']['name_history']
        s += 'Name: {}\nUUID: {}\n'.format(name, uuid)
        for i in hist:
            n = i['name']
            if 'changedToAt' in i:
                ts = i['changedToAt']
                d = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts) / 1000))
                # print(n, d)
                s += n + ' ' + d
        profile = MojangAPI.get_profile(uuid)
        s += f'Skin URL: {profile.skin_url}\n'
        s += f'Skin model: {profile.skin_model}\n'
        s += f'Cape URL: {profile.cape_url}\n'
        return s
    else:
        # print('Not found')
        return 'Not found'
if __name__ == '__main__':
    x = input('Name:')
    print(pq(x))
