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

    
RULES = {
  'A X': 1+3, 'A Y': 2+6, 'A Z': 3+0,
  'B X': 1+0, 'B Y': 2+3, 'B Z': 3+6,
  'C X': 1+6, 'C Y': 2+0, 'C Z': 3+3
}

CODEC = {
  'A X': 'A Z', 'A Y': 'A X', 'A Z': 'A Y',
  'B X': 'B X', 'B Y': 'B Y', 'B Z': 'B Z',
  'C X': 'C Y', 'C Y': 'C Z', 'C Z': 'C X'
}

def process_1(data):
  for line in data:
    yield RULES[line]
      
def process_2(data):
  return process_1(
    map(lambda x:CODEC[x], data))
  
  
data = list(input_data())
print(sum(process_1(data)))
print(sum(process_2(data)))
