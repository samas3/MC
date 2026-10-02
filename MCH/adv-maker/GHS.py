from util import capital_unicode
n = input('file:')
gh = ['JJ', 'JB', 'YJ', 'RF', 'JY', 'SJ', 'XJ', 'BQ', 'ZW', 'YD', 'HY', 'ZG', 'LC', 'GW', 'FG', 'SY', 'MG', 'QJ', 'XQ']
with open(n, encoding = 'utf-8') as f:
    s = f.read()
ans = []
l = s.split('\n')
cnt = 0
for i in l:
    cnt += 1
    ori = i
    ss, lst = capital_unicode(i)
    for j in lst:
        if len(j) < 2:
            continue
        for item in range(len(j) - 1):
            for k in gh:
                if k[0] in ss[j[item]] and k[1] in ss[j[item + 1]]:
                    ori = ori[:j[item]] + k + ori[j[item + 1] + 1:]
        # print(ori)
    ans.append(ori)
    print('%.2f%%' % (cnt / len(l) * 100))
with open('.'.join(n.split('.')[:-1]) + '_generated.' + n.split('.')[-1], 'w') as f:
    for i in ans:
        f.write(i + '\n')
