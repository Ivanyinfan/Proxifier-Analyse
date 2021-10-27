from collections import defaultdict
import enum
import re
TIME_POS = 0
PRO_POS = 2
ADDRESS_POS = 4
# TYPE_POS = 4
# SEND_POS = 5
# RECV_POS = 6
MIN_LEN = 5
TYPE_POS = 0
SEND_POS = 1
RECV_POS = 2
MIN_LEN2 = 3
PRO_PATTERN = re.compile('.*.exe')
TYPE_PATTERN = re.compile('^close.*')
BYTE_PATTERN = re.compile('\s*(\d+)\s?bytes')
file = "C:\\Users\\fany\\Documents\\Proxifier\\Log.txt"
f = open(file,'r')
line:str
pro_add_map = defaultdict(lambda: defaultdict(int))
pro_map = defaultdict(int)
valid = 0
for i,line in enumerate (f):
    lLine:list = line.lower().split()
    if len(lLine)<MIN_LEN: continue
    pro = PRO_PATTERN.fullmatch(lLine[PRO_POS])
    if not pro: continue
    pro_name:str = pro.string
    address = lLine[ADDRESS_POS]
    half2 = ' '.join(lLine[MIN_LEN:])
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
print(f'total line: {i}, valid line: {valid}')
for pro_name, add_map in pro_add_map.items():
    print(f'{pro_name}: {pro_map[pro_name]}')
    for add, value in add_map.items():
        print(f'\t{add}: {value}')

