import json
file1 = input("请输入第一个文件名：")
file2 = input("请输入第二个文件名：")
with open(file1, 'r', encoding='utf-8') as f:
    data1 = json.load(f)
with open(file2, 'r', encoding='utf-8') as f:
    data2 = json.load(f)
key1 = set(data1.keys())
key2 = set(data2.keys())
with open('diff.txt', 'w') as f:
    f.write(f'只在第一个文件中(共{len(key1 - key2)}条):\n')
    for i in key1 - key2:
        f.write('"%s": "%s",\n' % (i, data1[i].replace('\n', '\\n')))
    f.write(f'只在第二个文件中(共{len(key2 - key1)}条):\n')
    for i in key2 - key1:
        f.write('"%s": "%s",\n' % (i, data2[i].replace('\n', '\\n')))
        
