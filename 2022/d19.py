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
  
def parse_data(data):  
  pattern = re.compile((
   '.+costs (.+) ore'
   '.+costs (.+) ore'
   '.+costs (.+) ore.+and (.+) clay'
   '.+costs (.+) ore.+and (.+) obsidian'))
  result  = []
  for line in data:
    found = pattern.match(line)
    if not found:
      continue
    criteria = np.array((
      (0,int(found[6]),0,int(found[5])),
      (0,0,int(found[4]),int(found[3])),
      (0,0,0,int(found[2])),
      (0,0,0,int(found[1]))))
    identity = np.array((
      (1,0,0,0),
      (0,1,0,0),
      (0,0,1,0),
      (0,0,0,1)))
    result.append((criteria,identity))
  return result    


def maximize_profit(
  environ,fbegin,fnext,fselect,fprofit,timeout):
  previous,current,policy = set(),set(),dict()
  for vstate in fbegin(environ):
    current.add(vstate) 
    policy[vstate] = None
  for i in range(timeout):
    previous,current = current,set()
    for ustate in previous:
      states = fnext(ustate,environ)
      current.update(states)
      for s in states:  
        policy[s] = ustate
    current = fselect(list(current),environ)
  maxstate  = None
  maxprofit = 0
  for ustate in current:
    profit = fprofit(ustate,environ)
    if profit > maxprofit:
      maxstate  = ustate
      maxprofit = profit
  result = []
  state  = maxstate
  while state:
    result.append((state,fprofit(state,environ)))
    state = policy.get(state,None)
  return result, maxprofit

def process(data, timeout):
  def fbegin(env):
    return [((0,0,0,1),(0,0,0,0))]
    
  def fnext(u,env):
    robots, tokens = u
    robots = np.array(robots)
    tokens = np.array(tokens) 
    result = set()
    for criteria,identity in zip(*env):
      if all(criteria<=tokens):
        result.add((
          tuple(robots+identity),
          tuple(tokens-criteria+robots)))
    result.add((
      tuple(robots),
      tuple(tokens+robots)))   
    return result
    
  def fselect(states,env):
    states.sort(reverse=True)
    data   = np.array(states)
    result = []
    while len(data):
      test = data[0]
      data = data[1:]
      mask = np.all(data<=test,(1,2))
      data = data[~mask]
      if any(np.all(data>=test,(1,2))):
        continue
      result.append(tuple(tuple(e)for e in test))
    mvalue = max(result,key=lambda x:x[1])
    mindex = result.index(mvalue)
    return set(result[:min(mindex+10,len(result))])
     
  def fprofit(u,env):
    _,u_tokens = u
    return u_tokens[0]
    
  _,result = maximize_profit(
    data,fbegin,fnext,fselect,fprofit,timeout)
  return result


data   = list(input_data())
data   = parse_data(data)
result = sum(
  process(copy(d),24)*i 
  for i,d in enumerate(data,start=1))
print(1, result)
result = np.prod([
  process(copy(d),32) for d in data[:3]])
print(2, result)
