#python 3.7.1
import numpy as np  
import re

from pprint    import pprint
from copy      import deepcopy as copy 
from itertools import groupby
from functools import reduce

def display(var):
  pprint(var,width=50)

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()


def decode(data):
  translate = {"2":2,"1":1,"0":0,"-":-1,"=":-2}
  return sum([
    (translate[c]*5**i)
    for i, c in enumerate(reversed(data))])
  
def encode(data):
  translate = {2:"2",1:"1",0:"0",-1:"-",-2:"="}
  result  = []
  carrier = 0
  while data:
    data,remain = divmod(data,5)
    remain += carrier
    carrier = 0
    if remain > 2:
      remain -= 5
      carrier = 1
    result.append(remain)
  if carrier:
    result.append(carrier)  
  return ''.join([
    translate[n]
    for n in reversed(result)])
    
def process_1(data):
 return encode(sum(decode(line) for line in data))
   
    
result = input_data() 
result = process_1(result)
print(result)
