# python 3.7.1
from re     import compile 
from numpy  import max
from pprint import pprint
    
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


def process(data, top=1):
  data = split(data,str())
  data = map(lambda x:map(int,x),data)
  data = map(lambda x:sum(x),    data)
  data = sorted(data)
  data = list(data)
  data = sum(data[-top:])
  return data
    

data = list(input_data())
# PART 1
# data = process(data,1)
data = process(data,3)
print(data)
