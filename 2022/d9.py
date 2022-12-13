#python 3.7.1
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
from numpy  import array,rot90
from numpy  import apply_along_axis as apply
from numpy  import linspace
from numpy  import sign
    
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
  
  
def parse_data(data):
  result = []
  for d in data:
    d,s = d.split()
    result.append({
      'R':(+int(s),0),
      'L':(-int(s),0),
      'U':(0,+int(s)),
      'D':(0,-int(s))}[d])
  return result 
    
    
def walk_process(data):
  x, y = 0,0
  yield x,y
  for x_len, y_len in data:
    for i in linspace(0,x_len,num=abs(x_len)+1)[1:]:
      yield x+int(i), y
    x += x_len
    for i in linspace(0,y_len,num=abs(y_len)+1)[1:]:
      yield x, y+int(i)
    y += y_len
    
    
def walk_process_next(positions):
  def stretched(head, tail, max_diff=1):
    x_diff = abs(head[0] - tail[0])
    y_diff = abs(head[1] - tail[1])
    return x_diff > max_diff or y_diff > max_diff
     
  def move(head, tail):
    return tuple([
      t + int(sign(h-t)) 
      for h,t in zip(head,tail)])
      
  tail = (0,0)   
  yield tail
  for head in positions:
    if stretched(head,tail):
      tail = move(head,tail)
      yield tail
  
  
def process(data, n):
  data = walk_process(data)
  for i in range(n):
    data = walk_process_next(data)
  return set(data)
  
  
data   = list(input_data())
data   = parse_data(data)
result = process(data,1)
pprint(len(result))
result = process(data,9)
pprint(len(result))
