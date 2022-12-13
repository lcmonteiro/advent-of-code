#python 3.7.1
from re     import compile 
from pprint import pprint
from copy   import deepcopy  
from numpy  import array,rot90
from numpy  import apply_along_axis as apply
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
  
def parse_data(data):
  return array(
    [[int(c)for c in l]for l in data])

def visible_1(row):
      maximum = -1
      result  = []
      for height in row:
        if height > maximum: 
          maximum = height 
          result.append(True)
        else:
          result.append(False)
      return result
      
def visible_2(row):
  def distance(i):
    cnt,ref = 0,row[i]
    for c in row[i+1:]:
      cnt += 1
      if ref <= c : break
    return cnt
  return [distance(i) for i in range(len(row))]
      
def prepare_data(data, visible, init, merge):
  result = data.copy()
  result.fill(init)
  for i in range(4):
    data   = rot90(data)
    result = rot90(result)
    result = merge(result,apply(visible,1,data))
  return result

data   = list(input_data())
data   = parse_data(data)
result = prepare_data(data,visible_1,0,lambda x,y:x+y)
print((result > 0).sum())
result = prepare_data(data,visible_2,1,lambda x,y:x*y)
print(result.max())
