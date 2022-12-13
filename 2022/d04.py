#python 3.7.1
from re     import compile 
from pprint import pprint
    
def input_data(end="..."):
  line = input()
  while line != end:
    yield line
    line = input()

def parse_sections(data):
  regex  = compile(r'(\d+)-(\d+),(\d+)-(\d+)')
  result = []
  for line in data:
    found = regex.match(line)
    if found:
      result.append((
        set(range(int(found[1]),int(found[2])+1)),
        set(range(int(found[3]),int(found[4])+1))))
  return result    


def process_1(sections):
  for sec in sections:
    yield {
      True : 0,
      False: 1
    }[all([sec[0]-sec[1],sec[1]-sec[0]])]
  
def process_2(sections):
  for sec in sections:
    yield {
      True : 0,
      False: 1
    }[len(sec[0]|sec[1])==len(sec[0])+len(sec[1])]
  

data = list(input_data())
data = parse_sections(data)
print(sum(process_1(data)))
print(sum(process_2(data)))
