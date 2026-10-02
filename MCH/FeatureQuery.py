from util import *
import html as h
def bug(x):
    s = ''
    link = 'https://bugs.mojang.com/browse/{}'.format(x)
    # print('Link: {}'.format(link))
    s += 'Link: {}\n'.format(link)
    html = get_html(link)
    pos = findSubstring(html, '<h1 id="summary-val">')  + len('<h1 id="summary-val">')
    posend = findSubstring(html, '</h1>', begin = pos)
    bug_title = h.unescape(html[pos:posend])
    if len(bug_title) > 1000:
        # print('Not found')
        s += 'Not found'
        return s
    else:
        pos = findSubstring(html, '<div class="user-content-block">')  + len('<div class="user-content-block">')
        pos = findSubstring(html, '<p>', begin = pos) + len('<p>')
        posend = findSubstring(html, '</p>', begin = pos)
        bug_desc = filter_tags(h.unescape(html[pos:posend]))
        pos = findSubstring(html, '<span id="versions-val" class="value">') + len('<span id="versions-val" class="value">')
        pos = findSubstring(html, '<span title="', begin = pos) + len('<span title="')
        pos = findSubstring(html, '">', begin = pos) + len('">')
        posend = findSubstring(html, '</span>', begin = pos)
        affect = html[pos:posend]
        '''pos = findSubstring(html, '<div id="customfield_12200-val" class="value type-select" data-fieldtype="select" data-fieldtypecompletekey="com.atlassian.jira.plugin.system.customfieldtypes:select">') + len('<div id="customfield_12200-val" class="value type-select" data-fieldtype="select" data-fieldtypecompletekey="com.atlassian.jira.plugin.system.customfieldtypes:select">')
        posend = findSubstring(html, '</div>', begin = pos)
        priority = html[pos:posend].strip()'''
        pos = findSubstring(html, '<span id="resolution-val"') + len('<span id="resolution-val"')
        pos = findSubstring(html, '>', begin = pos) + len('>')
        posend = findSubstring(html, '</span>', begin = pos)
        res = html[pos:posend].strip()
        pos = findSubstring(html, '<span id="fixfor-val" class="value">') + len('<span id="fixfor-val" class="value">')
        posend = findSubstring(html, '</span>', begin = pos)
        fix = html[pos:posend].strip()
        if '</a>' in fix:
            pos = findSubstring(html, '<a', begin = pos) + len('<a')
            pos = findSubstring(html, '">', begin = pos) + len('">')
            posend = findSubstring(html, '</a>', begin = pos)
            fix = html[pos:posend]
        # if res == 'Duplicate' or res == 'Unresolved' or res == 'Incomplete' or res == 'Invalid':
        if len(fix) > 100:
            # print('Title: {}\nDesc: {}\nAffects Version(s): {}\nResolution: {}'
            #   .format(bug_title, bug_desc, affect, res))
            s += 'Title: {}\nDesc: {}\nAffects Version(s): {}\nResolution: {}\n'.format(bug_title, bug_desc, affect, res)
            return s
            # print(fix)
        else:
            # print('Title: {}\nDesc: {}\nAffects Version(s): {}\nResolution: {}\nFix Version(s): {}'
            #       .format(bug_title, bug_desc, affect, res, fix))
            s += 'Title: {}\nDesc: {}\nAffects Version(s): {}\nResolution: {}\nFix Version(s): {}'.format(bug_title, bug_desc, affect, res, fix)
            return s
if __name__ == '__main__':
    x = input('Bug ID:')
    print(bug(x))
