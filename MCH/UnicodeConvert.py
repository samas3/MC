def char2unicode(x):
    s = ''
    for i in x:
        s += ('\\u%4s' % str(hex(ord(i)))[2:]).replace(' ', '0')
    return s
def unicode2char(x):
    lst = x.split('\\u')[1:]
    s = ''
    for i in lst:
        s += chr(int(i, base = 16))
    return s
