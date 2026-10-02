from util import *
def wiki(x):
    s = ''
    link = 'https://minecraft.fandom.com/zh/wiki/{}'.format(x)
    # print('Link: {}'.format(link))
    s += 'Link: {}\n'.format(link)
    html = get_html(link)
    pos = findSubstring(html, '<div class="notaninfobox">') + len('<div class="notaninfobox">')
    pos = findSubstring(html, '</table>\n</div>', begin = pos) + len('</table></div>')
    pos = findSubstring(html, '<p><b>', begin = pos) + len('<p><b>')
    posend = findSubstring(html, '</p>', begin = pos)
    con = filter_tags(html[pos:posend])
    if not con.startswith('TYPE html>'):
        # print(con.strip())
        s += con.strip()
    else:
        # print('Not found')
        s += 'Not found'
    return s
if __name__ == '__main__':
    x = input('词条:')
    print(wiki(x))
