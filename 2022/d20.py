#python 3.7.1
import numpy as np  
import re

from pprint    import pprint
from copy      import deepcopy as copy 

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
  
def parse_data(data):
  return [int(d) for d in data]  
  
def mixing_process(data_beg, data_nxt):
  for i,d in data_beg:
    if d < 0: data_nxt.reverse()
    index = data_nxt.index((i,d))
    value = data_nxt.pop(index)
    delta = index + abs(d)
    delta = delta % len(data_nxt)
    data_nxt.insert(delta,value)  
    if d < 0: data_nxt.reverse() 
  return data_nxt
    
def process(data, key=1, n=1):
  data_beg = list(enumerate(key*v for v in data))
  data_nxt = list(enumerate(key*v for v in data))
  for i in range(n):
    print(f"mixing {i} ...")
    data_nxt = mixing_process(data_beg,data_nxt)
    #print([d for _,d in data_nxt])
  data  = [d for _,d in data_nxt]
  start = data.index(0)
  return sum(
    data[(start+position)%len(data)]
    for position in [1000,2000,3000])
       
    
data   = input_data()
data   = parse_data(data)
print(1, process(data, 1, 1))
print(2, process(data, 811589153, 10))
