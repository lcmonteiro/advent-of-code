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
  for line in data:
    param = line.split()
    result.append({
      'addx':lambda:(2,int(param[1])),
      'noop':lambda:(1,0)
    }[param[0]]())
  return result 
    
    
def cpu_process(data):
  register = 1
  for cycles, value in data:
    for i in range(cycles):
      yield register
    register += value
  
    
def display(data):
  data = array(data)
  data = data.reshape((-1,6,40))
  for screen in data:
    for row in screen:
      print(''.join([p for p in row]))
      
  
def process_1(data, init=19, step=40):
  data = list(enumerate(cpu_process(data)))
  data = data[init::step]
  data = [(a+1)*b for a,b in data]
  data = sum(data)
  return data
  
  
def process_2(data, height=6, width=40):
  sprite = list(cpu_process(data))
  crc    = list(range(width))*height
  data   = zip(crc,sprite)
  data = [abs(a-b) for a,b in data]
  data = ['$' if a<2 else ' ' for a in data]
  return data
  
  
data   = list(input_data())
data   = parse_data(data)
result = process_1(data)
print(result)
result = process_2(data)
display(result)
