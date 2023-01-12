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
    
def prepare_data(data):
  args = np.argwhere(data=='#')
  return {(y,x) for y,x in args}
        
def states_frame(states):
  y_min = min(states,key=lambda x:x[0])[0]
  x_min = min(states,key=lambda x:x[1])[1]
  y_max = max(states,key=lambda x:x[0])[0]
  x_max = max(states,key=lambda x:x[1])[1]
  frame = np.full(
    (y_max-y_min+1,x_max-x_min+1),False)
  for y,x in states:
    frame[y-y_min,x-x_min] = True
  return frame
  
def states_generator(state,seed):
  y,x = state
  sequence = [
    [(y-1,x-1),(y-1,x-0),(y-1,x+1)],
    [(y+1,x-1),(y+1,x-0),(y+1,x+1)],
    [(y-1,x-1),(y-0,x-1),(y+1,x-1)], 
    [(y-1,x+1),(y-0,x+1),(y+1,x+1)]]
    
  step = seed % len(sequence)
  for states in sequence[step:]+sequence[:step]:
    yield states[1], set(states)
  yield state, set()

def states_walk(states, steps):
  cur_states = states
  new_states = set()
  for i in range(steps):
    tmp_states = {}
    for cur in cur_states:
      result = [
        (new, len(states & cur_states)==0)
        for new, states in states_generator(cur,i)]
      if all(map(lambda x:x[1],result)):
        tmp_states.setdefault(cur,[]).append(cur)
        continue        
      new,_ = next(filter(lambda x:x[1],result))
      tmp_states.setdefault(new,[]).append(cur)
    new_states = set()
    for new, cur in tmp_states.items():
      if len(cur)>1: new_states.update(cur)
      else         : new_states.add(new)
    if cur_states == new_states:
      return i+1, states_frame(cur_states)
    cur_states = new_states 
  return steps, states_frame(cur_states)
  
def states_display(states):
  print()
  for row in states_frame(states):
    print(''.join('#' if v else '.'for v in row))
  print()

def process_1(data):
  _,result = states_walk(data,10)
  return result.size - result[result].size


def process_2(data):
  i,_ = states_walk(data,1000000)
  return i

data   = input_data()
data   = parse_data(data)
data   = prepare_data(data)
print(1, process_1(data))
print(2, process_2(data))
