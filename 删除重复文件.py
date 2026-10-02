import os, hashlib
def file_md5(fname):
    m = hashlib.md5()
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()
def walk_path(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for f in files:
            # print(os.path.join(root, f))
            fs.append(os.path.join(root, f))
    return fs
dir1 = input('检查目录:')
dir2 = input('对比目录:')
files1 = walk_path(dir1)
same_file = []
for i in files1:
    file = dir2 + os.sep + os.sep.join(i.split(os.sep)[1:])
    if os.path.isfile(file) and file_md5(i) == file_md5(file):
            same_file.append(dir1 + os.sep + os.sep.join(i.split(os.sep)[1:]))
input(f'共有{len(same_file)}个文件相同,是否删除?(enter确定)')
for i in same_file:
    print(f'删除{i}')
    os.remove(i)
