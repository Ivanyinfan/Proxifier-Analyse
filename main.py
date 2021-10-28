from collections import defaultdict
import enum
import re
TIME_POS = 0
PRO_POS = 2
ADDRESS_POS = 4
MIN_LEN = 6

TYPE_POS = 0
SEND_POS = 1
RECV_POS = 2
MIN_LEN2 = 3

PRO_PATTERN = re.compile('.*.exe')
TYPE_PATTERN = re.compile('^close.*')
BYTE_PATTERN = re.compile('\s*(\d+)\s?bytes')

UNITS = ['B','KB','MB','GB','TB']
def formatNumber(num:int):
    k,i=num/1024,0
    while k>1 and i+1<len(UNITS)-1: k,num,i=k/1024,k,i+1
    return f'{num:.2f}{UNITS[i]}'

file = "C:\\Users\\fany\\Documents\\Proxifier\\Log.txt"
output = "C:\\Users\\fany\\Documents\\Proxifier-Analyse\\Analyse.txt"
f = open(file,'r')
line:str
pro_add_map = defaultdict(lambda: defaultdict(int))
pro_map = defaultdict(int)
valid = 0
for lineNum,line in enumerate (f):
    lLine:list = line.lower().split(maxsplit=5)
    if len(lLine)<MIN_LEN: continue
    pro = PRO_PATTERN.fullmatch(lLine[PRO_POS])
    if not pro: continue
    pro_name:str = pro.string
    address = lLine[ADDRESS_POS]
    half2 = lLine[-1]
    lHalf2 = half2.split(',')
    if len(lHalf2)<MIN_LEN2: continue
    if lHalf2[TYPE_POS]!='close': continue
    sent = BYTE_PATTERN.findall(lHalf2[SEND_POS])
    if len(sent)<1: continue
    sent = int(sent[0])
    receive = BYTE_PATTERN.findall(lHalf2[RECV_POS])
    if len(receive)<1: continue
    receive = int(receive[0])
    valid = valid + 1
    pro_add_map[pro_name][address]+= sent + receive
    pro_map[pro_name] += sent + receive
f.close()
pro_list = list(pro_map.items())
pro_list.sort(key=lambda x: x[1], reverse=True)
pro_add_list = dict()
for pro_name, add_map in pro_add_map.items():
    add_list = list(add_map.items())
    add_list.sort(key=lambda x: x[1], reverse=True)
    pro_add_list[pro_name]=add_list
total = sum(pro_map.values())
for i,e in enumerate(pro_list): pro_list[i]=(e[0], formatNumber(e[1]),f'{e[1]/total:2.2%}')
for pro_name, v in pro_add_list.items():
    for i, e in enumerate(v): v[i]=(e[0], formatNumber(e[1]), f'{e[1]/pro_map[pro_name]:2.2%}')
f = open(output, 'w')
f.write(f'total line: {lineNum}, valid line: {valid}\n\n')
f.write(f'total:\t{formatNumber(total)}\n\n')
for e in pro_list:
    f.write(f'{e[0]}:\t{e[1]}\t{e[2]}\n')
f.write('\n')
for e in pro_list:
    f.write(f'{e[0]}:\t{e[1]}\t{e[2]}\n')
    for add_val in pro_add_list[e[0]]:
        f.write(f'\t{add_val[0]}:\t{add_val[1]}\t{add_val[2]}\n')
    f.write('\n')
f.close()

