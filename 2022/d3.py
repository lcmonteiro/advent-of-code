#python 3.7.1
from re        import compile 
from pprint    import pprint
from string    import ascii_letters
from functools import reduce

def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()

def prepare_data(data):
  transform = lambda x:ascii_letters.index(x)+1
  for line in data:
    res = [transform(c) for c in line]
    mid = len(res)>>1
    yield (set(res[:mid]),set(res[mid:]))

def process_1(data):
  for lhs,rhs in data:
    yield sum(lhs&rhs)
      
def process_2(data, step=3):
  for i in range(0,len(data),step):
    group = data[i:i+step]
    group = [lhs|rhs for lhs,rhs in group]
    group = reduce(lambda x,y:x&y, group)
    yield sum(group)
  

data = list(input_data())
data = list(prepare_data(data))

print(sum(process_1(data)))
print(sum(process_2(data)))
