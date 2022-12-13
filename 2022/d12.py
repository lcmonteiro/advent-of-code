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
    
    
def prepare_data(data):
  env = array([list(d) for d in data])
  beg = [p for p in zip(*where(env=="S"))]
  end = [p for p in zip(*where(env=="E"))]
  env[env=="S"] = "a"
  env[env=="E"] = "z"
  # uncomment for part 2
  # beg = [p for p in zip(*where(env=="a"))]
  env = vectorize(lambda x:ord(x))(env)  
  return dict(b=beg,e=end,w=env)
  
    
def process_bfs(beg, end, env, fnext):
  opened,closed,policy = [],[],{}
  opened.extend(beg)
  while opened:
    u = opened.pop(0)
    if u in end:
      result = []
      while u:
        result.append(u)
        u = policy.get(u,None)
      return list(reversed(result))
    for v in fnext(u,env):
      if v in opened or v in closed:
        continue 
      opened.append(v)
      policy[v] = u
    closed.append(u)
      
      
def process(data):
  def fnext(pos,env):
    res   = []    
    r ,c  = pos
    rb,re = max(r-1,0),min(r+2,env.shape[0])
    cb,ce = max(c-1,0),min(c+2,env.shape[1])
    roi   = env[rb:re,c]
    roi   = where(roi<=(env[pos]+1))
    roi   = [(rb+o,c) for o, in zip(*roi)]
    roi.remove(pos)
    res.extend(roi)  
    roi   = env[r,cb:ce]
    roi   = where(roi<=(env[pos]+1))
    roi   = [(r,cb+o) for o, in zip(*roi)]
    roi.remove(pos)
    res.extend(roi)
    return res
  
  result = process_bfs(
    data["b"],
    data["e"],
    data["w"],
    fnext)
  return len(result) - 1
  
  
data   = list(input_data())
data   = prepare_data(data)
result = process(deepcopy(data))
print(result)
