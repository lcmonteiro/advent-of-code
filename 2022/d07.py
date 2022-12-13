#python 3.7.1
'''
'''
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
  
def parse_data(data):
  re_cd = compile(r'. cd (.+)')
  re_ls = compile(r'. ls') 
  re_fd = compile(r'(\d+) (.+)')
  res = {}
  pwd = []
  cnt = 0
  
  for line in data:
    cd = re_cd.match(line)
    if cd:
      if   cnt is not None : res[tuple(pwd)] = cnt
      if   cd[1] == '/' : pwd = []
      elif cd[1] == '..': pwd.pop()
      else              : pwd.append(cd[1])
      cnt               = None
      continue
    ls = re_ls.match(line)
    if ls:
      cnt = 0
      continue
    fd = re_fd.match(line)
    if fd:
      cnt += int(fd[1])
      continue
    if cnt is not None : res[tuple(pwd)] = cnt
  return res

def prepare_data(data):
  result = deepcopy(data)
  for pwd, size in data.items():
    for p in map(lambda i: pwd[:i], range(len(pwd))):
        result[p] += size
  return result

def process_1(data, maximum=100000):
  result = filter(lambda x: x<=maximum, data.values())
  result = sum(result)
  return result

def process_2(data, required=30000000, total=70000000):
  free    = total - data[()]
  missing = required - free
  result  = filter(lambda x: x>=missing, data.values())
  result  = sorted(result)
  return result

data   = list(input_data())
data   = parse_data(data)
data   = prepare_data(data)

pprint(process_1(data))
pprint(process_2(data))
