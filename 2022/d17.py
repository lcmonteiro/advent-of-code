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
  for line in data:
    return [{'<':-1,'>':1}[c] for c in line]

def process_cave(
  nrocks, rocks, wind, spoint=(4,3), width=7):
    
  def free(p):
    return p not in occupied \
      and 0<p[0]             \
      and 0<p[1]<=width
      
  def profile(h):
    p = []
    for x in range(1,width+1):
      y = 0
      while free((h-y,x)): 
        y += 1
      p.append(y)
    return tuple(p)
    
  count     = 0
  highest   = 0
  r_count   = 0
  r_highest = 0
  occupied  = set()
  history   = dict()  
  while (count + r_count) < nrocks:
    g_rock, i_rock = next(rocks)
    y_rock, x_rock = spoint[0]+highest,spoint[1]
    for direction, begin in wind:
      if begin:
        pattern = (
          i_rock,
          y_rock - highest, 
          profile(highest))
        if pattern in history:
          count_, highest_ = history[pattern]
          d_count   = count-count_
          d_highest = highest-highest_
          d_remain  = int((nrocks-count)/d_count)
          r_count  += d_count   * d_remain
          r_highest+= d_highest * d_remain
          history   = dict()
        history[pattern]=(count,highest)
      x_rock += direction
      if not all(map(free,g_rock(y_rock,x_rock))):
        x_rock -= direction
      y_rock -= 1
      if not all(map(free,g_rock(y_rock,x_rock))):
        y_rock   += 1
        particles = set(g_rock(y_rock,x_rock))
        occupied |= particles
        highest   = [highest]
        highest  += [p[0]for p in particles]
        highest   = max(highest)  
        break
    count += 1
  return highest+r_highest


def rock_horizontal(y,x):
  return [(y,x+i) for i in range(4)]
  
def rock_vertical(y,x):
  return [(y+i,x) for i in range(4)]

def rock_star(y,x):
  s = [(1,0),(2,1),(1,2),(0,1)]
  return [(y+i,x+j) for i,j in s]
    
def rock_lshape(y,x):
  s = [(0,0),(0,1),(0,2),(1,2),(2,2)]
  return [(y+i,x+j) for i,j in s]
  
def rock_square(y,x):
  s = [(0,0),(1,0),(1,1),(0,1)]
  return [(y+i,x+j) for i,j in s]


def process(data, n):
  def rocks(types):
    while True:
      for i, t  in enumerate(types):
        yield t, i
  def wind(pattern):
    while True:
      yield pattern[0], True
      for direction in pattern[1:]:
        yield direction, False     
  return process_cave(
    n, rocks([
      rock_horizontal,
      rock_star,
      rock_lshape,
      rock_vertical,
      rock_square]),
    wind(data))


data   = list(input_data())
data   = parse_data(data)
result = process(deepcopy(data),2022)
print(result)
result = process(deepcopy(data),1000000000000)
print(result)
