# python 3.7.1
from re     import compile 
from pprint import pprint
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()
    
    
def window(data, size=1, step=1):
  print(range(0,len(data)-size,step))
  for i in range(0,len(data)-size,step):
    yield data[i:i+size]


def process(data, chunk_size=14):
  for i, chunk in enumerate(window(data,chunk_size)):
    if len(set(chunk)) == chunk_size:
      return i + chunk_size


data = list(input_data())
# data = map(lambda d:process(x,4),data) # PART-1
data = map(lambda d:process(x,14),data)
data = list(data)

pprint(data)
