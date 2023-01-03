#python 3.7.1
import numpy as np  
import re

from pprint    import pprint
from copy      import deepcopy  
from itertools import groupby
from functools import reduce

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
def parse_data(data):  
  result = [d.split(",") for d in data]
  result = np.array(result)
  return result.astype(int)

def patterns(n):
  result = np.array(list(range(n)))
  for i in result:
    yield tuple(np.roll(result,i))

def process_1(data):
  count = 0     
  for i,j,k in patterns(3):
    result = data[np.lexsort((
      data[:,i],
      data[:,j],
      data[:,k]))]
    result = result[1:]-result[:-1]        
    mask   = np.ones((3))  
    mask[j]=0
    mask[k]=0
    result = np.all(result==mask,1)
    count += np.count_nonzero(result)
  return ((len(data)*6)-(count*2))

def lrange(begin, end):
  result = []
  point  = deepcopy(begin)
  for i, (b, e) in enumerate(zip(begin,end)):
    for v in range(b+1,e):
      point[i] = v
      result.append(tuple(point))
  return set(result)

def process_2(data):
  points_t = []  
  points_p = []  
  for i,j,k in patterns(3):
    points_c = set()
    select   = data[:,[i,j]]
    groups   = np.unique(select,axis=0)
    for group in groups:
      values = data[np.all(select==group,1)]
      values = values[values[:,k].argsort()]
      for a, b in zip(values[:-1],values[1:]):
        points    = lrange(a,b)
        points_c |= points
        points_p.append(points)
    points_t.append(points_c)
  points_t = reduce(lambda x,y:x&y, points_t)
  while True:
    points_n = []    
    for points in points_p:
      if points <= points_t:
        points_n.append(points)
      else:
        points_t -= points
    if len(points_n) == len(points_p):
      break
    points_p = points_n  
  
  return (len(data)*6 -len(points_p)*2)



data   = list(input_data())
data   = parse_data(data)
result = process_1(deepcopy(data))
print(result)
result = process_2(deepcopy(data))
print(result)
