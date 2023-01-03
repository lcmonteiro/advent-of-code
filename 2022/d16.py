#python 3.7.1
import numpy as np  
import re

from pprint    import pprint
from copy      import deepcopy  
from itertools import combinations
from itertools import product

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
def parse_data(data):  
  pattern = re.compile("Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)")
  result  = []
  for line in data:
    found = pattern.match(line)
    if found:
      result.append((
        found[1],
        found[2],
        found[3].split(", ")))
  return result
    
def prepare_data(data):
  data   = list(sorted(data))
  keys   = {d[0]:i for i, d in enumerate(data)}
  result = []
  for d in data:
    result.append((
      int(d[1]),
      [keys[v] for v in d[2]]))
  return result

def maximize_rewards(
  env, fbegin, fnext, freward, fremain):
  from heapq import heappop, heappush
  backlog = [] 
  policy  = {}
  reward  = {}
  reward_selected = 0
  policy_selected = 0
  for v in fbegin(env):
    potential = fremain(env,v)
    heappush(backlog,(-potential,v))
    policy[v] = None
    reward[v] = 0
  while backlog:
    potential, u = heappop(backlog)
    if -potential <= reward_selected:
        continue
    for v in fnext(env,u):
      vr = reward[u] + freward(env,u,v)
      if v in reward and vr <= reward[v]:
        continue
      potential = vr + fremain(env,v)
      if potential <= reward_selected:
        continue
      heappush(backlog,(-potential,v))
      policy[v] = u
      reward[v] = vr
      if vr <= reward_selected:
        continue
      print(1,vr,v)
      reward_selected = vr
      policy_selected = v
  return policy_selected, policy, reward


def process(data, n=2, timeout=26):
  def fbegin(env):
    return [(
      0, tuple([0]*n), tuple(v[0]for v in env))]
    
  def fnext(env,u):
    time, positions, state = u
    if time >= timeout:
      return set()
    result = set()
    for n in product(*[env[p][1]+[p] for p in positions]):
      s = list(state)
      for i, p in enumerate(n):
        if p == positions[i]:
          s[p] = 0
      s = tuple(s)
      result.add((time+1,n,s))
    return result
    
  def freward(env,u,v):
    u_time,u_positions,u_state = u
    v_time,v_positions,v_state = v
    reward = 0
    
    for p in set(pu for pu, pv in zip(u_positions,v_positions) if pu == pv):
        reward += (u_state[p]*(timeout-v_time))
    return reward
    
  def fremain(env,u):
    time,positions,state  = u
    remain = timeout-time-1
    remain = range(remain,remain-len(state)*2,-2)
    remain = list(remain) * len(positions)
    return sum(v*t for v, t in zip(
      sorted(state,reverse=True),
      sorted(remain,reverse=True)))
    
  node, policy, rewards = maximize_rewards(
    data,
    fbegin,
    fnext,
    freward,
    fremain)
  return rewards[node]


data   = list(input_data())
data   = parse_data(data)
data   = prepare_data(data)
result = process(deepcopy(data),1,30)
print(result)
result = process(deepcopy(data),2,26)
print(result)
