#python 3.7.1
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
from numpy  import array,rot90
from numpy  import apply_along_axis as apply
from numpy  import linspace
from numpy  import sign
from numpy  import prod
from numpy  import sort

    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()


def parse_data(data, patterns):  
  patterns = list(map(compile,patterns))
  data     = iter(data)
  result   = []
  while True:
    findings = list()
    for pattern in patterns:
      for line in data:
        found = pattern.match(line)
        if found:
          findings.append(found)
          break
    if len(findings) == len(patterns):
      result.append(findings)
      continue 
    return result
    
      
def prepare_data(data):
  result = []
  for d in data:
    result.append({
      'i':list(map(int,d[0][1].split(', '))),
      'o':eval(f'lambda old:{d[1][1]}'),
      't':eval(f'lambda v:{d[3][1]} if v%{d[2][1]}==0 else {d[4][1]}'),
      'm':int(d[2][1])
     })
  return result
  
    
def process_rounds(data, func, n):
  for i in range(n):
    result = []
    for elem in data:
      items = elem['i']
      elem['i'] = []
      for v in items:
        level = elem['o'](v)
        level = func(level)
        index = elem['t'](level)
        data[index]['i'].append(level)
      result.append(len(items))
    yield i, array(result)
      
      
def process_1(data):
  process   = process_rounds(data,lambda x:int(x/3),20)
  i, result = next(process)
  for i, d in process:
    result += d
  result = sort(result)
  result = prod(result[-2:])
  return result
  
  
def process_2(data):
  limit     = int(prod([d['m'] for d in data]))
  keep      = lambda x:x%limit 
  process   = process_rounds(data,keep,10000)
  i, result = next(process)
  for i, d in process:
    result += d
  result = sort(result)
  result = prod(result[-2:])
  return result
  
  
data   = list(input_data())
data   = parse_data(data, [
  r'.*Starting items: (.*)',
  r'.*Operation: new =(.*)',
  r'.*Test: divisible by(.*)',
  r'.*If true: throw to monkey(.*)',
  r'.*If false: throw to monkey(.*)'])
data   = prepare_data(data)
result = process_1(deepcopy(data))
print(result)
result = process_2(deepcopy(data))
print(result)
