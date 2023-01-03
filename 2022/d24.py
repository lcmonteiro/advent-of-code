#python 3.7.1
import numpy as np  
import re

from pprint    import pprint
from copy      import deepcopy  
from itertools import count

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
def parse_data(data):  
  return np.array([[
   char 
   for j, char in enumerate(line)]
   for i, line in enumerate(data)])
    
def world_generator(data):
  translate = {'>':1,'<':2,'v':4,'^':8,'#':16}
  world = np.zeros(data.shape)
  world = world.astype(int)
  for char,number in translate.items():
    world[data==char]=number 
  moves = [(1,1,1),(2,-1,1),(4,1,0),(8,-1,0)]
  arena = world[1:-1,1:-1]
  for i in count(1):
    for v, s, d in moves:
      mask = (arena&v)==v
      arena[mask] = arena[mask]&(~v)
      mask = np.roll(mask,s,d)
      arena[mask] = arena[mask]|( v)
    yield i, world
  
def states_generator(state):
  y,x = state
  return [(y,x),(y-1,x),(y,x+1),(y+1,x),(y,x-1)]
    
def walk_process(begin, end, generator):
  states={begin}
  police={(0,begin):None}
  for time, arena in generator:
    next_states = set()
    for state in states:
      for next_state in states_generator(state):
        try :
          if arena[next_state] != 0:
            continue
        except:
          continue
        next_states.add(next_state)
    states = next_states
    if end in states:
      return time
        
def process_1(data):
  beg = (0,1)
  end = (data.shape[0]-1,data.shape[1]-2)
  gen = world_generator(data)
  return walk_process(beg,end,gen)

def process_2(data):
  beg  = (0,1)
  end  = (data.shape[0]-1,data.shape[1]-2)
  gen  = world_generator(data)
  time = walk_process(beg,end,gen)
  time = walk_process(end,beg,gen)
  time = walk_process(beg,end,gen)
  return time

data   = input_data()
data   = parse_data(data)
print(1, process_1(data))
print(2, process_2(data))
