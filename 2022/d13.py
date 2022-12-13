#python 3.7.1
from re        import compile 
from pprint    import pprint
from copy      import deepcopy  
from numpy     import array,rot90,vectorize 
from numpy     import apply_along_axis as apply
from numpy     import linspace, sign, prod, where
from functools import cmp_to_key

    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
def split(data, delimiter):
  chunk = []
  for line in data:
    if line == delimiter:
      yield chunk 
      chunk = []
      continue 
    chunk.append(line)
  if chunk: yield chunk
    
    
def prepare_data(data):
  return [
    (eval(a),eval(b)) for a,b in split(data,"")]
  
  
def compare(lhs, rhs):
  def compare_lists(lhs,rhs):
    for l,r in zip(lhs,rhs):
      res = compare(l,r)
      if res != 0: return res
    return sign(len(rhs)-len(lhs))
  return {
    (int ,int ): lambda: sign(rhs-lhs),
    (int ,list): lambda: compare([lhs],rhs),
    (list,int ): lambda: compare(lhs,[rhs]),
    (list,list): lambda: compare_lists(lhs,rhs)
  }[(type(lhs),type(rhs))]()
  
  
def serialize(data):
  for d in data:
    if isinstance(d,list):
      for s in serialize(d): yield s
    else: yield d


def process_1(data):
  result = 0
  for i, (lhs, rhs) in enumerate(data):
    if compare(lhs,rhs)>=0:
      result += (i+1)
  return result
  
def process_2(data):
  result = []
  for lhs, rhs in data:
    result.append(lhs)
    result.append(rhs)
  result.append([[2]])
  result.append([[6]])
  result = list(sorted(result, key=cmp_to_key(compare), reverse=True))
  result_1 = result.index([[2]]) + 1
  result_2 = result.index([[6]]) + 1
  return result_1*result_2
  
data   = list(input_data())
data   = prepare_data(data)
result = process_1(deepcopy(data))
pprint(result)
result = process_2(deepcopy(data))
pprint(result)
