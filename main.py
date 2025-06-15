import os
import sys
import datetime
from generate import *
#ROOTS为用户自定义目录，当%appdata%\ETS不存在或无法识别时使用
ROOTS = ""
# 默认根目录为 Windows %APPDATA%\ETS
APPDATA = os.getenv('APPDATA')
if not APPDATA:
    print('环境变量 APPDATA 未定义。请设置后重试。')
    sys.exit(1)
ROOT = os.path.join(APPDATA, 'ETS')

if not os.path.isdir(ROOT):
    print(f'默认根目录不存在: {ROOT}')
    if not ROOTS == "":
        ROOT=ROOTS
    else:
        sys.exit(1)

# 获取并按创建时间排序子目录
subdirs = []
for name in os.listdir(ROOT):
    full = os.path.join(ROOT, name)
    if os.path.isdir(full):
        ctime = os.path.getctime(full)
        subdirs.append((name, full, ctime))

if not subdirs:
    print(f'在根目录 {ROOT} 下未找到任何子目录。')
    sys.exit(1)

# 按创建时间排序（最早到最近）
subdirs.sort(key=lambda x: x[2])

print('可用数据根目录：')
for idx, (name, full, ctime) in enumerate(subdirs, 1):
    time_str = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{idx}. {name}    创建时间: {time_str}")

# 用户选择
choice = input('请输入要使用的目录序号: ').strip()
try:
    idx = int(choice)
    if idx < 1 or idx > len(subdirs):
        raise ValueError
    selected_root = subdirs[idx-1][1]
except ValueError:
    print('无效的序号，程序退出。')
    sys.exit(1)

print(f'已选择目录: {selected_root}')

# 遍历选定目录下的 content2.json 文件
datas = []
for root, dirs, files in os.walk(rf"{selected_root}", topdown=False):
    for name in files:
        if name == 'content2.json':
            datas.append(os.path.join(root, name))

# 解析并输出
answers = []
for data in datas:
    with open(rf"{data}", 'r', encoding='utf-8') as f:
        content = f.read()
    ans = QuestionType.from_json(content)
    answers.append(ans)
print(answers)
# 渲染结果
to_html(answers, 'result.html')
to_pdf(answers)
