#python 3.7.1
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
from numpy  import array,rot90,pad,ones,zeros
from numpy  import apply_along_axis as apply
from numpy  import linspace,sign,prod,where,vectorize
import numpy as np    
from itertools import combinations

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
  return array([
    [[m[0][1],m[0][2]],[m[0][3],m[0][4]]]
    for m in data]).astype(int)

def display(env):
  for line in env:
    print(''.join(map(str,map(int,list(line)))))
    
def line_equation(a,b):
  m = (b[1]-a[1])/(b[0]-a[0])
  b = (a[1])-(m*a[0])
  return (m,b)
   
def lines_intersection(a,b):
  x=(b[1]-a[1])/(a[0]-b[0])
  y=(a[0]*x)+a[1]
  return (x,y)
    
def process_2(data):
  distance = lambda s, b: sum(abs(b-s))
  radius   = np.sum(abs(data[:,0]-data[:,1]),1)
  center   = data[:,0]
  sensing  = list(zip(center,radius))
  # 
  result_1 = []    
  for (a_c,a_r),(b_c,b_r) in combinations(sensing,2):
    if distance(a_c,b_c) == (a_r+b_r+2):
      result_1.append([array(sorted(
        [a_c[i],a_c[i]+a_r+1,a_c[i]-a_r-1,
         b_c[i],b_c[i]+b_r+1,b_c[i]-b_r-1])[2:4])
        for i in range(2)])
  # find intersection
  result_2 = []
  for (a_x,a_y),(b_x,b_y) in combinations(result_1,2):
    ar1 = line_equation(
      [a_x[0],a_y[0]],[a_x[1],a_y[1]])
    ar2 = line_equation(
      [a_x[1],a_y[0]],[a_x[0],a_y[1]])
    br1 = line_equation(
      [b_x[0],b_y[0]],[b_x[1],b_y[1]])
    br2 = line_equation(
      [b_x[1],b_y[0]],[b_x[0],b_y[1]])
    result_2.append(lines_intersection(ar1,br2))
    result_2.append(lines_intersection(br1,ar2))
  # find the right point
  for p in set(result_2):
    p = array(p).astype(int)
    if all([distance(c,p)>r for c,r in sensing]):
      return p[0]*4000000+p[1]
    

def process_1(data, y=10):
  def fill(sensor, beacon, y_position):
    result    = []
    distance  = sum(abs(beacon-sensor)) + 1
    x_sensor  = sensor[0]
    y_sensor  = sensor[1]
    x_beacon  = beacon[0]
    y_beacon  = beacon[1]
    y_offset  = abs(y_sensor - y_position)
    if y_offset > distance: 
      return result
    result.append((x_sensor,1))
    for i in range(1, distance-y_offset):
      result.append((x_sensor+i,1))
      result.append((x_sensor-i,1))
    if y_sensor == y_position:
      result.append((x_sensor,2))  
    if y_beacon == y_position:
      result.append((x_beacon,3))  
    return result

  result = set()
  for sensor, beacon in data:
    result = result | set(fill(sensor, beacon, y))
  result = np.array(list(result))
  return len(result[result[:,1]==1])-len(result[result[:,1]!=1])

data   = list(input_data())
data   = parse_data(data, [r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)"])
data   = prepare_data(data)
#result = process_1(deepcopy(data),2000000)
#print(result)
result = process_2(deepcopy(data))
print(result)
