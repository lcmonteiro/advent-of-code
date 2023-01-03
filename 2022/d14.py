#python 3.7.1
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
from numpy  import array,rot90,vectorize 
from numpy  import apply_along_axis as apply
from numpy  import linspace, sign, prod, where
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
def parse_data(data):
  split1 = lambda x: list(map(int,x.split(",")))
  split2 = lambda x: list(map(split1,x.split("->")))
  result = map(split2,data)
  result = map(array,result)
  return list(result)   
    
def prepare_data(data):
  result = set()
  lrange = lambda b,e:linspace(b,e,abs(b-e)+1,True)
  for d in data:
    for b, e in zip(d[:-1],d[1:]):
      for y in lrange(b[0],e[0]):
        result.add((int(y),b[1]))
      for x in lrange(b[1],e[1]):
        result.add((e[0],int(x)))
  return result
  

def process(data):
  maximum = max(map(lambda x:x[1],data))
  maximum0 = max(map(lambda x:x[0],data))
  print(maximum0*maximum)
  print(len(data))
  def walk(pos, env):
    while pos not in env:
      pos = (pos[0],pos[1]+1)
      #if pos[1] > maximum: return None # PART-1
      if pos[1] >= (maximum + 2): 
        return (pos[0], pos[1]-1)
        
    left = (pos[0]-1,pos[1])    
    if left not in env:
      return walk(left,env)
    right = (pos[0]+1,pos[1])    
    if right not in env:
      return walk(right,env)
    return (pos[0], pos[1]-1)
    
  env = deepcopy(data)
  cnt = 0
  while True:
    pos  = walk((500,0),env)
    cnt +=1
    if (cnt%100)==0:
      print(cnt,len(env))
      print(cnt,len(env)-cnt)
    if not pos or pos[1]<=0: 
      break
    env.add(pos)
  return len(env)-len(data)
  
  
data   = list(input_data())
data   = parse_data(data)
data   = prepare_data(data)
result = process(deepcopy(data))
# print(result) # PART-1
print(result+1)
